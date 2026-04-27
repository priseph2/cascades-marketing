import time
import requests
from config import CONFIG


SEED_KEYWORDS = [
    "perfume Nigeria",
    "buy perfume Lagos",
    "niche perfume Nigeria",
    "luxury perfume Nigeria",
    "perfume gift Nigeria",
]

BRAND_KEYWORDS = [
    "Strangelove perfume Nigeria",
    "Boadicea the Victorious Nigeria",
    "Clive Christian perfume Lagos",
    "Spirit of Dubai Nigeria",
    "Fragrance du Bois Nigeria",
]


def _pytrends_available():
    try:
        import pytrends  # noqa: F401
        return True
    except ImportError:
        return False


def get_autocomplete(query):
    try:
        r = requests.get(
            "https://suggestqueries.google.com/complete/search",
            params={"client": "firefox", "q": query, "hl": "en-NG"},
            timeout=8,
        )
        if r.status_code == 200:
            return r.json()[1]
    except Exception:
        pass
    return []


def get_trends_data(keywords):
    if not _pytrends_available():
        return {"error": "pytrends not installed — trends unavailable"}
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl="en-US", tz=60, timeout=(10, 25), retries=2, backoff_factor=0.5)
        chunks = [keywords[i:i+5] for i in range(0, len(keywords), 5)]
        combined = {}
        for chunk in chunks:
            try:
                pt.build_payload(chunk, timeframe="today 12-m", geo="NG")
                df = pt.interest_over_time()
                if not df.empty:
                    for kw in chunk:
                        if kw in df.columns:
                            vals = df[kw]
                            combined[kw] = {
                                "avg":   round(float(vals.mean()), 1),
                                "max":   int(vals.max()),
                                "trend": "up" if vals.iloc[-4:].mean() > vals.iloc[:4].mean() else "down",
                            }
                time.sleep(2)
            except Exception as e:
                for kw in chunk:
                    combined[kw] = {"error": str(e)}
        return combined
    except Exception as e:
        return {"error": str(e)}


def get_related_queries(keyword):
    if not _pytrends_available():
        return {"error": "pytrends not installed"}
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl="en-US", tz=60, timeout=(10, 25), retries=2, backoff_factor=0.5)
        pt.build_payload([keyword], timeframe="today 12-m", geo="NG")
        related = pt.related_queries()
        result = {}
        if keyword in related:
            top    = related[keyword].get("top")
            rising = related[keyword].get("rising")
            if top is not None and not top.empty:
                result["top"]    = top.head(10).to_dict("records")
            if rising is not None and not rising.empty:
                result["rising"] = rising.head(10).to_dict("records")
        return result
    except Exception as e:
        return {"error": str(e)}


def run_keyword_research():
    autocomplete = {}
    for kw in SEED_KEYWORDS:
        autocomplete[kw] = get_autocomplete(kw)
        time.sleep(0.5)

    for kw in BRAND_KEYWORDS[:3]:
        autocomplete[kw] = get_autocomplete(kw)
        time.sleep(0.5)

    trends  = get_trends_data(SEED_KEYWORDS)
    related = get_related_queries("perfume Nigeria")

    return {
        "autocomplete":    autocomplete,
        "trends":          trends,
        "related_queries": related,
        "seed_keywords":   SEED_KEYWORDS,
        "brand_keywords":  BRAND_KEYWORDS,
    }
