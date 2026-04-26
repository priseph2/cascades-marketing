"""
Fetches published WooCommerce products with their current RankMath SEO data.

Usage: py tools/fetch_seo_data.py                    # all products (no filter)
       py tools/fetch_seo_data.py --no-seo            # products with no RankMath title set
       py tools/fetch_seo_data.py --brand "BTV"       # filter by brand category
       py tools/fetch_seo_data.py --limit 20          # cap results
       py tools/fetch_seo_data.py --no-seo --limit 20
"""
import sys
import json
import time
import requests

sys.path.insert(0, ".")
from config import CONFIG


def fetch_page(base, auth, page):
    for attempt in range(1, 4):
        try:
            r = requests.get(
                f"{base}/wp-json/wc/v3/products",
                auth=auth,
                params={"per_page": 100, "status": "publish", "page": page},
                timeout=60,
            )
            r.raise_for_status()
            return r
        except Exception as e:
            if attempt == 3:
                raise
            wait = attempt * 10
            sys.stderr.write(f"Page {page} attempt {attempt} failed ({e}) — retrying in {wait}s\n")
            time.sleep(wait)


def fetch_all_products():
    base = CONFIG["store_url"].rstrip("/")
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])
    all_products = []
    page = 1
    while True:
        r = fetch_page(base, auth, page)
        batch = r.json()
        if not batch:
            break
        all_products.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", 1))
        sys.stderr.write(f"Fetched page {page}/{total_pages} ({len(batch)} products)\n")
        if page >= total_pages:
            break
        page += 1
        time.sleep(1)
    return all_products


def get_meta(meta_data, key):
    for m in meta_data:
        if m["key"] == key:
            return m.get("value", "")
    return ""


def main():
    no_seo_only  = "--no-seo" in sys.argv
    brand_filter = None
    limit        = None
    id_filter    = None

    if "--brand" in sys.argv:
        idx = sys.argv.index("--brand")
        brand_filter = sys.argv[idx + 1].lower()

    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])

    if "--ids" in sys.argv:
        idx = sys.argv.index("--ids")
        id_filter = set(int(x) for x in sys.argv[idx + 1].split(","))

    products = fetch_all_products()

    results = []
    for p in products:
        meta       = p.get("meta_data", [])
        categories = [c["name"] for c in p.get("categories", [])]
        rm_title   = get_meta(meta, "rank_math_title")
        rm_desc    = get_meta(meta, "rank_math_description")

        if id_filter and p["id"] not in id_filter:
            continue

        if no_seo_only and rm_title:
            continue

        if brand_filter:
            if not any(brand_filter in cat.lower() for cat in categories):
                continue

        images      = p.get("images", [])[:1]
        results.append({
            "id":                       p["id"],
            "name":                     p["name"],
            "permalink":                p.get("permalink", ""),
            "slug":                     p.get("slug", ""),
            "price":                    p.get("price", ""),
            "categories":               categories,
            "description":              p.get("description", ""),
            "short_description":        p.get("short_description", ""),
            "current_seo_title":        rm_title,
            "current_seo_desc":         rm_desc,
            "current_focus_keyword":    get_meta(meta, "rank_math_focus_keyword"),
            "image_srcs":               [img["src"] for img in images],
            "image_ids":                [img["id"]  for img in images],
            "image_alts":               [img.get("alt", "") for img in images],
        })

    if limit:
        results = results[:limit]

    print(json.dumps(results, indent=2))
    sys.stderr.write(f"Found {len(results)} products\n")


if __name__ == "__main__":
    main()
