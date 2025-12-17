from typing import List


def search_official_tourism_docs(country: str) -> List[str]:
    """
    MVP: return a hard-coded list of URLs per country.

    Later we'll replace this with a real web search.
    For now, put 1–2 official tourism strategy/forecast URLs here.
    """
    hardcoded = {
        "USA": [
            "https://www.ustravel.org/research/travel-forecasts"
        ],
        "Spain": [
            "https://www.tourism-review.com/increasing-numbers-of-international-travelers-to-turn-spain-in-destination-no-1-news14657"
        ],
    }

    return hardcoded.get(country, [])
