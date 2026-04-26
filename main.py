import os
import json
import time
from datetime import datetime

from config import CONFIG
from utils.helpers import log, sl, ngn
from history.tracker import load_history, save_history, compute_run_diff, compute_weekly_summary
from audits.pagespeed import run_pagespeed_audit
from audits.ux import audit_store_ux
from audits.seo import run_seo_audit
from audits.products import audit_product_pages
from audits.checkout import audit_checkout
from audits.competitors import audit_competitors
from integrations.woocommerce import get_woo_store_data
from intelligence.revenue import calculate_revenue_impact
from intelligence.price import run_price_intelligence
from reporting.compiler import compile_full_report
from reporting.pdf_generator import generate_pdf


def run_audit():
    print("\n" + "="*62)
    print("  PERFUME eCOMMERCE AUDIT AGENT  v2.0")
    print("  scentifiedperfume.com")
    print("="*62 + "\n")

    if not CONFIG["store_url"]:
        CONFIG["store_url"] = input("Store URL: ").strip()
    if not CONFIG["woo_consumer_key"]:
        CONFIG["woo_consumer_key"] = input("WooCommerce Consumer Key (Enter to skip): ").strip()
    if not CONFIG["woo_consumer_secret"] and CONFIG["woo_consumer_key"]:
        CONFIG["woo_consumer_secret"] = input("WooCommerce Consumer Secret: ").strip()

    store_url = CONFIG["store_url"].rstrip("/")
    start     = time.time()
    history   = load_history()

    pagespeed      = run_pagespeed_audit(store_url, CONFIG["pagespeed_api_key"])
    ux             = audit_store_ux(store_url)
    seo            = run_seo_audit(store_url)
    products       = audit_product_pages(store_url, CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])
    checkout       = audit_checkout(store_url)
    competitors    = audit_competitors(CONFIG["known_competitors"])
    woo_data       = get_woo_store_data()
    revenue_impact = calculate_revenue_impact(pagespeed, checkout, ux, products, woo_data)
    price_intel    = run_price_intelligence()

    report, overall = compile_full_report(
        store_url, pagespeed, ux, products, checkout,
        competitors, seo, woo_data, revenue_impact, price_intel
    )

    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(CONFIG["output_dir"], f"audit_{ts}.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    history_entry = {
        "date":           datetime.now().strftime("%Y-%m-%d %H:%M"),
        "overall_score":  overall,
        "mobile_speed":   pagespeed.get("mobile", {}).get("performance", 0),
        "ux_score":       ux.get("score", 0),
        "seo_score":      seo.get("score", 0),
        "checkout_score": checkout.get("score", 0),
    }

    run_diff       = compute_run_diff(history, history_entry)
    weekly_summary = compute_weekly_summary(history + [history_entry])

    report["run_diff"]       = run_diff
    report["weekly_summary"] = weekly_summary

    history  = save_history(history, history_entry)
    pdf_path = generate_pdf(report, history[:-1], CONFIG["output_dir"])

    elapsed = round(time.time() - start, 1)
    print("\n" + "="*62)
    print(f"  AUDIT COMPLETE  ({elapsed}s)")
    print(f"  Overall Score  : {overall}/100 - {sl(overall)}")
    if run_diff.get("available"):
        delta = run_diff["diffs"]["overall_score"]["delta"]
        arrow = "^" if delta > 0 else ("v" if delta < 0 else "=")
        print(f"  vs Last Run    : {arrow} {abs(delta)} pts  ({run_diff['previous_date']})")
    if weekly_summary.get("available"):
        print(f"  Weekly Health  : {weekly_summary['health']}")
    print(f"  JSON           : {json_path}")
    print(f"  PDF            : {pdf_path}")
    print(f"  History        : {len(history)} audit runs tracked")
    if weekly_summary.get("available"):
        print(f"  Weekly Summary : {CONFIG['output_dir']}/weekly_summary.json")
    print("="*62 + "\n")

    return report, json_path, pdf_path


if __name__ == "__main__":
    run_audit()
