"""
Document classification and data extraction module.

This module provides functions to:
1. Classify documents to determine if they contain tourism projections
2. Extract structured projection data (visitor arrivals, revenue forecasts)

The module uses a Hugging Face LLM to analyze document text and return
structured JSON responses.
"""

from typing import Dict, Any
from textwrap import shorten
import json

from config import client


CLASSIFIER_SYSTEM_PROMPT = """
You are a JSON-only classifier for tourism documents.

Task:
Given some text from a document, decide if it contains
quantitative FUTURE projections of tourism (visitor arrivals and/or tourism revenue).

You MUST respond with a single JSON object and NOTHING else.

JSON schema:
{
  "contains_projections": boolean,
  "projection_type": "arrivals" | "revenue" | "both" | "none",
  "years_mentioned": [int, ...],
  "confidence": float
}
"""


def classify_document(text: str, max_chars: int = 4000) -> Dict[str, Any]:
    """
    Classify whether a document contains future tourism projections.
    
    Uses a Hugging Face LLM to analyze the document text and determine
    if it contains quantitative forecasts for tourism arrivals or revenue.
    
    Args:
        text: The full text content of the document to classify.
        max_chars: Maximum characters to send to the model (default 4000).
                   Longer documents are truncated to fit within token limits.
    
    Returns:
        A dictionary containing:
        - contains_projections (bool): Whether the document has projections
        - projection_type (str): "arrivals", "revenue", "both", or "none"
        - years_mentioned (list): Years referenced in projections
        - confidence (float): Model's confidence score (0.0 to 1.0)
    
    Example:
        >>> result = classify_document("Tourism arrivals expected to reach 50M by 2025")
        >>> result["contains_projections"]
        True
    """
    short_text = shorten(text, width=max_chars, placeholder="... [TRUNCATED] ...")

    messages = [
        {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
        {"role": "user", "content": short_text},
    ]

    resp = client.chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.0,
    )

    content = resp.choices[0].message["content"]

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {
            "contains_projections": False,
            "projection_type": "none",
            "years_mentioned": [],
            "confidence": 0.0,
            "raw": content,
        }

    return data


def extract_projections(text: str, country: str, url: str, max_chars: int = 8000) -> Dict[str, Any]:
    """
    Extract numerical tourism projections from a document.
    
    Parses the document text to find and structure future tourism forecasts,
    including visitor arrival numbers and revenue projections.
    
    Args:
        text: The full text content of the document.
        country: The country this document relates to (e.g., "USA", "Spain").
        url: The source URL of the document (for reference tracking).
        max_chars: Maximum characters to analyze (default 8000).
    
    Returns:
        A dictionary containing:
        - country (str): The country name
        - source_url (str): Where the data came from
        - projections (list): List of projection objects, each with:
            - indicator: "arrivals" or "revenue"
            - year: The forecast year (int)
            - value: The projected number
            - unit: "visitors", "USD", "EUR", or "local_currency"
    
    Example:
        >>> result = extract_projections(doc_text, "USA", "https://example.com/forecast.pdf")
        >>> for proj in result["projections"]:
        ...     print(f"{proj['year']}: {proj['value']} {proj['unit']}")
    """
    short_text = shorten(text, width=max_chars, placeholder="... [TRUNCATED] ...")

    SYSTEM_PROMPT = """
    You are a data extraction assistant.
    Your job is to extract quantitative FUTURE tourism projections from the document.

    Return ONLY a VALID JSON object.
    
    JSON schema:
    {
      "country": string,
      "source_url": string,
      "projections": [
        {
          "indicator": "arrivals" | "revenue",
          "year": int,
          "value": number,
          "unit": "visitors" | "USD" | "EUR" | "local_currency"
        }
      ]
    }
    
    IMPORTANT RULES:
    - Only extract *future projections*, not historical numbers.
    - If you are unsure, include an empty list.
    - Do NOT include explanations.
    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": short_text}
    ]

    resp = client.chat_completion(
        messages=messages,
        max_tokens=2048,
        temperature=0.0,
    )

    content = resp.choices[0].message["content"]

    try:
        data = json.loads(content)
    except Exception:
        data = {
            "country": country,
            "source_url": url,
            "projections": [],
            "raw": content,
        }

    return data
