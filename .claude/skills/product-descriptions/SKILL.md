# Product Description Writer

Research each WooCommerce product that is missing a description, write SEO-optimised
short and long descriptions, verify them against a strict quality checklist, then export
a full Excel report to `audit_reports/` for human review.

**Descriptions are NOT pushed to WooCommerce automatically.**
The Excel report is the deliverable. A human reviews and approves before going live.

## Arguments

- No args / a number         → research & write descriptions for products that have NONE (default: 5)
- `--all`                    → research & write for every product including ones that already have descriptions
- `--reformat N`             → reformat N products in the OLD format into the new SEO template (default: 10)
- `--reformat --all`         → reformat every product still in the old format
- `--reformat --brand "Name"` → reformat all old-format products for one brand (e.g. "BTV", "Clive Christian")
- `--push`                   → push all `qa_passed: true` entries in the staging file to WooCommerce (skips research)
- `--status`                 → show a live count of products by status and image coverage (no desc / needs reformat / done / no image)
- `--no-image [N]`           → list products that have no images; optional limit N; combinable with `--brand "Name"`

---

## If `--reformat` was passed — Reformat existing descriptions into the SEO template

Products already have descriptions. The goal is NOT to rewrite the copy from scratch —
it is to restructure it into the standard SEO template while preserving the existing
narrative and notes. Research is lighter: only Performance and About Brand need looking up.

### Reformat Step 1 — Initialise

Clear `tools/descriptions_staging.json` to `[]`.

### Reformat Step 2 — Fetch products that need reformatting

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --needs-reformat --limit $N
```

If no number was given after `--reformat`, default to `--limit 10`.
If `--reformat --all` was passed, omit `--limit`.
If `--reformat --brand "Name"` was passed, add `--brand "Name"` and omit `--limit`:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --needs-reformat --brand "Name"
```

The `--needs-reformat` flag automatically excludes products already in the new SEO format
(detected by the presence of `<h3>` tags). No manual skip list is needed.

### Reformat Step 3 — Brand cache

Before processing individual products, build a brand cache: identify every unique brand
in the batch (from `categories`). For each brand not yet researched in this session:

`WebSearch`: `"[brand name]" perfume house founded heritage official site`
`WebFetch` the top brand result. Extract: founding year, founder, brand philosophy,
country of origin, positioning (niche/luxury/mainstream).

Store these brand summaries — they are reused for every product of that brand in
the batch, avoiding duplicate searches.

### Reformat Step 4 — For each product: extract → research performance → rewrite → verify → stage

Work one product at a time.

#### 4a. Extract from existing description

Parse `current_desc` and `current_short` to extract:
- **Opening narrative** — the first `<p>` in the long description (keep as-is or lightly refine)
- **Top Notes** — from `current_short` (look for "Top Notes:" line) or from prose in `current_desc`
- **Heart/Middle Notes** — same
- **Base Notes** — same
- **Fragrance family** — from `current_short` ("Olfactive Family:") or prose
- **Concentration** — from product name (EDP, EDT, Parfum, etc.)
- **Bottle size** — from product name (e.g. 100ml, 50ml)
- **Bottle/packaging description** — any packaging paragraph in the existing long desc

If notes are NOT present in the existing copy, fall back to Fragrantica (WebSearch snippet).

#### 4b. Research Performance only

`WebSearch`: `"[product name]" site:fragrantica.com longevity sillage`

Extract: longevity rating and sillage/projection rating from the search snippet.
If not on Fragrantica, use concentration-based estimates:
- Parfum / Extrait: 10–14 hours, Strong projection
- EDP: 6–10 hours, Moderate–Strong projection
- EDT: 4–7 hours, Moderate projection
- EDC: 2–4 hours, Light projection

#### 4c. Rewrite into the SEO template

Assemble the new description using the extracted/researched data:

**Short Description** (plain text, 60–100 words)
- Rewrite from scratch using the notes and key facts
- Must name: brand, key notes, concentration, bottle size
- Must include a geographic delivery signal — vary naturally across: "Nigeria", "Lagos", "West Africa", "across West Africa". Do NOT use the same phrase in every product. Do NOT use "across Africa" or "across the continent" — the store operates in Nigeria, Ghana, and two other West African countries, not the whole continent.
- No HTML tags

