"""
Updates a single WooCommerce product's descriptions.
Reads a JSON payload file written by the agent.

Usage: py tools/update_product.py <payload_file>

Payload file format (JSON):
{
  "id": 1234,
  "name": "Product Name",
  "short_description": "...",
  "description": "..."
}

Exits with code 0 on success, 1 on failure.
"""
import sys
import json
import requests

sys.path.insert(0, ".")
from config import CONFIG

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: py tools/update_product.py <payload_file>\n")
        sys.exit(1)

    payload_file = sys.argv[1]
    with open(payload_file, encoding="utf-8") as f:
        payload = json.load(f)

    product_id        = payload["id"]
    product_name      = payload.get("name", f"ID {product_id}")
    short_description = payload.get("short_description", "")
    description       = payload.get("description", "")

    if not description and not short_description:
        sys.stderr.write(f"SKIP {product_name} - payload has no descriptions\n")
        sys.exit(1)

    base = CONFIG["store_url"].rstrip("/")
    auth = (CONFIG["woo_consumer_key"], CONFIG["woo_consumer_secret"])

    data = {}
    if description:
        data["description"] = description
    if short_description:
        data["short_description"] = short_description

    r = requests.put(
        f"{base}/wp-json/wc/v3/products/{product_id}",
        auth=auth,
        json=data,
        timeout=60,
    )

    if r.status_code in (200, 201):
        result = r.json()
        print(f"OK  [{product_id}] {result.get('name', product_name)}")
        sys.exit(0)
    else:
        sys.stderr.write(f"FAIL [{product_id}] {product_name} - HTTP {r.status_code}: {r.text[:200]}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
