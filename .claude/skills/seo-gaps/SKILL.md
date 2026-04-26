# SEO Gaps

Research and generate fully optimised RankMath on-page SEO for WooCommerce products —
focus keyword, SEO title, meta description, slug, content patch, and image alt text —
then push everything live via the WooCommerce REST API.

**SEO data is NOT pushed automatically.**
An Excel report is produced for human review first. Run `--push` to go live.

---

## Arguments

- No args / a number      → optimise N products with no SEO title set (default: 10)
- `--all`                 → optimise every product regardless of current SEO status
- `--brand "Name"`        → optimise all products for one brand (e.g. "BTV")
- `--ids 123,456,789`     → optimise specific products by ID (comma-separated, no spaces); useful for re-running SEO on products that already have titles set
- `--push`                → push all `qa_passed: true` entries in the staging file live
- `--dry-run`             → preview what would be pushed without actually pushing

---

## If `--push` or `--dry-run` was passed

Run this command and display the output, then stop:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/push_seo.py
```

For `--dry-run`:
```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/push_seo.py --dry-run
```

Display the push summary, then stop.

---

## Step 1 — Initialise

Clear `tools/seo_staging.json` to `[]`.

---

## Step 2 — Fetch products

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_seo_data.py --no-seo --limit $N
```

- Default (no args): `--no-seo --limit 10` — products with no RankMath title yet
- If `--all`: omit `--no-seo`, omit `--limit`
- If `--brand "Name"`: add `--brand "Name"`
- If a number was given: `--no-seo --limit $N`
- If `--ids 123,456`: `py tools/fetch_seo_data.py --ids 123,456` — omit `--no-seo` and `--limit` (IDs override both; fetches those products regardless of whether they already have a title set)

---

## Step 3 — For each product: research → generate → verify → stage

Work one product at a time.

---

### 3a. Select the Focus Keyword

The focus keyword is 2–4 words. It must be something a Nigerian buyer would type into Google.

**Formula:** `[Brand short name] [Product short name] [EDP/EDT/Parfum]`

**Rules:**
- Use the brand's common name (e.g. "AAA" not "Asghar Adam Ali", "Essential Parfums" not "EP")
- Shorten long product names (e.g. "Velvet Iris" not "VELVET IRIS EDP 100ML")
- Include concentration only if it fits within 4 words total
- The focus keyword must be able to appear naturally in a sentence

**Examples:**
```
AAA Ranya EDP
Essential Parfums Rose Magnetic
Fragrance du Bois Santal Complet
BTV Oud Intense
Clive Christian No 1 EDP
```

---

### 3b. Research SERP landscape

`WebSearch`: `"[brand] [product name]" perfume buy Nigeria`

From the search snippet results, note:
- How many results are from scentifiedperfume.com (if any)
- What titles and meta descriptions the top-ranking pages use
- What keywords appear repeatedly in top results
- Any structured data signals (price, rating) visible in snippets
- Official brand website URL (needed for external link in Step 3f)

Record these as `serp_notes` in the staging entry.

---

### 3c. Generate SEO Title — Focus Keyword Near the Beginning

**Formula:** `[Focus Keyword] | Buy in Nigeria — Scentified`
or if the keyword fits with EDP/size: `[Brand] [Product] EDP | Buy in Nigeria — Scentified`

**Rules:**
- 50–60 characters total (count exactly)
- Focus keyword MUST appear within the first 30 characters
- Brand name first — Google weights the beginning of the title most heavily
- Include "Nigeria" — this is the primary buying intent signal
- End with "— Scentified" or "| Scentified" to build brand recognition
- Never truncate mid-word — shorten the product name if needed

**Examples:**
```
AAA Ranya EDP | Buy in Nigeria — Scentified            (43 chars) ✓
Essential Parfums Rose Magnetic | Nigeria — Scentified  (54 chars) ✓
Fragrance du Bois Santal Complet | Nigeria — Scentified (55 chars) ✓
```

---

### 3d. Generate Meta Description — Focus Keyword Included

**Formula:** `[Key notes hook]. [Performance signal]. [Focus keyword + Brand authenticity]. [CTA + Nigeria/Lagos]`

