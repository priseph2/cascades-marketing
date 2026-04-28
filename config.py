import os

# Load .env for local development (file is gitignored — safe to put real credentials there)
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

CONFIG = {
    "store_url":           os.environ.get("STORE_URL",           "https://scentifiedperfume.com"),
    "woo_consumer_key":    os.environ.get("WOO_CONSUMER_KEY",    ""),
    "woo_consumer_secret": os.environ.get("WOO_CONSUMER_SECRET", ""),
    "pagespeed_api_key":    os.environ.get("PAGESPEED_API_KEY",   ""),
    "monthly_visitors":    500,
    "avg_order_value_ngn": 220000,
    "usd_to_ngn":          1600,
    "output_dir":          "./audit_reports",
    "history_file":        "./audit_reports/score_history.json",
    "known_competitors": [
        "https://fragrances.com.ng/",
        "https://www.edgars.co.za",
    ],
    "target_keywords": [
        "buy perfume Nigeria",
        "luxury perfume Lagos",
        "niche perfume Nigeria",
        "Strangelove perfume Nigeria",
        "Boadicea the Victorious Nigeria",
        "Clive Christian perfume Lagos",
        "perfume gift set Nigeria",
        "best perfume shop Lagos",
    ],
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}

# Industry benchmarks for luxury eCommerce
IMPACT = {
    "mobile_speed_per_point":   0.002,
    "checkout_guest":           0.25,
    "reviews_present":          0.18,
    "local_currency":           0.12,
    "product_images_extra":     0.08,
    "abandoned_cart_recovery":  0.12,
    "free_shipping_threshold":  0.15,
}
