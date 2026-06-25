import urllib.request

from services.aws_file_utils import get_presigned_url_from_key

DEFAULT_PDFS = {
    "alice_in_wonderland": {
        "title_en": "Alice in Wonderland",
        "title_he": "עליסה בארץ הפלאות",
        "filename": "alice_in_wonderland.pdf",
        "s3_key": "pdf/2a08f2f4-0967-45fc-b48d-d6cefd9b9a97_alice_in_wonderland.pdf",
    }
}

PRESIGNED_URL_EXPIRES_IN = 3600


def get_default_pdf_s3_key(pdf_id: str) -> str:
    if pdf_id not in DEFAULT_PDFS:
        raise ValueError(f"Unknown default PDF: {pdf_id}")
    return DEFAULT_PDFS[pdf_id]["s3_key"]


def get_default_pdf_presigned_url(pdf_id: str, expires_in: int = PRESIGNED_URL_EXPIRES_IN) -> tuple[str, str]:
    if pdf_id not in DEFAULT_PDFS:
        raise ValueError(f"Unknown default PDF: {pdf_id}")
    key = DEFAULT_PDFS[pdf_id]["s3_key"]
    return get_presigned_url_from_key(key, expires_in=expires_in), key


def _fetch_bytes_from_presigned_url(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:
        return response.read()


def get_default_pdf_bytes(pdf_id: str) -> tuple[bytes, str]:
    url, key = get_default_pdf_presigned_url(pdf_id)
    return _fetch_bytes_from_presigned_url(url), key


def list_default_pdfs() -> list[dict]:
    return [
        {"id": pdf_id, **meta}
        for pdf_id, meta in DEFAULT_PDFS.items()
    ]
