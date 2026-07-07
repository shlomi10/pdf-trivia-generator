import openai
import os
import fitz
from dotenv import load_dotenv
import json
import re
from io import BytesIO
import random
from concurrent.futures import ThreadPoolExecutor

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
        explanation = it.get("explanation")
        explanation = explanation.strip() if isinstance(explanation, str) else ""
        out.append({
            "question": q.strip(),
            "options": [o.strip() for o in opts],
            "answer": ans.strip(),
            "explanation": explanation,
        })
    return out


def _select_text_parts(text: str, num_parts: int = 1) -> list[str]:
    if len(text) < 8000:
        return [text]
    chunks = chunk_text(text, chunk_size=8000, overlap=500)
    if len(chunks) <= num_parts:
        return chunks
    body_chunks = chunks[1:] if len(chunks) > 2 else chunks
    return random.sample(body_chunks, min(num_parts, len(body_chunks)))


DIFFICULTY_CLAUSES = {
    "easy": (
        "Difficulty: EASY. Ask about facts stated explicitly in the text; the correct answer "
        "should be directly and clearly supported, and the distractors clearly wrong.\n"
    ),
    "medium": (
        "Difficulty: MEDIUM. Require understanding and connecting ideas across the text, not just "
        "recalling a single word; the distractors should be plausible.\n"
    ),
    "hard": (
        "Difficulty: HARD. Require inference, nuance, and careful reading; use closely related, "
        "plausible distractors that demand real understanding to rule out.\n"
    ),
}


def _ask_gpt(text, k, avoid_questions=None, lang="en", difficulty="medium"):
    avoid_clause = ""
    if avoid_questions:
        listed = "\n".join(f"- {q}" for q in avoid_questions[:20])
        avoid_clause = (
            f"Do NOT repeat or closely paraphrase any of these existing questions:\n{listed}\n"
        )
    difficulty_clause = DIFFICULTY_CLAUSES.get(difficulty, DIFFICULTY_CLAUSES["medium"])
    lang_clause = ""
    if lang == "he":
        lang_clause = "Write all questions, all four answer options, and every explanation in Hebrew.\n"
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
        f"{difficulty_clause}"
        f"NEVER ask about document packaging or metadata, including: table of contents, chapter or section "
        f"listings, page numbers, author or writer name, publisher, publication date, ISBN, copyright, "
        f"dedications, preface credits, headers, footers, cover page details, or any bibliographic information.\n"
        f"Each question must be clearly distinct from the others. Vary topics and angles.\n"
        f"All four options must be short and distinct. The correct answer must be one of the options.\n"
        f"For each question also add a very short explanation (one concise sentence, about 15 words "
        f"maximum) grounded in the text that says why the correct answer is right.\n"
        f"Return ONLY a JSON array of objects with fields: question, options (exactly 4), answer, explanation.\n"
        f"If you cannot find enough substantive content, return as many as you can, but never fabricate.\n"
        f"{lang_clause}"
        f"{avoid_clause}"
        f"Text:\n{text}"
    )
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": sys}, {"role": "user", "content": usr}],
        max_tokens=min(2000, k * 200 + 300),
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

PER_CALL_MAX = 12
TARGET_PER_CALL = 5
MAX_PARALLEL_CALLS = 10
MAX_ROUNDS = 2


def _split_progressive(n: int):
    base = n // 3
    counts = [base, base, base]
    for i in range(n % 3):
        counts[i] += 1
    return list(zip(("easy", "medium", "hard"), counts))


def _run_calls_parallel(specs, lang, difficulty):
    def _worker(spec):
        text, k, avoid = spec
        try:
            return _ask_gpt(text, k, avoid_questions=avoid, lang=lang, difficulty=difficulty)
        except Exception:
            return []

    with ThreadPoolExecutor(max_workers=min(len(specs), MAX_PARALLEL_CALLS)) as ex:
        return list(ex.map(_worker, specs))


def _generate_for_difficulty(text, num_questions, lang, difficulty, seen_keys, avoid_base=None):
    oversampled = (num_questions * 13) // 10
    num_calls = max(1, min(MAX_PARALLEL_CALLS, (oversampled + TARGET_PER_CALL - 1) // TARGET_PER_CALL))
    parts = _select_text_parts(text, num_calls)
    if not parts:
        return []
    per_call = min(PER_CALL_MAX, (num_questions + num_calls - 1) // num_calls + 2)
    result = []
    for round_idx in range(MAX_ROUNDS):
        if len(result) >= num_questions:
            break
        remaining = num_questions - len(result)
        calls_this_round = max(1, (remaining + TARGET_PER_CALL - 1) // TARGET_PER_CALL)
        avoid = (avoid_base or []) + [item["question"] for item in result]
        specs = [
            (parts[(round_idx * calls_this_round + c) % len(parts)], per_call, avoid)
            for c in range(calls_this_round)
        ]
        added_before = len(result)
        for items in _run_calls_parallel(specs, lang, difficulty):
            for item in _clean_and_validate(items, seen_keys):
                result.append(item)
                if len(result) >= num_questions:
                    break
        if len(result) == added_before:
            break
    return result


def generate_trivia_from_pdf(file_bytes: bytes, num_questions: int = 3, lang: str = "en", difficulty: str = "medium", exclude_questions=None):
    text = extract_text_from_pdf(file_bytes)
    if not text or not text.strip():
        return []
    exclude_questions = exclude_questions or []
    exclude_keys = {_normalize_question_key(q) for q in exclude_questions}
    if difficulty == "progressive":
        levels = [(level, n) for level, n in _split_progressive(num_questions) if n > 0]
        with ThreadPoolExecutor(max_workers=len(levels)) as ex:
            batches = list(ex.map(
                lambda ln: _generate_for_difficulty(text, ln[1], lang, ln[0], set(exclude_keys), avoid_base=exclude_questions),
                levels,
            ))
        ordered = []
        seen = set(exclude_keys)
        for batch in batches:
            for item in batch:
                key = _normalize_question_key(item["question"])
                if key in seen:
                    continue
                seen.add(key)
                ordered.append(item)
        return ordered[:num_questions]
    items = _generate_for_difficulty(text, num_questions, lang, difficulty, set(exclude_keys), avoid_base=exclude_questions)
    random.shuffle(items)
    return items[:num_questions]