**Long Description** (HTML, 280–400 words)

For fragrances:
```html
<p>[Keep or lightly refine the existing opening paragraph. Must name the product.]</p>

<h3>Fragrance Notes</h3>
<p><strong>Top Notes:</strong> [from extracted notes]<br>
<strong>Heart Notes:</strong> [from extracted notes]<br>
<strong>Base Notes:</strong> [from extracted notes]</p>

<h3>Performance</h3>
<p><strong>Longevity:</strong> [X–Y hours]<br>
<strong>Projection:</strong> [Intimate / Moderate / Strong]<br>
<strong>Concentration:</strong> [EDP / EDT / Parfum / etc.]</p>

<h3>Best For</h3>
<p>[2 sentences: specific occasions, seasons, time of day. May reference Lagos, Nigeria, or African context — but not required in every product.]</p>

<h3>About [Brand Name]</h3>
<p>[2–3 sentences from the brand cache. Factually accurate only.]</p>

<p><em>Authentic [Brand] fragrances, sourced directly and delivered across West Africa. Shop the full [Brand] collection at Scentified.</em></p>
```

For skincare/body care products: use the Key Ingredients / How To Use template
(see non-fragrance template in the Write descriptions section below).

If the existing long description has a packaging/bottle paragraph, you MAY include it
as an additional `<p>` before the `<h3>Fragrance Notes</h3>` heading — it adds value.

#### 4d. Verify — same 13-point QA checklist as the full research flow

Run all checks in Section 3c. Rewrite and re-check on failure.

#### 4e. Stage

Same JSON format as Section 3d. Set `"update_status": "draft"`.

---

## If `--no-image` was passed — List products missing images

Run this command and display the output as a table (id, name, brand, price), then stop.

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --no-image
```

If a number was passed (e.g. `--no-image 20`), append `--limit 20`.
If `--brand "Name"` was also passed, append `--brand "Name"`.

Display results as:
```
=== PRODUCTS MISSING IMAGES ===

Found X products with no images:

  ID     Name                                    Brand         Price
  ----   -------------------------------------   -----------   --------
  1234   Product Name                            BTV           ₦185,000
  ...

To fix: upload images via WooCommerce > Products, or source images from the brand's official site.
```

---

## If `--status` was passed — Show live description status

Run this command and display the output, then stop. Do not run any other steps.

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/status.py
```

---

## If `--push` was passed — Push staged descriptions live

Run this command and display the output, then stop. Do not run Steps 1–5.

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/push_descriptions.py
```

After it completes, display:

```
=== PUSH COMPLETE ===

Pushed  : X products
Failed  : X  (update_error column in staging JSON for details)
Skipped : X  (qa_passed was false)
```

If any product failed, show its name and error message, and suggest the user re-run
`/product-descriptions --push` after fixing the issue.

---

## Step 1 — Initialise the staging file

Before processing any products, create (or overwrite) `tools/descriptions_staging.json`
as an empty JSON array `[]`.

---

## Step 2 — Fetch the product list

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --limit $ARGUMENTS
```

If no argument was provided, default to `--limit 5`.
Parse the JSON output into a working list.

---

## Step 3 — For each product: research → write → verify → stage

Work through one product at a time. Do not move to the next until the current one
passes verification (Step 3c).

### 3a. Research

Gather source material from ALL of these — do not skip any (6 sources total):

**Source 1 — Product page**
`WebFetch` the `permalink`. Extract: any copy already on the page, listed notes,
brand claims, bottle/size info, concentration.

**Source 2 — Fragrantica**
`WebSearch`: `"[exact product name]" site:fragrantica.com`
`WebFetch` the top result. Extract:
- Top / Heart / Base notes (exact ingredient names, e.g. "Bergamot, Lemon, Pink Pepper")
- Fragrance family (Floral, Oriental, Woody, etc.)
- Longevity rating (Poor / Moderate / Long Lasting / Eternal)
- Sillage rating (Intimate / Moderate / Strong / Enormous)
- Launch year
- Perfumer name (if listed)

If the exact product name returns no results, try: `"[brand name]" "[shortened product name]" fragrantica`

**Source 3 — Brand official site**
`WebSearch`: `"[brand name]" "[product name]" official site fragrance`
`WebFetch` the top brand result (not a retailer). Extract: brand storytelling,
inspiration behind the fragrance, mood language, occasion copy, any official note listing.

