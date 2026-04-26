import time
import requests
from bs4 import BeautifulSoup
from utils.helpers import log, safe_get, sl


PERFUME_KEYWORDS = {
    "fragrance_notes": ["top note", "heart note", "base note", "accord", "notes of", "scent profile", "opening", "dry down"],
    "longevity":       ["longevity", "long-lasting", "hours", "projection", "sillage", "stays", "lasts"],
    "mood":            ["mood", "feel", "emotion", "confidence", "sensual", "fresh", "warm", "woody", "floral", "oriental"],
}


def score_product_page(url, soup, title=""):
    score, issues, passes = 0, [], []
    text = soup.get_text(" ", strip=True).lower()

    images    = soup.select("img.wp-post-image,.woocommerce-product-gallery img,.product-image img,img[class*='product']")
    img_count = len(images)
    if img_count >= 3:
        score += 20
        passes.append(f"Good image count ({img_count} images)")
    elif img_count >= 1:
        score += 10
        issues.append((f"Only {img_count} image(s) — luxury perfume needs 3+ angles",
            "Shoot and upload minimum 5 product angles. Request press kit images from brand distributor."))
    else:
        issues.append(("No product images detected",
            "Upload at least 5 high-quality product images immediately."))

    notes_found = [kw for kw in PERFUME_KEYWORDS["fragrance_notes"] if kw in text]
    if notes_found:
        score += 20
        passes.append("Fragrance notes present")
    else:
        issues.append(("No fragrance notes found",
            "Add structured Top/Heart/Base note pyramid above the fold. Source from brand's product sheet or Fragrantica.com."))

    if any(kw in text for kw in PERFUME_KEYWORDS["longevity"]):
        score += 15
        passes.append("Longevity/projection info present")
    else:
        issues.append(("No longevity or projection info",
            "Add: Longevity: X hrs | Projection: Moderate/Strong | Concentration: EDP/EDP. Source from Fragrantica or brand sheet."))

    review_els = soup.select(".woocommerce-Reviews,#reviews,.comment,[class*='review'],[class*='rating'],.star-rating")
    if review_els:
        score += 20
        passes.append("Reviews section present")
    else:
        issues.append(("No reviews found",
            "Enable WooCommerce reviews. Email past buyers. Use Judge.me plugin (free). Even 3 reviews lift conversion by 18%."))

    price = soup.select_one(".price,.woocommerce-Price-amount,[class*='price']")
    if price:
        score += 10
        passes.append(f"Price displayed: {price.get_text(strip=True)[:20]}")
    else:
        issues.append(("Price not visible",
            "Ensure price is shown clearly above the Add to Cart button."))

    atc = soup.select_one("button.single_add_to_cart_button,[name='add-to-cart'],.add_to_cart_button")
    if atc:
        score += 10
        passes.append("Add to Cart button present")
    else:
        issues.append(("Add to Cart button not detected",
            "Check WooCommerce product settings — ensure product status is Published and stock is managed."))

    if any(kw in text for kw in PERFUME_KEYWORDS["mood"]):
        score += 5
        passes.append("Mood/emotion language present")
    else:
        issues.append(("No mood/storytelling copy",
            "Add 1-2 sentence mood description: 'For the confident, who command every room they enter.' Perfume is emotional — copy must reflect that."))

    return {"url": url, "title": title, "score": score, "label": sl(score), "passes": passes, "issues": issues}


def audit_product_pages(store_url, woo_key, woo_secret):
    log("Auditing product pages...", "RUN")
    results = []
    if woo_key:
        api_url = f"{store_url.rstrip('/')}/wp-json/wc/v3/products"
        try:
            r        = requests.get(api_url, auth=(woo_key, woo_secret), params={"per_page": 8}, timeout=15)
            products = r.json()
            for p in products[:5]:
                prod_url = p.get("permalink", "")
                if not prod_url:
                    continue
                pr = safe_get(prod_url)
                if not pr:
                    continue
                soup   = BeautifulSoup(pr.text, "html.parser")
                result = score_product_page(prod_url, soup, p.get("name", ""))
                results.append(result)
                time.sleep(1)
            return results
        except Exception as e:
            log(f"API product fetch failed: {e} — falling back to scrape", "WARN")

    r = safe_get(store_url)
    if not r:
        return results
    soup  = BeautifulSoup(r.text, "html.parser")
    links = list(set([a["href"] for a in soup.select("a[href*='/product/']") if a.get("href")]))[:5]
    for link in links:
        pr = safe_get(link)
        if not pr:
            continue
        psoup  = BeautifulSoup(pr.text, "html.parser")
        title  = psoup.title.string if psoup.title else link
        result = score_product_page(link, psoup, title)
        results.append(result)
        time.sleep(1)
    return results
