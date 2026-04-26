from datetime import datetime
from utils.helpers import sl


def compile_full_report(store_url, pagespeed, ux, products, checkout, competitors, seo, woo_data, revenue_impact, price_intel):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scores    = [
        pagespeed.get("mobile",  {}).get("performance", 0),
        ux.get("score", 0),
        checkout.get("score", 0),
        seo.get("score", 0),
    ]
    if products:
        scores.append(round(sum(p["score"] for p in products) / len(products)))
    overall = round(sum(scores) / len(scores))

    report = {
        "meta":           {"generated_at": timestamp, "store_url": store_url, "version": "2.0"},
        "overall_score":  overall,
        "overall_label":  sl(overall),
        "pagespeed":      pagespeed,
        "ux_audit":       ux,
        "seo_audit":      seo,
        "product_pages":  products,
        "checkout":       checkout,
        "competitors":    competitors,
        "woo_data":       woo_data,
        "revenue_impact": revenue_impact,
        "price_intel":    price_intel,
    }
    return report, overall