**Source 4 — Wikiparfum**
`WebSearch`: `"[product name]" site:wikiparfum.com`
`WebFetch` the top result. Extract: notes, concentration, launch year, brand description,
any additional storytelling copy not found in previous sources.

**Source 5 — Basenotes**
`WebSearch`: `"[product name]" site:basenotes.com`
`WebFetch` the top result. Extract: notes, fragrance family, community longevity/projection
ratings, any additional context not yet found.

**Source 6 — Secondary retailer (if notes still missing after all above)**
`WebSearch`: `"[product name]" "[brand name]" EDP fragrance notes`
`WebFetch` one reputable retailer result (e.g. Harrods, Selfridges, Twisted Lily,
Luckyscent, Osme). Extract any note or description data not yet found.

Record every URL fetched as `sources_used`, even ones that returned no useful data.

---

### 3b. Write descriptions

Use ONLY notes and facts found in Step 3a. Never invent or assume.

**Short Description** (plain text, 60–100 words)
- 2–3 complete sentences
- Must name: the brand, key fragrance notes, concentration (EDP/EDT/Parfum), bottle size if known
- Must include a geographic delivery signal, varied naturally — "Nigeria", "Lagos", "West Africa", "across West Africa". Do not repeat the same phrase across products. Do NOT use "across Africa" or "across the continent".
- Tone: confident, sensory, aspirational — written for someone spending ₦150,000–₦2,000,000
- No bullet points, no HTML

**Long Description** (HTML, 280–400 words)
Use this exact structure — do not change the heading tags or order:

```html
<p>[Opening — 2–3 sentences on the mood, emotion and story of this fragrance. Make it vivid and specific to THIS product, not generic luxury copy.]</p>

<h3>Fragrance Notes</h3>
<p><strong>Top Notes:</strong> [exact notes from research, comma-separated]<br>
<strong>Heart Notes:</strong> [exact notes from research, comma-separated]<br>
<strong>Base Notes:</strong> [exact notes from research, comma-separated]</p>

<h3>Performance</h3>
<p><strong>Longevity:</strong> [X–Y hours based on longevity rating]<br>
<strong>Projection:</strong> [Intimate / Moderate / Strong based on sillage rating]<br>
<strong>Concentration:</strong> [EDP / EDT / Parfum / Extrait / etc.]</p>

<h3>Best For</h3>
<p>[2 sentences: specific occasions, seasons, time of day, personality type this fragrance suits. Be concrete — "evening events and black-tie occasions in Lagos" beats "everyday wear".]</p>

<h3>About [Brand Name]</h3>
<p>[2–3 sentences on the brand's heritage, founding story, or positioning. Must be factually accurate — sourced from the brand site or Fragrantica. Do not paraphrase vaguely.]</p>

<p><em>Authentic [Brand] fragrances, sourced directly and delivered across West Africa. Shop the full [Brand] collection at Scentified.</em></p>
```

If any notes section is genuinely not found after all 4 sources: write
`<strong>Top Notes:</strong> To be confirmed` — never guess.

**For non-fragrance products (skincare, body care, hair care):**
Adapt the HTML structure — keep the same heading tags and order, but replace the
fragrance-specific sections with product-appropriate equivalents:

```html
<p>[Opening — specific to THIS product: the problem it solves, the key ingredient, the sensory experience.]</p>

<h3>Key Ingredients</h3>
<p><strong>[Ingredient 1]:</strong> [what it does]<br>
<strong>[Ingredient 2]:</strong> [what it does]<br>
...</p>

<h3>How To Use</h3>
<p><strong>Frequency:</strong> [daily / weekly / etc.]<br>
<strong>Volume:</strong> [size]<br>
<strong>Method:</strong> [brief usage instruction from product page]</p>

<h3>Best For</h3>
<p>[Specific skin type, concern, climate, occasion. Geographic reference optional — use Lagos, Nigeria, Africa, or none depending on what feels natural.]</p>

<h3>About [Brand Name]</h3>
<p>[Brand heritage, sourced from brand site. Factually accurate only.]</p>

<p><em>Authentic [Brand] skincare, sourced directly and delivered across West Africa. Shop the full [Brand] collection at Scentified.</em></p>
```

---

