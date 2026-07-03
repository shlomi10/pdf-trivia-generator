import openai
import os
import fitz
from dotenv import load_dotenv
import json
import re
from io import BytesIO
import random

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(s: str, chunk_size: int = 15000, overlap: int = 800):
    if chunk_size <= 0:
        return [s]
    chunks = []
    i = 0
    n = len(s)
    while i < n:
        end = min(i + chunk_size, n)
        chunks.append(s[i:end])
        if end == n:
            break
        i = end - overlap
        if i < 0:
            i = 0
    return chunks

def _normalize_question_key(q: str) -> str:
    q = q.strip().lower()
    q = re.sub(r"[^\w\s]", "", q, flags=re.UNICODE)
    return re.sub(r"\s+", " ", q).strip()


def _is_metadata_question(q: str) -> bool:
    return bool(re.search(
        r"\b(author|writer|publisher|published|publication|isbn|copyright|"
        r"table of contents|dedication|foreword|preface|page number|"
        r"printed by|edition|press|bibliograph)\b|"
        r"תוכן עניינים|מחבר|סופר|הוצאה|מהדורה|זכויות יוצרים",
        q,
        re.IGNORECASE,
    ))


def _clean_and_validate(items, seen=None):
    if seen is None:
        seen = set()
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        q = it.get("question")
        opts = it.get("options")
        ans = it.get("answer")
        if not isinstance(q, str) or not isinstance(opts, list) or len(opts) != 4 or not all(isinstance(o, str) for o in opts):
            continue
        if ans not in opts:
            continue
        if _is_metadata_question(q):
            continue
        key = _normalize_question_key(q)
        if not key or key in seen:
            continue
        if any(
            key[:40] == s[:40] or (len(key) > 20 and (key in s or s in key))
            for s in seen
        ):
            continue
        seen.add(key)
        out.append({"question": q.strip(), "options": [o.strip() for o in opts], "answer": ans.strip()})
    return out


def _select_text_parts(text: str, num_parts: int = 1) -> list[str]:
    if len(text) < 12000:
        return [text]
    chunks = chunk_text(text, chunk_size=15000, overlap=800)
    if len(chunks) <= num_parts:
        return chunks
    body_chunks = chunks[1:] if len(chunks) > 2 else chunks
    return random.sample(body_chunks, min(num_parts, len(body_chunks)))


def _ask_gpt(text, k, avoid_questions=None, lang="en"):
    avoid_clause = ""
    if avoid_questions:
        listed = "\n".join(f"- {q}" for q in avoid_questions[:20])
        avoid_clause = (
            f"Do NOT repeat or closely paraphrase any of these existing questions:\n{listed}\n"
        )
    lang_clause = ""
    if lang == "he":
        lang_clause = "Write all questions and all four answer options in Hebrew.\n"
    sys = (
        "You generate trivia questions from any document type (book, article, report, resume, "
        "lecture notes, etc.) and output only valid JSON arrays."
    )
    usr = (
        f"Create exactly {k} trivia questions strictly from the text below.\n"
        f"First infer what kind of document this is, then ask questions that are relevant to its "
        f"actual subject matter and main information.\n"
        f"Examples by document type:\n"
        f"- Book or story: events, ideas, arguments, lessons, relationships between parts of the text.\n"
        f"- Article or essay: claims, evidence, conclusions, key concepts.\n"
        f"- Resume or CV: roles, skills, experience, education, projects, achievements.\n"
        f"- Report or manual: procedures, findings, recommendations, definitions, facts.\n"
        f"Use a mix of easy and moderate difficulty. Questions may require understanding, not only memorizing a single word.\n"
        f"NEVER ask about document packaging or metadata, including: table of contents, chapter or section "
        f"listings, page numbers, author or writer name, publisher, publication date, ISBN, copyright, "
        f"dedications, preface credits, headers, footers, cover page details, or any bibliographic information.\n"
        f"Each question must be clearly distinct from the others. Vary topics and angles.\n"
        f"All four options must be short and distinct. The correct answer must be one of the options.\n"
        f"Return ONLY a JSON array of objects with fields: question, options (exactly 4), answer.\n"
        f"If you cannot find enough substantive content, return as many as you can, but never fabricate.\n"
        f"{lang_clause}"
        f"{avoid_clause}"
        f"Text:\n{text}"
    )
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": sys}, {"role": "user", "content": usr}],
        max_tokens=2000,
        temperature=0.7,
    )
    raw = r.choices[0].message.content
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        data = json.loads(m.group(0)) if m else []
    return _clean_and_validate(data if isinstance(data, list) else [])

def generate_trivia_from_pdf(file_bytes: bytes, num_questions: int = 3, lang: str = "en"):
    text = extract_text_from_pdf(file_bytes)
    if not text or not text.strip():
        return []
    num_parts = 1 if num_questions <= 5 else 2
    parts = _select_text_parts(text, num_parts)
    all_items = []
    seen_keys = set()
    for p in parts:
        needed = num_questions - len(all_items)
        if needed <= 0:
            break
        request_k = needed + min(3, max(1, needed // 2))
        items = _ask_gpt(
            p,
            request_k,
            avoid_questions=[item["question"] for item in all_items],
            lang=lang,
        )
        for item in _clean_and_validate(items, seen_keys):
            all_items.append(item)
            if len(all_items) >= num_questions:
                break
    random.shuffle(all_items)
    return all_items[:num_questions]
