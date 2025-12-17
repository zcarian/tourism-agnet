import os
from typing import Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO


def get_file_extension_from_url(url: str) -> str:
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext.lower()


def download_content(url: str) -> bytes:
    """
    Download raw bytes from the URL.
    """
    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.content


def parse_pdf_bytes(pdf_bytes: bytes, max_pages: Optional[int] = None) -> str:
    """
    Extract text from PDF bytes using pypdf.
    """
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = reader.pages
    if max_pages is not None:
        pages = pages[:max_pages]

    texts = []
    for page in pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            # ignore pages that fail
            continue

    return "\n\n".join(texts)


def parse_html_bytes(html_bytes: bytes) -> str:
    """
    Extract visible text from HTML using BeautifulSoup.
    """
    html = html_bytes.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    # strip scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def fetch_and_parse_url(url: str, max_pdf_pages: Optional[int] = 20) -> str:
    """
    Download URL and return plain text (PDF or HTML).
    """
    ext = get_file_extension_from_url(url)
    raw = download_content(url)

    if ext == ".pdf":
        return parse_pdf_bytes(raw, max_pages=max_pdf_pages)
    else:
        # default: treat as HTML
        return parse_html_bytes(raw)