**Rules:**
- 140–155 characters total (count exactly)
- Open with the 2–3 most evocative notes — this is the hook
- The exact focus keyword must appear verbatim at least once
- Include a performance signal (long-lasting, strong projection, etc.)
- Include "Nigeria", "Lagos", or "West Africa" — buying intent signal. Vary across products.
- End with a CTA: "Shop now", "Order today", "Buy at Scentified"
- No generic copy ("perfect for everyone", "unique fragrance")

**Example:**
```
Cherry, Saffron and Tuberose in a 7–9 hour Floral EDP. Authentic AAA Ranya EDP,
buy in Nigeria and get delivered fast — Scentified.                               (151 chars) ✓
```

---

### 3e. Slug Optimisation

Check the current product `slug` (e.g. `aaa-ranya-100ml-spray-perfume`).

**Propose a new slug if:**
- The current slug is longer than 50 characters, OR
- The current slug does not contain the brand and product name

**Formula:** `[brand-slug]-[product-slug]-[concentration]`
- All lowercase, hyphens only, no stopwords ("the", "and", "of", "in")
- Maximum 50 characters
- Must contain the focus keyword words

**Examples:**
```
Current: aaa-ranya-100ml-spray-perfume  (30 chars) → keep if already contains keyword
Current: essential-parfum-velvet-iris-edp-100ml  (38 chars) → propose: essential-parfums-velvet-iris-edp
```

⚠️ **Important:** Slug changes can break existing backlinks and Google-indexed URLs.
Only propose a new slug if the current one is clearly suboptimal. Record `proposed_slug` in the staging entry only when proposing a change. If slug is fine, leave `proposed_slug` empty.

---

### 3f. Content Patch — Embed Focus Keyword and Add Links

The product description already follows the SEO template. This step patches it to satisfy the remaining RankMath on-page checks.

**6a — Focus keyword in first paragraph**
Read the opening `<p>` of `description`. Check if the focus keyword (or its component words) appear in the first sentence.

- If yes: no change needed for this paragraph.
- If no: rewrite the first sentence to naturally include the focus keyword. Keep the tone intact.
  - Before: `"With a name that evokes admiration, Ranya by Asghar Adam Ali is an ode to beauty..."`
  - After: `"AAA Ranya EDP — a fragrance that evokes admiration — is Asghar Adam Ali's ode to beauty..."`

**6b — Focus keyword in a subheading**
Scan all `<h3>` tags. If none contains the focus keyword words, update the "Best For" heading:

```html
<h3>Best For — AAA Ranya EDP</h3>
```

Only do this if it reads naturally. If it looks forced, skip it and note `keyword_in_h3: false`.

**6c — Keyword density (~1%)**
Count total words in the description (strip HTML). Count occurrences of the full focus keyword.
Target: approximately 1 occurrence per 100 words.
- Description ~350 words → aim for 3–4 keyword occurrences
- If below 0.5%: add 1–2 more natural mentions in the body
- If above 2%: it is keyword stuffing — remove some

**6d — Internal link**
In the closing tagline `<em>` paragraph, wrap the collection anchor text with an internal link:

```html
<p><em>Authentic [Brand] fragrances, sourced directly and delivered across West Africa.
Shop the full <a href="https://scentifiedperfume.com/product-category/[brand-slug]/">[Brand] collection</a> at Scentified.</em></p>
```

Use the brand's category slug (lowercase, hyphenated). If unsure of the exact category URL, use: `https://scentifiedperfume.com/?s=[brand+name]`

**6e — External DoFollow link**
In the About [Brand] `<h3>` section, add one external link to the brand's official website.
Use the brand site URL found in Step 3b SERP research.

```html
<h3>About [Brand Name]</h3>
<p>[existing brand copy...] <a href="[brand-official-url]" target="_blank" rel="noopener noreferrer">Visit [Brand]'s official website</a>.</p>
```

If no official brand URL was found in research, skip this and note it in `qa_notes`.

Store the full patched HTML as `proposed_description` in the staging entry.

---

### 3g. Image Alt Text

**Formula:** `[Focus Keyword] perfume Nigeria`

Example: `"AAA Ranya EDP perfume Nigeria"`

This will be set on the product's primary image via the WooCommerce API on push.
Store as `image_alt_text` in the staging entry.

---

### 3h. Verify — Full RankMath QA Checklist

Run all checks before staging. Rewrite and re-check on failure.

