import re
from bs4 import BeautifulSoup
from utils.helpers import log, safe_get, sl


def audit_checkout(store_url):
    log("Auditing checkout...", "RUN")
    result       = {"score": 0, "passes": [], "issues": []}
    checkout_url = f"{store_url.rstrip('/')}/checkout/"

    if store_url.startswith("https://"):
        result["score"] += 20
        result["passes"].append("SSL/HTTPS active — checkout is secure")
    else:
        result["issues"].append(("No HTTPS",
            "Contact your hosting provider to install a free Let's Encrypt SSL certificate. Without HTTPS, browsers warn buyers the site is unsafe."))

    r = safe_get(checkout_url)
    if r and r.status_code == 200:
        result["score"] += 20
        result["passes"].append("Checkout page loads successfully")
        soup   = BeautifulSoup(r.text, "html.parser")
        fields = soup.select("input:not([type='hidden']):not([type='submit']),select")
        fc     = len(fields)
        result["field_count"] = fc
        if fc <= 8:
            result["score"] += 20
            result["passes"].append(f"Streamlined checkout ({fc} fields)")
        else:
            result["issues"].append((f"{fc} checkout fields — too many for mobile",
                "Reduce to 6-8 fields max. Remove unnecessary fields via WooCommerce > Settings > Accounts. Install Fluid Checkout plugin for mobile-optimised layout."))

        guest = soup.find(string=re.compile(r"guest|no account|continue without", re.I))
        if guest:
            result["score"] += 15
            result["passes"].append("Guest checkout option available")
        else:
            result["issues"].append(("No guest checkout detected",
                "WooCommerce > Settings > Accounts & Privacy > Enable 'Allow customers to place orders without an account'. This alone can lift checkouts by 25%."))

        pay = soup.select("[class*='payment'],[class*='paystack'],img[src*='visa'],img[src*='mastercard']")
        if pay:
            result["score"] += 15
            result["passes"].append("Payment method indicators found")
        else:
            result["issues"].append(("No payment trust icons on checkout",
                "Add Paystack, Visa, Mastercard, Verve logo images above the Place Order button. Download from official brand press kits."))
    else:
        result["issues"].append(("Checkout page not accessible (503/error)",
            "URGENT: Check WooCommerce > Status > System Status. Disable plugins one-by-one to find conflicts. Test a real purchase immediately."))

    result["label"] = sl(result["score"])
    return result
