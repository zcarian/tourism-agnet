"""
Document source search module.

This module provides functions to find official tourism documents
for different countries. Currently uses a hardcoded list of URLs
as an MVP implementation.

To add more countries:
1. Find official tourism ministry/board websites
2. Look for strategy documents, forecasts, or annual reports
3. Add the URLs to the HARDCODED_SOURCES dictionary below
"""

from typing import List


HARDCODED_SOURCES = {
    "USA": [
        "https://www.ustravel.org/research/travel-forecasts"
    ],
    "Spain": [
        "https://www.tourism-review.com/increasing-numbers-of-international-travelers-to-turn-spain-in-destination-no-1-news14657"
    ],
}

#TODO create a function that will search for the documents in the web
def search_official_tourism_docs(country: str) -> List[str]:
    """
    Get a list of official tourism document URLs for a country.
    
    Currently returns hardcoded URLs as an MVP. Future versions will
    implement actual web search functionality.
    
    Args:
        country: The country name to search for (e.g., "USA", "Spain").
                 Must match a key in HARDCODED_SOURCES exactly.
    
    Returns:
        A list of URLs pointing to tourism documents for that country.
        Returns an empty list if the country is not configured.
    
    Example:
        >>> urls = search_official_tourism_docs("USA")
        >>> for url in urls:
        ...     print(url)
    
    To add a new country, update HARDCODED_SOURCES at the top of this file:
        HARDCODED_SOURCES["France"] = [
            "https://example.com/france-tourism-report.pdf"
        ]
    """
    return HARDCODED_SOURCES.get(country, [])
