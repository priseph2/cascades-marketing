"""
Fetches published WooCommerce products and outputs a JSON array to stdout.

Usage: py tools/fetch_no_desc.py                          # products missing descriptions
       py tools/fetch_no_desc.py --all                    # all products
       py tools/fetch_no_desc.py --has-desc               # products WITH descriptions (old or new format)
       py tools/fetch_no_desc.py --needs-reformat         # products with old-format descriptions (no <h3> tag)
       py tools/fetch_no_desc.py --needs-reformat --brand "BTV"  # filter by brand category name
       py tools/fetch_no_desc.py --no-image               # products with no images at all
       py tools/fetch_no_desc.py --no-image --brand "BTV" # no-image products for one brand
       py tools/fetch_no_desc.py --limit 10               # cap results
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

def is_new_format(description):
    """Returns True if description already uses the new SEO template (has <h3> tags)."""
    return "<h3>" in description

def main():
    include_all      = "--all"            in sys.argv
    has_desc_only    = "--has-desc"       in sys.argv
    needs_reformat   = "--needs-reformat" in sys.argv
    no_image_only    = "--no-image"       in sys.argv
    brand_filter     = None
    limit            = None

    if "--brand" in sys.argv:
        idx = sys.argv.index("--brand")
        brand_filter = sys.argv[idx + 1].lower()

    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])

    products = fetch_all_products()

    results = []
    for p in products:
        desc      = p.get("description", "")
        has_desc  = bool(desc.strip())
        has_short = bool(p.get("short_description", "").strip())
        categories = [c["name"] for c in p.get("categories", [])]
        images    = p.get("images", [])

        if no_image_only:
            # Only products with no images
            if images:
                continue
        elif needs_reformat:
            # Only products that have a description but are NOT in the new format
            if not has_desc or is_new_format(desc):
                continue
        elif has_desc_only:
            if not has_desc:
                continue
        elif not include_all:
            # Default: only products missing descriptions
            if has_desc:
                continue

        # Brand filter (case-insensitive substring match against any category name)
        if brand_filter:
            if not any(brand_filter in cat.lower() for cat in categories):
                continue

        results.append({
            "id":                p["id"],
            "name":              p["name"],
            "permalink":         p.get("permalink", ""),
            "price_usd":         p.get("price", ""),
            "categories":        categories,
            "tags":              [t["name"] for t in p.get("tags", [])],
            "has_description":   has_desc,
            "has_short_desc":    has_short,
            "current_desc":      desc,
            "current_short":     p.get("short_description", ""),
            "images":            [img["src"] for img in p.get("images", [])[:3]],
            "rating":            p.get("average_rating", "0"),
            "review_count":      p.get("rating_count", 0),
        })

    if limit:
        results = results[:limit]

    print(json.dumps(results, indent=2))
    sys.stderr.write(f"Found {len(results)} products\n")

if __name__ == "__main__":
    main()
