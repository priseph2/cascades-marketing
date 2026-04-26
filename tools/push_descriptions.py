"""
Reads tools/descriptions_staging.json and pushes all qa_passed entries
to WooCommerce. Updates update_status in-place.

Usage: py tools/push_descriptions.py
       py tools/push_descriptions.py --dry-run
"""
import sys
import json
import time
import requests

sys.path.insert(0, ".")
from config import CONFIG


def push_product(base, auth, entry):
    product_id = entry["id"]
    data = {}
    if entry.get("description"):
        data["description"] = entry["description"]
    if entry.get("short_description"):
        data["short_description"] = entry["short_description"]

    r = requests.put(
        f"{base}/wp-json/wc/v3/products/{product_id}",
        auth=auth,
        json=data,
        timeout=60,
    )
    return r


def main():
    dry_run = "--dry-run" in sys.argv
    staging_file = "tools/descriptions_staging.json"

    with open(staging_file, encoding="utf-8") as f:
        products = json.load(f)

    base = CONFIG["store_url"].rstrip("/")
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])

    pushed = 0
    failed = 0
    skipped = 0

    for p in products:
        name = p.get("name", f"ID {p['id']}")

        if not p.get("qa_passed"):
            print(f"SKIP [{p['id']}] {name} — qa_passed is false")
            p["update_status"] = "skipped"
            skipped += 1
            continue

        if dry_run:
            print(f"DRY  [{p['id']}] {name} — would push (dry run)")
            continue

        r = push_product(base, auth, p)
        if r.status_code in (200, 201):
            result = r.json()
            print(f"OK   [{p['id']}] {result.get('name', name)}")
            p["update_status"] = "success"
            p["update_error"] = ""
            pushed += 1
        else:
            err = f"HTTP {r.status_code}: {r.text[:200]}"
            print(f"FAIL [{p['id']}] {name} — {err}", file=sys.stderr)
            p["update_status"] = "failed"
            p["update_error"] = err
            failed += 1

        time.sleep(1)

    with open(staging_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    if not dry_run:
        print(f"\nDone — Pushed: {pushed}  Failed: {failed}  Skipped: {skipped}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
