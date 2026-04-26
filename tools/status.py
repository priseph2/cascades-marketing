"""
Queries WooCommerce and reports product description and image status.

Usage: py tools/status.py
"""
import sys
import time
import requests
from collections import defaultdict

sys.path.insert(0, ".")
from config import CONFIG


def fetch_all_products():
    base = CONFIG["store_url"].rstrip("/")
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])
    all_products = []
    page = 1
    while True:
        for attempt in range(1, 4):
            try:
                r = requests.get(
                    f"{base}/wp-json/wc/v3/products",
                    auth=auth,
                    params={"per_page": 100, "status": "publish", "page": page},
                    timeout=60,
                )
                r.raise_for_status()
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(attempt * 10)
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


def classify_desc(p):
    desc = p.get("description", "").strip()
    if not desc:
        return "no_desc"
    if "<h3>" in desc:
        return "done"
    return "needs_reformat"


def has_image(p):
    return len(p.get("images", [])) > 0


def main():
    print("Fetching all products from WooCommerce...\n")
    products = fetch_all_products()

    desc_buckets = {"no_desc": 0, "needs_reformat": 0, "done": 0}
    brand_buckets = defaultdict(lambda: {"no_desc": 0, "needs_reformat": 0, "done": 0, "no_image": 0})
    no_image_count = 0

    for p in products:
        status = classify_desc(p)
        desc_buckets[status] += 1
        cats = [c["name"] for c in p.get("categories", [])]
        brand = cats[0] if cats else "Uncategorised"
        brand_buckets[brand][status] += 1
        if not has_image(p):
            no_image_count += 1
            brand_buckets[brand]["no_image"] += 1

    total = len(products)
    no_desc        = desc_buckets["no_desc"]
    needs_reformat = desc_buckets["needs_reformat"]
    done           = desc_buckets["done"]

    print("=" * 60)
    print("  SCENTIFIED — PRODUCT STATUS REPORT")
    print("=" * 60)
    print(f"  Total products      : {total}")
    print()
    print("  DESCRIPTIONS")
    print(f"    No description    : {no_desc}  ({no_desc*100//total if total else 0}%)")
    print(f"    Needs reformat    : {needs_reformat}  ({needs_reformat*100//total if total else 0}%)")
    print(f"    New format (done) : {done}  ({done*100//total if total else 0}%)")
    print(f"    Remaining work    : {no_desc + needs_reformat} products")
    print()
    print("  IMAGES")
    print(f"    Missing images    : {no_image_count}  ({no_image_count*100//total if total else 0}%)")
    print(f"    Have images       : {total - no_image_count}  ({(total - no_image_count)*100//total if total else 0}%)")
    print()
    print("=" * 60)
    print()
    print(f"  {'Brand':<30} {'No Desc':>7} {'Reformat':>9} {'Done':>6} {'No Img':>7}")
    print("-" * 60)
    for brand in sorted(brand_buckets):
        b = brand_buckets[brand]
        total_brand = b["no_desc"] + b["needs_reformat"] + b["done"]
        if total_brand == 0:
            continue
        no_img_str = str(b["no_image"]) if b["no_image"] else "-"
        print(f"  {brand:<30} {b['no_desc']:>7} {b['needs_reformat']:>9} {b['done']:>6} {no_img_str:>7}")
    print("=" * 60)
    print()
    print("  Next steps:")
    print("    /product-descriptions --reformat 20")
    print('    /product-descriptions --reformat --brand "BTV"')
    print("    /product-descriptions --no-image 20   (list products missing images)")
    print()


if __name__ == "__main__":
    main()
