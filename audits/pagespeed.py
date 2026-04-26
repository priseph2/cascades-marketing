import time
from utils.helpers import log, safe_get, sl


def run_pagespeed_audit(url, api_key):
    log(f"Running PageSpeed audit on {url}", "RUN")
    results = {}
    for strategy in ["mobile", "desktop"]:
        endpoint = (
            f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            f"?url={url}&strategy={strategy}&key={api_key}"
        )
        r = None
        for attempt in range(1, 4):
            r = safe_get(endpoint, timeout=90)
            if r:
                break
            wait = attempt * 10
            log(f"  PageSpeed {strategy} attempt {attempt} failed — retrying in {wait}s", "WARN")
            time.sleep(wait)

        if not r:
            log(f"  PageSpeed {strategy} failed after 3 attempts", "ERROR")
            results[strategy] = {"error": "API call failed after 3 attempts", "performance": 0}
            continue

        data   = r.json()
        cats   = data.get("lighthouseResult", {}).get("categories", {})
        audits = data.get("lighthouseResult", {}).get("audits", {})
        perf   = round((cats.get("performance",   {}).get("score", 0) or 0) * 100)
        seo_s  = round((cats.get("seo",           {}).get("score", 0) or 0) * 100)
        acc    = round((cats.get("accessibility",  {}).get("score", 0) or 0) * 100)
        bp     = round((cats.get("best-practices", {}).get("score", 0) or 0) * 100)
        results[strategy] = {
            "performance":    perf,
            "seo":            seo_s,
            "accessibility":  acc,
            "best_practices": bp,
            "lcp":            audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
            "tbt":            audits.get("total-blocking-time",       {}).get("displayValue", "N/A"),
            "cls":            audits.get("cumulative-layout-shift",   {}).get("displayValue", "N/A"),
            "speed_index":    audits.get("speed-index",               {}).get("displayValue", "N/A"),
            "opportunities": [
                {"title": v.get("title", ""), "savings": v.get("displayValue", "")}
                for k, v in audits.items()
                if v.get("score") is not None and v.get("score") < 0.9
                and v.get("details", {}).get("type") == "opportunity"
            ][:5],
        }
        log(f"  {strategy.capitalize()} Performance: {perf} ({sl(perf)})", "OK")
        time.sleep(2)
    return results
