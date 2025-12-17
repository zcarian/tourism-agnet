"""
Main pipeline module for tourism projection extraction.

This module orchestrates the entire extraction process:
1. Search for official tourism documents by country
2. Download and parse each document (PDF or HTML)
3. Classify documents to identify those with projections
4. Extract structured projection data from relevant documents
5. Save results to a JSON file

Run this module directly to execute the pipeline:
    python src/pipeline.py
"""

from typing import List, Dict, Any
from tqdm import tqdm

from extract import classify_document, extract_projections
from search import search_official_tourism_docs
from parser import fetch_and_parse_url


def process_document_for_country(country: str, url: str) -> Dict[str, Any]:
    """
    Download, parse, classify, and extract data from a single document.
    
    This is the core processing function that handles one document URL.
    It downloads the content, classifies it, and extracts projections
    if the document contains relevant forecast data.
    
    Args:
        country: The country this document relates to.
        url: The URL of the document to process.
    
    Returns:
        A result dictionary containing:
        - country (str): The country name
        - url (str): The source URL
        - status (str): "ok" or "error"
        - classification (dict): Classification results (if successful)
        - extracted (dict or None): Extracted projections (if applicable)
        - error (str): Error message (if status is "error")
    """
    print(f"\n=== Processing URL for {country} ===")
    print(url)
    
    try:
        text = fetch_and_parse_url(url)
        print(f"  Downloaded and parsed document, length={len(text)} characters")
    except Exception as e:
        print(f"  ERROR downloading/parsing {url}: {e}")
        return {
            "country": country,
            "url": url,
            "status": "error",
            "error": str(e),
        }

    classification = classify_document(text)
    print("  Classification:", classification)

    if classification.get("contains_projections"):
        extracted = extract_projections(text, country, url)
        print("  Extracted projections:", extracted)
    else:
        extracted = None

    return {
        "country": country,
        "url": url,
        "status": "ok",
        "classification": classification,
        "extracted": extracted,
    }


def run_country_pipeline(country: str) -> List[Dict[str, Any]]:
    """
    Run the extraction pipeline for all documents from a single country.
    
    Searches for document URLs, then processes each one in sequence
    with a progress bar.
    
    Args:
        country: The country name to process (e.g., "USA", "Spain").
    
    Returns:
        A list of result dictionaries, one per processed document.
    """
    urls = search_official_tourism_docs(country)
    if not urls:
        print(f"No URLs found for {country}. Add some in search.py HARDCODED_SOURCES.")
        return []

    results = []
    for url in tqdm(urls, desc=f"Processing {country}"):
        result = process_document_for_country(country, url)
        results.append(result)

    return results


def main():
    """
    Main entry point for the tourism projections pipeline.
    
    Processes all configured countries and saves results to
    classification_results.json in the current directory.
    
    To add more countries, modify the countries list below or
    update HARDCODED_SOURCES in search.py.
    """
    countries = ["USA"]

    all_results = []
    for c in countries:
        res = run_country_pipeline(c)
        all_results.extend(res)

    import json
    with open("classification_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("\nSaved classification_results.json")


if __name__ == "__main__":
    main()