**Focus Keyword**
- [ ] Focus keyword is 2–4 words and appears natural in a sentence
- [ ] Focus keyword is set in the staging entry

**SEO Title**
- [ ] SEO title is 50–60 characters (count exactly)
- [ ] Focus keyword appears within the first 30 characters of the title
- [ ] SEO title contains "Nigeria" or "Scentified"
- [ ] SEO title contains the brand name

**Meta Description**
- [ ] Meta description is 140–155 characters (count exactly)
- [ ] Focus keyword appears verbatim in the meta description
- [ ] Meta description contains "Nigeria", "Lagos", or "West Africa"
- [ ] Meta description contains a CTA ("Shop", "Buy", "Order")
- [ ] Meta description contains at least one specific fragrance note

**Content**
- [ ] Focus keyword appears in the first sentence of the opening `<p>`
- [ ] Focus keyword appears in at least one `<h3>` (or `keyword_in_h3: false` noted if forced)
- [ ] Keyword density is between 0.5% and 2% (count words and occurrences)
- [ ] At least one internal link is present in `proposed_description`
- [ ] At least one external DoFollow link is present in `proposed_description`

**Slug**
- [ ] `proposed_slug` is ≤50 characters (if proposing a change)
- [ ] `proposed_slug` contains the brand and product name words

**Image**
- [ ] `image_alt_text` is set and contains the focus keyword

**General**
- [ ] No sentence starts with "Introducing" or "Experience"
- [ ] No generic copy ("suitable for all occasions", "a fragrance for everyone")

After passing all checks, set `"qa_passed": true`.
If still failing after 2 rewrites, set `"qa_passed": false` and record `qa_notes`.

---

### 3i. Stage

Read `tools/seo_staging.json`, append this entry, write it back:

```json
{
  "id": <product_id>,
  "name": "<product name>",
  "permalink": "<url>",
  "price": "<price>",
  "categories": ["<brand>"],
  "focus_keyword": "<2–4 word focus keyword>",
  "current_seo_title": "<existing rank_math_title or empty>",
  "current_seo_desc": "<existing rank_math_description or empty>",
  "current_slug": "<current product slug>",
  "proposed_seo_title": "<new title>",
  "proposed_seo_desc": "<new meta description>",
  "proposed_slug": "<new slug, or empty string if no change>",
  "proposed_description": "<full patched HTML description>",
  "image_ids": [<image_id_integer>],
  "image_alt_text": "<focus keyword> perfume Nigeria",
  "research": {
    "primary_keyword": "<focus keyword>",
    "brand_site_url": "<official brand URL or empty>",
    "sources_used": ["<url1>", "<url2>"],
    "serp_notes": "<what top results look like>",
    "keyword_density": "<X.X%>",
    "keyword_in_h3": true
  },
  "qa_passed": true,
  "qa_notes": "",
  "update_status": "draft",
  "update_error": ""
}
```

---

## Step 4 — Export Excel

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/export_seo_excel.py
```

Capture and display the output path.

---

## Step 5 — Final summary

```
=== SEO GAPS DRAFT COMPLETE ===

Processed  : X products
QA Passed  : X
QA Failed  : X

Excel report: audit_reports/seo_gaps_<timestamp>.xlsx
  Sheet 1: Summary       — focus keyword, slug, image alt, QA result per product
  Sheet 2: Side by Side  — current vs. proposed titles, descriptions, content patch flag
  Sheet 3: Research Data — keywords, SERP notes, sources, keyword density per product

Next step: review the Excel, then run:
  /seo-gaps --push
```

---

## Important rules

- Never exceed 60 characters for a title — Google truncates at 60
- Never exceed 155 characters for a meta description — Google truncates at 155
- Focus keyword MUST be in the first 30 characters of the title
- Focus keyword MUST appear verbatim in the meta description
- Focus keyword MUST appear in the first sentence of the product description
- Geographic signal: use "Nigeria", "Lagos", or "West Africa" — never "across Africa" or "across the continent" (store operates in Nigeria, Ghana, and two other West African countries)
- External links must be DoFollow (no `rel="nofollow"`) — use `rel="noopener noreferrer"` only
- Never invent notes or facts not found in the product description or research
- Always count characters exactly before staging — estimates are not enough
- Slug changes can break indexed URLs — only propose when clearly necessary
