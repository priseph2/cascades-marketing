from bs4 import BeautifulSoup
from utils.helpers import log, safe_get, sl


def audit_store_ux(store_url):
    log("Auditing store UX...", "RUN")
    result = {"score": 0, "passes": [], "issues": [], "seo": {}}
    r = safe_get(store_url)
    if not r:
        return result
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    if soup.find("meta", {"name": "viewport"}):
        result["score"] += 15
        result["passes"].append("Mobile viewport meta tag present")
    else:
        result["issues"].append(("No mobile viewport tag",
            "Add <meta name='viewport' content='width=device-width, initial-scale=1'> to your theme's header.php or via a header plugin."))

    nav_links = soup.select("nav a,.menu a,header a")
    if 4 <= len(nav_links) <= 12:
        result["score"] += 10
        result["passes"].append(f"Clean navigation ({len(nav_links)} links)")
    elif len(nav_links) > 12:
        result["issues"].append((f"Navigation too cluttered ({len(nav_links)} links)",
            "Reduce to 5-7 primary nav items. Move secondary links to footer."))

    if soup.select_one("input[type='search'],input[name='s'],.search-form"):
        result["score"] += 10
        result["passes"].append("Search bar present")
    else:
        result["issues"].append(("No search bar",
            "Add WooCommerce Product Search widget to header. Buyers looking for specific brands need this."))

    trust_kw = ["authentic", "genuine", "100%", "guarantee", "trusted", "official", "exclusive"]
    found = [kw for kw in trust_kw if kw in text]
    if found:
        result["score"] += 10
        result["passes"].append(f"Trust language: {', '.join(found[:3])}")
    else:
        result["issues"].append(("No trust signals on homepage",
            "Add a trust bar: 'Authentic Products | Sourced Directly | Secure Payment | Nationwide Delivery'. Place below hero."))

    socials = soup.select("a[href*='instagram'],a[href*='facebook'],a[href*='tiktok']")
    if socials:
        result["score"] += 10
        result["passes"].append(f"{len(socials)} social media links found")
    else:
        result["issues"].append(("No social media links",
            "Add Instagram, Facebook, TikTok links to header and footer. Go to Appearance > Customize > Social Links."))

    wa = soup.select_one("a[href*='wa.me'],a[href*='whatsapp'],a[href*='tel:']")
    if wa:
        result["score"] += 10
        result["passes"].append("WhatsApp/contact link present")
    else:
        result["issues"].append(("No WhatsApp contact link",
            "Install WP Social Chat. Add floating WhatsApp button with +234 902 084 2708. Nigerian luxury buyers expect direct contact at ₦200k+ price points."))

    meta = soup.find("meta", {"name": "description"})
    if meta:
        result["score"] += 10
        result["passes"].append("Meta description present")
    else:
        result["issues"].append(("No meta description",
            "Install Yoast SEO. Set homepage description to 150-160 chars including 'Nigeria', 'luxury perfume', and your top brand names."))

    title = soup.title.string.strip() if soup.title else ""
    result["seo"] = {
        "title":               title,
        "has_meta_description": bool(meta),
        "meta_description":    meta.get("content", "") if meta else "",
    }

    if soup.select_one("footer,.footer,#footer"):
        result["score"] += 5
        result["passes"].append("Footer present")

    result["label"] = sl(result["score"])
    return result