### 3c. Verify — MANDATORY before staging

After writing both descriptions, run this checklist. Do NOT proceed to staging if any
item fails — rewrite and re-check.

**Relevance checks (does the copy match this specific product?)**
- [ ] The short description names THIS product's actual fragrance notes (not generic "floral" without specifics)
- [ ] The long description opening paragraph is specific to THIS fragrance — it does not read as generic luxury copy that could apply to any perfume
- [ ] The `<h3>About [Brand]</h3>` section describes the CORRECT brand for this product
- [ ] The concentration (EDP/EDT/Parfum) in the Performance section matches what the product name or research says
- [ ] The bottle size mentioned (if any) matches the product listing

**Accuracy checks (are facts grounded in research?)**
- [ ] Every note listed in Top / Heart / Base was found in at least one source in `sources_used`
- [ ] Longevity and Projection values are consistent with the Fragrantica ratings found (e.g. "Long Lasting" → 8–12 hours)
- [ ] No claim about the brand is made that was not found in a source

**Quality checks (is the copy good?)**
- [ ] Short description is 60–100 words (count them)
- [ ] Long description is 280–400 words (count plain-text words, ignoring HTML tags)
- [ ] Short description contains a geographic delivery signal ("Nigeria", "Lagos", "West Africa", or "across West Africa") — vary across products, do not repeat the same phrase, do NOT use "across Africa" or "across the continent"
- [ ] Long description contains the product name in the first paragraph
- [ ] Long description contains the brand name at least twice
- [ ] No sentence starts with "Introducing" or "Experience" — these are clichés to avoid
- [ ] No phrase like "a fragrance for everyone" or "suitable for all occasions" — be specific
- [ ] HTML structure is intact: `<p>`, `<h3>`, `<strong>`, `<br>` tags are all properly closed

**If any check fails:** note which check failed, rewrite the relevant section, and
re-run only the failed checks before proceeding.

After passing all checks, record `"qa_passed": true` in the staging entry.
If checks fail after 2 rewrites, record `"qa_passed": false` and `"qa_notes"` explaining what could not be resolved, then move on.

---

### 3d. Stage the result

Read `tools/descriptions_staging.json`, append this entry, write it back:

```json
{
  "id": <product_id>,
  "name": "<product name>",
  "permalink": "<url>",
  "price_usd": "<price>",
  "categories": ["<cat1>"],
  "research": {
    "sources_used": ["<url1>", "<url2>"],
    "top_notes": "<comma-separated notes or empty>",
    "heart_notes": "<comma-separated notes or empty>",
    "base_notes": "<comma-separated notes or empty>",
    "longevity": "<value or empty>",
    "projection": "<value or empty>",
    "fragrance_family": "<value or empty>",
    "perfumer": "<value or empty>",
    "launch_year": "<value or empty>"
  },
  "short_description": "<plain text>",
  "description": "<HTML>",
  "qa_passed": true or false,
  "qa_notes": "<any QA failures or empty string>",
  "update_status": "draft",
  "update_error": ""
}
```

Wait 1 second before moving to the next product.

---

## Step 4 — Export Excel report

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/export_to_excel.py
```

Capture and display the output path.

---

## Step 5 — Final summary

```
=== PRODUCT DESCRIPTIONS DRAFT COMPLETE ===

Processed  : X products
QA Passed  : X
QA Failed  : X  (see Excel Sheet 1 — qa_notes column for details)

Excel report: audit_reports/product_descriptions_<timestamp>.xlsx
  Sheet 1: Summary        — status and QA result per product
  Sheet 2: Research Data  — notes and sources per product
  Sheet 3: Generated Copy — plain-text descriptions for reading
  Sheet 4: Raw HTML       — HTML ready to paste into WooCommerce

Next step: review the Excel, approve descriptions, then run:
  /product-descriptions --push
```

---

## Important rules

- Never invent fragrance notes — only write notes found across the 6 sources.
- Never fabricate brand history — only use verifiable claims.
- Always use HTML in the long description field.
- Short description must be plain text (no HTML tags).
- If any source is unreachable, continue to the next — only write descriptions
  from what was actually found. Record every failed fetch in `sources_used`
  with a `(failed)` suffix (e.g. `"https://fragrantica.com/... (failed)"`)
  so failures are clearly visible in the Excel report.
