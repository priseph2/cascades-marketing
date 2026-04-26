import requests
from datetime import datetime
from config import CONFIG
from utils.helpers import log, safe_get, ngn


def woo_api(endpoint, params=None):
    base = CONFIG["store_url"].rstrip("/")
    url  = f"{base}/wp-json/wc/v3/{endpoint}"
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])
    r = safe_get(url, auth=auth, timeout=20)
    if not r:
        return None
    try:
        return r.json()
    except Exception:
        return None


def get_woo_store_data():
    log("Pulling WooCommerce store data...", "RUN")
    if not CONFIG["woo_consumer_key"]:
        log("No WooCommerce API keys — skipping deep store data", "WARN")
        return None

    data = {}

    products = woo_api("products?per_page=50&status=publish")
    if products:
        data["total_products"]           = len(products)
        data["products_no_image"]        = [p["name"] for p in products if not p.get("images")]
        data["products_no_description"]  = [p["name"] for p in products if not p.get("description")]
        data["products_no_reviews"]      = [p["name"] for p in products if int(p.get("rating_count", 0)) == 0]
        data["out_of_stock"]             = [p["name"] for p in products if p.get("stock_status") == "outofstock"]
        data["low_stock"]                = [p["name"] for p in products if p.get("stock_quantity") and int(p["stock_quantity"]) < 3]
        prices                           = [float(p.get("price", 0)) for p in products if p.get("price")]
        data["price_range_usd"]          = {"min": min(prices) if prices else 0, "max": max(prices) if prices else 0}
        data["products_list"]            = [
            {"name": p["name"], "price": p.get("price", ""), "stock": p.get("stock_quantity", "?"),
             "rating": p.get("average_rating", "0"), "reviews": p.get("rating_count", 0)}
            for p in products[:20]
        ]
        log(f"  {data['total_products']} products found via API", "OK")

    from_date = datetime.now().strftime("%Y-%m-01T00:00:00")
    orders = woo_api(f"orders?per_page=50&after={from_date}&status=completed,processing")
    if orders:
        data["orders_this_month"]        = len(orders)
        revenue                          = sum(float(o.get("total", 0)) for o in orders)
        data["revenue_usd_this_month"]   = revenue
        data["revenue_ngn_this_month"]   = revenue * CONFIG["usd_to_ngn"]
        aov                              = revenue / len(orders) if orders else 0
        data["aov_usd"]                  = round(aov, 2)
        data["aov_ngn"]                  = round(aov * CONFIG["usd_to_ngn"])
        log(f"  {data['orders_this_month']} orders this month | Revenue: {ngn(data['revenue_ngn_this_month'])}", "OK")

    data["abandoned_cart_note"] = "Install WooCommerce Cart Abandonment Recovery plugin for exact data"
    return data
