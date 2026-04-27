import time
import requests
from bs4 import BeautifulSoup
from config import CONFIG
from utils.helpers import safe_get


OUR_BRANDS = [
    "strangelove", "boadicea", "clive christian", "spirit of dubai",
    "fragrance du bois", "bois 1920", "lord milano", "pantheon roma",
    "spirit of kings", "essential parfum", "oman luxury",
]


def analyze_competitor(url):
    result = {
        "url":                   url,
        "title":                 "",
        "meta_description":      "",
        "h1":                    [],
        "h2":                    [],
        "keywords_found":        [],
        "brands_found":          [],
        "has_blog":              False,
        "has_schema":            False,
        "has_reviews":           False,
        "internal_link_count":   0,
        "error":                 None,
    }
    try:
        r = safe_get(url, timeout=15)
        if not r:
            result["error"] = "Could not fetch page"
            return result

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        if soup.title:
            result["title"] = soup.title.string.strip()

        meta = soup.find("meta", {"name": "description"})
        if meta:
            result["meta_description"] = meta.get("content", "").strip()

        result["h1"] = [h.get_text(strip=True) for h in soup.find_all("h1")][:5]
        result["h2"] = [h.get_text(strip=True) for h in soup.find_all("h2")][:10]

        target_kws = CONFIG.get("target_keywords", [])
        result["keywords_found"] = [kw for kw in target_kws if kw.lower() in text]
        result["brands_found"]   = [b for b in OUR_BRANDS if b in text]

        result["has_blog"]    = any(x in text[:3000] for x in ["blog", "journal", "article", "magazine"])
        result["has_schema"]  = bool(soup.find("script", {"type": "application/ld+json"}))
        result["has_reviews"] = any(x in text for x in ["review", "rating", "stars", "verified buyer"])

        all_links      = soup.find_all("a", href=True)
        domain         = url.split("//")[-1].split("/")[0]
        result["internal_link_count"] = sum(
            1 for a in all_links
            if domain in a["href"] or a["href"].startswith("/")
        )
    except Exception as e:
        result["error"] = str(e)

    return result


def run_competitor_seo_analysis():
    competitors = CONFIG.get("known_competitors", [])
    results     = []

    for url in competitors:
        data = analyze_competitor(url)
        results.append(data)
        time.sleep(1)

    our_keywords  = set(CONFIG.get("target_keywords", []))
    comp_keywords = set()
    for r in results:
        comp_keywords.update(r.get("keywords_found", []))

    comp_only = comp_keywords - our_keywords
    our_only  = our_keywords  - comp_keywords
    shared    = our_keywords  & comp_keywords

    comp_brands = set()
    for r in results:
        comp_brands.update(r.get("brands_found", []))
    brand_gaps = [b for b in OUR_BRANDS if b not in comp_brands]

    return {
        "competitors":                results,
        "shared_keywords":            sorted(shared),
        "competitor_only_keywords":   sorted(comp_only),
        "our_unique_keywords":        sorted(our_only),
        "brands_not_on_competitors":  brand_gaps,
        "gap_summary": (
            f"{len(comp_only)} keyword(s) competitors target that we don't; "
            f"{len(our_only)} keyword(s) we target uniquely; "
            f"{len(brand_gaps)} of our brand(s) absent from competitor sites"
        ),
    }
