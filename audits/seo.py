from bs4 import BeautifulSoup
from config import CONFIG
from utils.helpers import log, safe_get, sl


def run_seo_audit(store_url):
    log("Running SEO audit...", "RUN")
    result = {
        "homepage_title":    "",
        "meta_description":  "",
        "h1_tags":           [],
        "h2_tags":           [],
        "keyword_presence":  {},
        "internal_links":    0,
        "image_alt_missing": 0,
        "schema_markup":     False,
        "og_tags":           False,
        "sitemap_found":     False,
        "robots_found":      False,
        "score":             0,
        "passes":            [],
        "issues":            [],
    }

    r = safe_get(store_url)
    if not r:
        result["issues"].append("Homepage not accessible for SEO audit")
        return result

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    # Title
    title = soup.title.string.strip() if soup.title else ""
    result["homepage_title"] = title
    if title and len(title) >= 30:
        result["score"] += 10
        result["passes"].append(f"Page title present ({len(title)} chars): '{title[:60]}'")
    else:
        result["issues"].append(("No or too-short page title",
            "Set title to: 'Scentified | Buy Niche & Luxury Perfumes in Nigeria | Lagos' (50-60 chars) via Yoast SEO plugin."))

    # Meta description
    meta = soup.find("meta", {"name": "description"})
    desc = meta.get("content", "").strip() if meta else ""
    result["meta_description"] = desc
    if desc and len(desc) >= 100:
        result["score"] += 10
        result["passes"].append(f"Meta description present ({len(desc)} chars)")
    else:
        result["issues"].append(("No meta description (hurts Google click-through rate)",
            "Install Yoast SEO. Set: 'Shop Africa's finest niche perfumes. Exclusive brands: Strangelove, Boadicea, Clive Christian. Fast delivery across Nigeria.' (Target: 150-160 chars)"))

    # H1 tags
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    result["h1_tags"] = h1s[:5]
    if len(h1s) == 1:
        result["score"] += 10
        result["passes"].append(f"Single H1 tag present: '{h1s[0][:50]}'")
    elif len(h1s) == 0:
        result["issues"].append(("No H1 tag on homepage",
            "Add a single H1 tag to your homepage hero section. E.g. '<h1>Africa's Home of Niche Perfumery</h1>'. Critical for Google to understand the page topic."))
    else:
        result["issues"].append((f"Multiple H1 tags ({len(h1s)}) — confuses search engines",
            "Keep exactly one H1 per page. Demote extra H1s to H2. Edit in Elementor or your page builder."))

    # H2 tags
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
    result["h2_tags"] = h2s[:8]
    if h2s:
        result["score"] += 5
        result["passes"].append(f"{len(h2s)} H2 tags found — good content structure")

    # Keyword presence
    for kw in CONFIG["target_keywords"]:
        result["keyword_presence"][kw] = kw.lower() in text
        if kw.lower() in text:
            result["score"] += 3

    # Image alt text
    imgs        = soup.find_all("img")
    missing_alt = sum(1 for img in imgs if not img.get("alt", "").strip())
    result["image_alt_missing"] = missing_alt
    if missing_alt == 0:
        result["score"] += 10
        result["passes"].append("All images have alt text — good for SEO and accessibility")
    elif missing_alt <= 5:
        result["issues"].append((f"{missing_alt} images missing alt text",
            f"Add descriptive alt text to all product images. E.g. alt='Strangelove A Fire Within EDP 100ml perfume bottle'. Affects both SEO and accessibility score."))
    else:
        result["issues"].append((f"{missing_alt} images missing alt text — significant SEO gap",
            "Use 'SEO Friendly Images' WordPress plugin to auto-generate alt text from filenames. Then manually refine product images with keyword-rich descriptions."))

    # Internal links
    internal = [a for a in soup.find_all("a", href=True)
                if store_url.split("//")[-1].split("/")[0] in a["href"] or a["href"].startswith("/")]
    result["internal_links"] = len(internal)
    if len(internal) >= 10:
        result["score"] += 5
        result["passes"].append(f"Good internal linking ({len(internal)} internal links)")

    # Schema markup
    schema = soup.find("script", {"type": "application/ld+json"})
    result["schema_markup"] = bool(schema)
    if schema:
        result["score"] += 10
        result["passes"].append("Schema/structured data markup found — helps Google rich results")
    else:
        result["issues"].append(("No schema markup (JSON-LD) — missing rich results in Google",
            "WooCommerce + Yoast SEO automatically generates Product schema. Install both. Also add Organization schema to homepage manually or via Schema Pro plugin."))

    # Open Graph tags
    og = soup.find("meta", {"property": "og:title"})
    result["og_tags"] = bool(og)
    if og:
        result["score"] += 5
        result["passes"].append("Open Graph tags present — pages share correctly on social media")
    else:
        result["issues"].append(("No Open Graph tags — links shared on Instagram/WhatsApp won't show preview image",
            "Yoast SEO automatically adds OG tags when configured. Go to Yoast > Social > Facebook and enable Open Graph metadata."))

    # Sitemap
    sitemap_r = safe_get(f"{store_url.rstrip('/')}/sitemap.xml", timeout=5)
    if sitemap_r and sitemap_r.status_code == 200:
        result["sitemap_found"] = True
        result["score"] += 10
        result["passes"].append("XML sitemap found — helps Google discover all pages")
    else:
        result["issues"].append(("No XML sitemap found at /sitemap.xml",
            "Yoast SEO auto-generates a sitemap. After installing, submit it in Google Search Console at search.google.com/search-console. This accelerates Google indexing of all product pages."))

    # Robots.txt
    robots_r = safe_get(f"{store_url.rstrip('/')}/robots.txt", timeout=5)
    if robots_r and robots_r.status_code == 200:
        result["robots_found"] = True
        result["score"] += 5
        result["passes"].append("robots.txt found — search engine crawling is configured")
    else:
        result["issues"].append(("No robots.txt file",
            "WordPress auto-generates this but it may be blocked. Check via WordPress Admin > Settings > Reading — ensure 'Discourage search engines' is UNCHECKED."))

    result["score"] = min(result["score"], 100)
    log(f"  SEO Score: {result['score']} ({sl(result['score'])})", "OK")
    return result
