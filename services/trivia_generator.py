import math
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

def _clean_and_validate(items):
    out = []
    seen = set()
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
        key = q.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append({"question": q.strip(), "options": [o.strip() for o in opts], "answer": ans.strip()})
    return out

def _ask_gpt(text, k):
    sys = "You are a careful generator that outputs only valid JSON arrays."
    usr = (
        f"Create exactly {k} VERY EASY trivia questions strictly from the text. "
        f"Use only obvious, basic facts from the provided text. No trick or hard questions. "
        f"All four options must be short and distinct. The correct answer must be one of the options. "
        f"Return ONLY a JSON array of objects with fields: question, options (exactly 4), answer. "
        f"If you cannot find enough facts, return as many as you can, but never fabricate. "
        f"Text:\n{text}"
    )
    r = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "system", "content": sys}, {"role": "user", "content": usr}],
        max_completion_tokens=600,
        top_p=1,
        reasoning_effort="low"
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

def generate_trivia_from_pdf(file_bytes: bytes, num_questions: int = 3):
    text = extract_text_from_pdf(file_bytes)
    if not text or not text.strip():
        return []
    if len(text) < 12000:
        parts = [text]
    else:
        parts = chunk_text(text, chunk_size=15000, overlap=800)[:2]
    per_part = max(1, math.ceil(num_questions / max(1, len(parts))))
    all_items = []
    for p in parts:
        items = _ask_gpt(p, per_part)
        all_items.extend(items)
        if len(all_items) >= num_questions:
            break
    all_items = _clean_and_validate(all_items)
    random.shuffle(all_items)
    return all_items[:num_questions]
