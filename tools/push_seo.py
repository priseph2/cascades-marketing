"""
Pushes qa_passed: true entries from seo_staging.json to WooCommerce
by writing rank_math_title and rank_math_description via product meta_data.

Usage: py tools/push_seo.py
       py tools/push_seo.py --dry-run
"""
import sys
import json
import time
import requests

sys.path.insert(0, ".")
from config import CONFIG

STAGING_FILE = "tools/seo_staging.json"
DRY_RUN = "--dry-run" in sys.argv


def push_product(base, auth, entry):
    product_id = entry["id"]

    payload = {
        "meta_data": [
            {"key": "rank_math_title",         "value": entry["proposed_seo_title"]},
            {"key": "rank_math_description",   "value": entry["proposed_seo_desc"]},
            {"key": "rank_math_focus_keyword", "value": entry.get("focus_keyword", "")},
        ]
    }

    # Patch description if content has been updated
    if entry.get("proposed_description"):
        payload["description"] = entry["proposed_description"]

    # Update slug only if explicitly proposed and different from current
    proposed_slug = entry.get("proposed_slug", "")
    current_slug  = entry.get("current_slug", "")
    if proposed_slug and proposed_slug != current_slug:
        payload["slug"] = proposed_slug

    # Update primary image alt text
    image_ids = entry.get("image_ids", [])
    if image_ids and entry.get("image_alt_text"):
        payload["images"] = [{"id": image_ids[0], "alt": entry["image_alt_text"]}]

    r = requests.put(
        f"{base}/wp-json/wc/v3/products/{product_id}",
        auth=auth,
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main():
    with open(STAGING_FILE, "r", encoding="utf-8") as f:
        staging = json.load(f)

    base = CONFIG["store_url"].rstrip("/")
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])

    pushed = failed = skipped = 0

    for entry in staging:
        if not entry.get("qa_passed"):
            skipped += 1
            continue

        if entry.get("update_status") == "success":
            skipped += 1
            continue

        name = entry.get("name", entry["id"])

        if DRY_RUN:
            print(f"  [DRY RUN] Would push: {name}")
            print(f"    Focus Keyword : {entry.get('focus_keyword', '—')}")
            print(f"    Title         : {entry['proposed_seo_title']}")
            print(f"    Desc          : {entry['proposed_seo_desc']}")
            if entry.get("proposed_slug"):
                print(f"    Slug          : {entry.get('current_slug','?')} → {entry['proposed_slug']}")
            if entry.get("image_alt_text"):
                print(f"    Image alt     : {entry['image_alt_text']}")
            if entry.get("proposed_description"):
                print(f"    Description   : [patched — {len(entry['proposed_description'])} chars]")
            pushed += 1
            continue

        try:
            push_product(base, auth, entry)
            entry["update_status"] = "success"
            entry["update_error"]  = ""
            pushed += 1
            print(f"  Pushed: {name}")
        except Exception as e:
            entry["update_status"] = "failed"
            entry["update_error"]  = str(e)
            failed += 1
            print(f"  FAILED: {name} — {e}")

        time.sleep(0.5)

    if not DRY_RUN:
        with open(STAGING_FILE, "w", encoding="utf-8") as f:
            json.dump(staging, f, indent=2, ensure_ascii=False)

    print()
    print("=== SEO PUSH COMPLETE ===")
    print(f"Pushed  : {pushed}")
    print(f"Failed  : {failed}")
    print(f"Skipped : {skipped}  (qa_passed false or already pushed)")

    if failed:
        print()
        print("Failed products:")
        for e in staging:
            if e.get("update_status") == "failed":
                print(f"  {e['name']} — {e['update_error']}")


if __name__ == "__main__":
    main()
