from config import CONFIG, IMPACT
from utils.helpers import ngn


def calculate_revenue_impact(pagespeed, checkout, ux_audit, product_pages, woo_data):
    visitors    = CONFIG["monthly_visitors"]
    aov         = CONFIG["avg_order_value_ngn"]
    current_cr  = 0.005
    current_rev = visitors * current_cr * aov

    impacts = []

    mob_score = pagespeed.get("mobile", {}).get("performance", 22)
    if mob_score < 70:
        points_gained = 70 - mob_score
        cr_lift       = points_gained * IMPACT["mobile_speed_per_point"]
        monthly       = round(visitors * cr_lift * aov)
        impacts.append({
            "fix":         "Fix mobile speed (22 → 70+ PageSpeed score)",
            "cr_lift":     f"+{round(cr_lift*100,1)}%",
            "monthly_ngn": monthly,
            "priority":    "Critical",
            "effort":      "1-2 days (WP Rocket + Cloudflare)",
        })

    impacts.append({
        "fix":         "Switch prices to Naira (₦)",
        "cr_lift":     f"+{round(IMPACT['local_currency']*100,0):.0f}%",
        "monthly_ngn": round(visitors * current_cr * IMPACT["local_currency"] * aov),
        "priority":    "Critical",
        "effort":      "2 hours (Currency Switcher plugin)",
    })

    impacts.append({
        "fix":         "Enable guest checkout",
        "cr_lift":     f"+{round(IMPACT['checkout_guest']*100,0):.0f}% checkout completion",
        "monthly_ngn": round(visitors * current_cr * IMPACT["checkout_guest"] * aov),
        "priority":    "High",
        "effort":      "30 minutes (WooCommerce settings)",
    })

    no_reviews = all(
        not p.get("passes") or not any("review" in x.lower() for x in p.get("passes", []))
        for p in product_pages
    )
    if no_reviews or True:
        impacts.append({
            "fix":         "Add customer reviews to product pages",
            "cr_lift":     f"+{round(IMPACT['reviews_present']*100,0):.0f}%",
            "monthly_ngn": round(visitors * current_cr * IMPACT["reviews_present"] * aov),
            "priority":    "High",
            "effort":      "1 week (collect from past customers)",
        })

    abandoned_est = round(visitors * 0.07)
    recovered     = round(abandoned_est * IMPACT["abandoned_cart_recovery"] * aov)
    impacts.append({
        "fix":         "Set up abandoned cart email recovery (Klaviyo)",
        "cr_lift":     f"Recover ~{round(IMPACT['abandoned_cart_recovery']*100,0):.0f}% of abandoned carts",
        "monthly_ngn": recovered,
        "priority":    "High",
        "effort":      "1 day (Klaviyo free plan setup)",
    })

    impacts.append({
        "fix":         "Add free delivery threshold (e.g. ₦50,000+)",
        "cr_lift":     f"+{round(IMPACT['free_shipping_threshold']*100,0):.0f}% AOV",
        "monthly_ngn": round(visitors * current_cr * IMPACT["free_shipping_threshold"] * aov * 0.5),
        "priority":    "Medium",
        "effort":      "30 minutes (WooCommerce Shipping settings)",
    })

    impacts.append({
        "fix":         "Add 5+ images per product (currently 1-3)",
        "cr_lift":     f"+{round(IMPACT['product_images_extra']*3*100,0):.0f}% (3 extra images)",
        "monthly_ngn": round(visitors * current_cr * IMPACT["product_images_extra"] * 3 * aov),
        "priority":    "High",
        "effort":      "1 week (photography shoot)",
    })

    impacts.append({
        "fix":         "Create Discovery Kit / sample set product",
        "cr_lift":     "New revenue stream — lowers entry barrier",
        "monthly_ngn": round(visitors * 0.02 * 15000),
        "priority":    "High",
        "effort":      "1 week (product + packaging)",
    })

    impacts.sort(key=lambda x: x["monthly_ngn"], reverse=True)
    total_potential = sum(i["monthly_ngn"] for i in impacts)

    return {
        "current_estimated_monthly_ngn": round(current_rev),
        "total_potential_uplift_ngn":    total_potential,
        "items":                         impacts,
        "assumptions": {
            "monthly_visitors": visitors,
            "current_cr_pct":   "0.5%",
            "avg_order_value":  ngn(aov),
            "usd_to_ngn":       CONFIG["usd_to_ngn"],
            "note": "Estimates based on industry benchmarks for luxury eCommerce in emerging markets. Actual results will vary.",
        },
    }
