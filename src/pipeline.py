from typing import List, Dict, Any
from tqdm import tqdm

from extract import classify_document, extract_projections
from search import search_official_tourism_docs
from parser import fetch_and_parse_url
from extract import classify_document


def process_document_for_country(country: str, url: str) -> Dict[str, Any]:
    """
    Download, parse, and classify a single document.
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

    # If the document actually contains projections → extract them
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
    urls = search_official_tourism_docs(country)
    if not urls:
        print(f"No URLs found for {country}. Add some in search_official_tourism_docs().")
        return []

    results = []
    for url in tqdm(urls, desc=f"Processing {country}"):
        result = process_document_for_country(country, url)
        results.append(result)

    return results


def main():
    countries = ["USA"]  # start with one, expand later

    all_results = []
    for c in countries:
        res = run_country_pipeline(c)
        all_results.extend(res)

    # Save to file
    import json
    with open("classification_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("\nSaved classification_results.json")


if __name__ == "__main__":
    main()
