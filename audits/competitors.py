import time
from bs4 import BeautifulSoup
from utils.helpers import log, safe_get, sl


def audit_competitors(urls):
    log("Auditing competitors...", "RUN")
    results = []
    checks  = {
        "has_video":         ["video", "youtube"],
        "has_discovery_kit": ["discovery", "sample", "travel size"],
        "has_loyalty":       ["loyalty", "reward", "earn points"],
        "has_bundle":        ["bundle", "gift set", "buy 2"],
        "has_reviews":       ["review", "rating", "stars"],
        "has_newsletter":    ["newsletter", "subscribe"],
        "has_chat":          ["chat", "whatsapp", "tawk"],
        "has_free_shipping": ["free shipping", "free delivery"],
        "has_urgency":       ["limited", "low stock", "selling fast"],
    }
    for url in urls:
        r = safe_get(url)
        if not r:
            results.append({"url": url, "accessible": False, "score": 0, "features": {}, "strengths": [], "weaknesses": []})
            continue
        text     = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True).lower()
        features = {k: any(kw in text for kw in v) for k, v in checks.items()}
        score    = min(sum(1 for v in features.values() if v) * 11, 100)
        results.append({
            "url":        url,
            "accessible": True,
            "score":      score,
            "label":      sl(score),
            "features":   features,
            "strengths":  [k.replace("has_", "").replace("_", " ").title() for k, v in features.items() if v],
            "weaknesses": [k.replace("has_", "").replace("_", " ").title() for k, v in features.items() if not v],
        })
        time.sleep(2)
    return results
