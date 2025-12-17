"""
Document downloading and parsing module.

This module handles fetching and extracting text from various document formats:
- PDF files: Extracted using pypdf
- HTML pages: Parsed using BeautifulSoup with script/style removal

The module automatically detects file type based on URL extension.
"""

import os
from typing import Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO


def get_file_extension_from_url(url: str) -> str:
    """
    Extract the file extension from a URL path.
    
    Args:
        url: The full URL to parse.
    
    Returns:
        The lowercase file extension (e.g., ".pdf", ".html") or empty string.
    
    Example:
        >>> get_file_extension_from_url("https://example.com/report.pdf")
        '.pdf'
    """
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext.lower()


def download_content(url: str) -> bytes:
    """
    Download raw bytes from a URL.
    
    Uses httpx with automatic redirect following and a 30-second timeout.
    
    Args:
        url: The URL to download from.
    
    Returns:
        The raw bytes content of the response.
    
    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        httpx.TimeoutException: If the request times out after 30 seconds.
    """
    with httpx.Client(follow_redirects=True, timeout=30.0) as http_client:
        resp = http_client.get(url)
        resp.raise_for_status()
        return resp.content


def parse_pdf_bytes(pdf_bytes: bytes, max_pages: Optional[int] = None) -> str:
    """
    Extract text content from PDF bytes.
    
    Args:
        pdf_bytes: The raw PDF file content as bytes.
        max_pages: Optional limit on number of pages to extract.
                   If None, extracts all pages.
    
    Returns:
        The extracted text from all (or limited) pages, joined by double newlines.
    
    Example:
        >>> with open("report.pdf", "rb") as f:
        ...     text = parse_pdf_bytes(f.read(), max_pages=10)
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
            continue

    return "\n\n".join(texts)


def parse_html_bytes(html_bytes: bytes) -> str:
    """
    Extract visible text from HTML bytes.
    
    Removes script, style, and noscript tags before extracting text.
    Cleans up whitespace and empty lines.
    
    Args:
        html_bytes: The raw HTML content as bytes.
    
    Returns:
        Clean text content with one element per line.
    """
    html = html_bytes.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def fetch_and_parse_url(url: str, max_pdf_pages: Optional[int] = 20) -> str:
    """
    Download a URL and extract its text content.
    
    Automatically detects whether the URL points to a PDF or HTML page
    and uses the appropriate parser.
    
    Args:
        url: The URL to fetch and parse.
        max_pdf_pages: Maximum PDF pages to extract (default 20).
                       Ignored for HTML content.
    
    Returns:
        The extracted plain text content.
    
    Raises:
        httpx.HTTPStatusError: If download fails.
    
    Example:
        >>> text = fetch_and_parse_url("https://tourism.gov/forecast.pdf")
        >>> print(f"Extracted {len(text)} characters")
    """
    ext = get_file_extension_from_url(url)
    raw = download_content(url)

    if ext == ".pdf":
        return parse_pdf_bytes(raw, max_pages=max_pdf_pages)
    else:
        return parse_html_bytes(raw)
