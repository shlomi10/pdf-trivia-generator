import openai
import os
import fitz
from dotenv import load_dotenv
import json
import re
from io import BytesIO
import random

'''
Extracts content from PDFs and sends it to OpenAI API to generate trivia questions.
'''

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tone_variants = [
    "Focus on fun and surprising facts.",
    "Use a mix of easy and hard questions.",
    "Try to include tricky or less obvious facts.",
    "Favor unique or unexpected details.",
    "Prioritize questions that could stump even experts."
]

tone = random.choice(tone_variants)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def generate_trivia_from_pdf(file_path, num_questions=3):
    text = extract_text_from_pdf(file_path)
    prompt = (
        f"Create exactly {num_questions} trivia questions from the following text. "
        f"{tone} Return ONLY a JSON array of objects. Each must contain:\n"
        "- question: string\n"
        "- options: list of 4 strings\n"
        "- answer: one of the options\n\n"
        f"Text:\n{text[:3000]}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=1.2,
        top_p=0.85
    )

    raw = response.choices[0].message.content
    print("\n📦 Raw GPT response:")
    print(raw)

    try:
        parsed = json.loads(raw)
        print("\n✅ Parsed trivia:")
        print(parsed)
        return parsed
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            print("\n✅ Extracted JSON from fallback regex:")
            print(parsed)
            return parsed
        else:
            print("\n❌ Failed to parse trivia response.")
            return []
