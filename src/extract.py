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
    Use Hugging Face model to classify whether a document contains future tourism projections.
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
        # Fallback if the model misbehaves
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
    Extract numerical FUTURE tourism projections (arrivals & revenue)
    from a document using the HF model.
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
        # Fallback: return empty result
        data = {
            "country": country,
            "source_url": url,
            "projections": [],
            "raw": content,
        }

    return data
