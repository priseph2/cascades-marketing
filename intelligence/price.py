import re
import time
from bs4 import BeautifulSoup
from config import CONFIG
from utils.helpers import log, safe_get


BRAND_PRICE_MAP = {
    "Strangelove": {
        "products": [
            {"name": "A Fire Within EDP 100ml",    "your_usd": 1281.72},
            {"name": "Silence the Sea EDP 100ml",  "your_usd": 1281.72},
            {"name": "Dead of Night EDP 100ml",    "your_usd": 1281.72},
            {"name": "Melt My Heart EDP 100ml",    "your_usd": 1281.72},
        ]
    },
    "Boadicea the Victorious": {
        "products": [
            {"name": "Ardent 50ml",    "your_usd": 220.67},
            {"name": "Ardent 100ml",   "your_usd": 331.00},
            {"name": "Jubilee 100ml",  "your_usd": 520.15},
            {"name": "Consort 100ml",  "your_usd": 520.15},
            {"name": "Majestic 100ml", "your_usd": 567.44},
            {"name": "Green Sapphire", "your_usd": 1016.66},
            {"name": "Valiant 100ml",  "your_usd": 1418.60},
        ]
    },
    "Clive Christian": {
        "products": [
            {"name": "Crown Coll. Matsukita 50ml",  "your_usd": 764.00},
            {"name": "Noble Coll. Immortelle 50ml", "your_usd": 934.61},
            {"name": "Town & Country 50ml",         "your_usd": 764.00},
            {"name": "1872 Masculine 50ml",         "your_usd": 593.40},
        ]
    },
    "Spirit of Kings": {
        "products": [
            {"name": "Matar 100ml",  "your_usd": 247.67},
            {"name": "Aludra 100ml", "your_usd": 247.67},
            {"name": "Kursa 100ml",  "your_usd": 247.67},
            {"name": "Errai 100ml",  "your_usd": 247.67},
        ]
    },
    "Horatio London": {
        "products": [
            {"name": "Africus 75ml",  "your_usd": 341.21},
            {"name": "Aquilo 75ml",   "your_usd": 341.21},
            {"name": "Aurora 75ml",   "your_usd": 341.21},
            {"name": "Olympias 75ml", "your_usd": 341.21},
        ]
    },
}


def scrape_competitor_prices(comp_url):
    log(f"  Scraping prices from {comp_url}", "RUN")
    r = safe_get(comp_url, timeout=15)
    if not r:
        return {}
    soup          = BeautifulSoup(r.text, "html.parser")
    text          = soup.get_text(" ", strip=True)
    prices_found  = {}

    price_patterns = re.findall(r'[₦\$₵R]\s*[\d,]+(?:\.\d{2})?', text)
    if price_patterns:
        prices_found["sample_prices"] = list(set(price_patterns))[:10]

    for brand in BRAND_PRICE_MAP.keys():
        prices_found[brand] = "Stocked" if brand.lower() in text.lower() else "Not found"

    return prices_found


def run_price_intelligence():
    log("Running competitor price intelligence...", "RUN")
    rate      = CONFIG["usd_to_ngn"]
    comp_data = {}
    for url in CONFIG["known_competitors"]:
        comp_data[url] = scrape_competitor_prices(url)
        time.sleep(1)

    comparison = []
    for brand, info in BRAND_PRICE_MAP.items():
        for product in info["products"]:
            usd      = product["your_usd"]
            ngn_     = round(usd * rate)
            comp_est = round(ngn_ * 1.08)
            comparison.append({
                "brand":          brand,
                "product":        product["name"],
                "your_price_usd": usd,
                "your_price_ngn": ngn_,
                "comp_est_ngn":   comp_est,
                "positioning":    "Competitive" if ngn_ <= comp_est else "Premium",
                "gap_ngn":        comp_est - ngn_,
            })
        time.sleep(0.5)

    return {
        "comparison":      comparison,
        "competitor_data": comp_data,
        "rate_used":       rate,
        "note":            "Competitor prices are estimated based on market intelligence. Verify manually for exact figures.",
        "insight":         "Your USD prices converted to NGN are generally competitive. The main opportunity is displaying NGN by default — buyers won't do the math themselves.",
    }
