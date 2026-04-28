# Scentified Marketing Suite — User Manual

**Project:** cascades-marketing  
**Store:** scentifiedperfume.com  
**Last updated:** April 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Slash Commands Reference](#2-slash-commands-reference)
3. [Setup & Configuration](#3-setup--configuration)
4. [Skill: /audit](#4-skill-audit)
5. [Skill: /product-descriptions](#5-skill-product-descriptions)
6. [Skill: /seo-gaps](#6-skill-seo-gaps)
7. [Streamlit Web App](#7-streamlit-web-app)
8. [Understanding the Reports](#8-understanding-the-reports)
9. [Tools Reference](#9-tools-reference)
10. [Project File Structure](#10-project-file-structure)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Overview

The Scentified Marketing Suite is a Claude Code project that gives you AI-powered slash commands for running, writing, and pushing content for scentifiedperfume.com — plus a live Streamlit web app for non-technical team members.

| Command | What it does |
|---|---|
| `/audit` | Runs a full 9-point eCommerce audit and generates a scored PDF report |
| `/product-descriptions` | Researches products, writes SEO copy, verifies quality, and pushes descriptions to WooCommerce |
| `/seo-gaps` | Generates optimised RankMath SEO titles and meta descriptions, exports for review, and pushes live |

Slash commands are invoked directly in Claude Code (the CLI, VS Code extension, or desktop app). No terminal commands needed — just type the slash command and Claude handles everything.

The [Streamlit web app](#7-streamlit-web-app) provides a browser-based UI for running audits, managing descriptions, analysing SEO gaps, and viewing Market SEO Intelligence (keyword trends, competitor gaps, Search Console data).

---

## 2. Slash Commands Reference

> **How to add a new command:** Create a new skill file at `.claude/skills/<command-name>/SKILL.md`, then add it to the table below in the relevant category. The command is immediately available in Claude Code with no restart required.

### Scentified — Store Operations

These commands are scoped to scentifiedperfume.com.

| Command | Description |
|---|---|
| `/audit` | Full 9-point eCommerce audit → scored PDF + JSON |
| `/audit` | Re-run any time — score history is tracked automatically |

### Scentified — Content & SEO

| Command | Description |
|---|---|
| `/product-descriptions` | Research & write descriptions for 5 products with no copy |
| `/product-descriptions 10` | Same, for 10 products |
| `/product-descriptions 20` | Same, for 20 products |
| `/product-descriptions --all` | Research & write for every product missing a description |
| `/product-descriptions --reformat` | Reformat 10 existing descriptions into the SEO template |
| `/product-descriptions --reformat 20` | Same, for 20 products |
| `/product-descriptions --reformat --all` | Reformat every old-format product |
| `/product-descriptions --reformat --brand "BTV"` | Reformat all BTV products |
| `/product-descriptions --reformat --brand "Clive Christian"` | Reformat all Clive Christian products |
| `/product-descriptions --status` | Live count of products by status and image coverage |
| `/product-descriptions --no-image` | List all products with no images |
| `/product-descriptions --no-image 20` | List up to 20 products with no images |
| `/product-descriptions --no-image --brand "BTV"` | No-image products for one brand |
| `/product-descriptions --push` | Push all QA-approved descriptions live to WooCommerce |
| `/seo-gaps` | Generate SEO titles & meta descriptions for 10 products with no RankMath title |
| `/seo-gaps 20` | Same, for 20 products |
| `/seo-gaps --all` | Optimise every product regardless of current SEO status |
| `/seo-gaps --brand "BTV"` | Optimise all products for one brand |
| `/seo-gaps --ids 123,456,789` | Optimise specific products by WooCommerce ID |
| `/seo-gaps --dry-run` | Preview what would be pushed without making any changes |
| `/seo-gaps --push` | Push all QA-approved SEO data live |

### Marketing — Content & Campaigns

| Command | Description |
|---|---|
| `/market-social` | Generate a 7-day Instagram/TikTok content calendar from your product catalogue |
| `/market-social --month` | 28-day content calendar |
| `/market-social --product "Name"` | 5 posts dedicated to one product |
| `/market-social --brand "Name"` | 7 posts showcasing one brand |
| `/market-social --reels` | TikTok/Reels video scripts only |
| `/market-social --stories` | Instagram Stories sequences only |
| `/market-emails --sequence welcome` | 4-email welcome sequence for new subscribers |
| `/market-emails --sequence abandoned-cart` | 3-email cart recovery sequence |
| `/market-emails --sequence new-arrivals` | Single new product announcement email |
| `/market-emails --sequence vip` | 3-email VIP/loyalty sequence for repeat buyers |
| `/market-emails --sequence re-engagement` | 3-email win-back sequence for inactive subscribers |
| `/market-emails --sequence launch --brand "Name"` | 3-email brand launch sequence |
| `/market-ads` | Full Meta + Google ad campaign for the store |
| `/market-ads --product "Name"` | Ad set for one specific product |
| `/market-ads --brand "Name"` | Campaign for all products from one brand |
| `/market-ads --platform meta` | Meta (Facebook + Instagram) only |
| `/market-ads --platform google` | Google Search + Performance Max only |
| `/market-ads --retargeting` | Retargeting sequences for warm audiences only |

### Marketing — Strategy & Brand

| Command | Description |
|---|---|
| `/market-brand` | Analyse Scentified's brand voice and produce a BRAND-VOICE.md guidelines document |
| `/market-brand --quick` | Condensed version: voice summary, do's/don'ts, and copy samples only |
| `/market-brand --compare` | Include competitor voice comparison (3 Nigerian luxury retailers) |
| `/market-launch --brand "Name"` | Full 4-week launch playbook for a new brand (e.g. first time carrying Fragrance du Bois) |
| `/market-launch --product "Name"` | 2-week spotlight campaign for a single hero product |
| `/market-launch --seasonal "Campaign"` | Seasonal campaign plan (Valentine's Day, Eid, Christmas, etc.) |
| `/market-launch --restock "Brand"` | Quick 2-week restock announcement plan |

### System & Configuration

| Command | Description |
|---|---|
| `/update-config` | Update `config.py` credentials (WooCommerce keys, API key) interactively |

### Quick Reference: Which command for which situation?

| Situation | Command |
|---|---|
| Product has NO description at all | `/product-descriptions` |
| Product HAS a description but it's in the old format | `/product-descriptions --reformat` |
| Reformat an entire brand in one go | `/product-descriptions --reformat --brand "Brand Name"` |
| Find products with no images | `/product-descriptions --no-image` |
| Check how many products still need work | `/product-descriptions --status` |
| Push all approved descriptions live | `/product-descriptions --push` |
| Generate SEO titles for products that have none | `/seo-gaps` |
| Generate SEO titles for a specific brand | `/seo-gaps --brand "Brand Name"` |
| Push approved SEO data live | `/seo-gaps --push` |
| Run a full site health check | `/audit` |
| Plan a week of Instagram content | `/market-social --week` |
| Write email sequences for customers | `/market-emails --sequence welcome` |
| Generate Meta + Google ad copy | `/market-ads` |
| Generate ad copy for one specific product | `/market-ads --product "Name"` |
| Document Scentified's brand voice | `/market-brand` |
| Create a launch plan for a new brand | `/market-launch --brand "Name"` |
| Create a seasonal campaign plan | `/market-launch --seasonal "Valentine's Day"` |

---

## 3. Setup & Configuration

### Prerequisites

```
Python 3.x (installed as `py` on Windows)
pip packages: see requirements.txt
```

Install all dependencies:
```bash
py -m pip install -r requirements.txt
```

### config.py

All credentials and settings live in `config.py`. Edit this file before first use:

```python
CONFIG = {
    "store_url":            "https://scentifiedperfume.com",
    "woo_consumer_key":     "ck_...",       # WooCommerce REST API key
    "woo_consumer_secret":  "cs_...",       # WooCommerce REST API secret
    "pagespeed_api_key":    "AIza...",      # Google PageSpeed Insights API key
}
```

**Where to find these:**
- WooCommerce keys: WooCommerce > Settings > Advanced > REST API
- PageSpeed API key: Google Cloud Console > APIs & Services > PageSpeed Insights API

### Streamlit Cloud secrets

When running the web app on Streamlit Community Cloud, credentials are stored in `.streamlit/secrets.toml` (configured via the Streamlit Cloud dashboard, not committed to git):

```toml
[woocommerce]
store_url        = "https://scentifiedperfume.com"
consumer_key     = "ck_..."
consumer_secret  = "cs_..."

[pagespeed]
api_key = "AIza..."

[gsc]
client_id     = "..."
client_secret = "..."
refresh_token = "..."
site_url      = "https://scentifiedperfume.com/"
```

---

## 4. Skill: /audit

### What it does

Runs a complete eCommerce health check across 9 dimensions and produces:
- A scored **PDF report** (branded, with charts)
- A raw **JSON file** with all data
- A running **score history** so you can track improvement over time

### How to run

In Claude Code, type:
```
/audit
```

Allow up to **3 minutes** to complete. The PageSpeed audit alone takes 60–90 seconds because it runs Google Lighthouse twice (mobile + desktop).

### What gets audited

| Audit | What it checks |
|---|---|
| **Mobile Speed** | Google PageSpeed score, LCP, TBT, CLS, Speed Index |
| **Desktop Speed** | Same metrics on desktop |
| **Store UX** | Viewport meta tag, mobile navigation, button sizes, search functionality |
| **SEO** | Title tags, meta descriptions, H1/H2 structure, structured data, sitemap, robots.txt |
| **Products** | Product images, descriptions, reviews, perfume-specific keywords |
| **Checkout** | SSL, guest checkout, payment security, friction points |
| **Competitors** | Gap analysis vs. known competitors (video, loyalty, bundles, live chat, free shipping) |
| **Pricing Intelligence** | Brand price mapping, competitive positioning |
| **Revenue Potential** | Estimated monthly revenue impact of fixing top issues |

### Reading the terminal summary

```
=== SCENTIFIED AUDIT COMPLETE ===

Overall Score:  72/100  (Needs Work)
vs Last Run:    +4 pts

Score Breakdown:
  Mobile Speed:    45/100
  Desktop Speed:   71/100
  Store UX:        80/100
  SEO:             68/100
  Products (avg):  74/100
  Checkout:        85/100

Top Issues Found:
  1. Mobile LCP is 8.2s — target is under 2.5s
  2. 47 products missing long descriptions
  3. No structured data (JSON-LD) on product pages
```

### Score grades

| Score | Grade | Meaning |
|---|---|---|
| 85–100 | Excellent | Minor optimisations only |
| 70–84 | Good | Clear opportunities to improve |
| 55–69 | Needs Work | Significant gaps to address |
| 40–54 | Poor | Major overhaul needed |
| 0–39 | Critical | Fundamental issues |

### Output files

Every run saves two files to `audit_reports/`:

```
audit_reports/
  audit_20260421_200254.json                 Raw data (all scores, issues, recommendations)
  scentified_audit_v2_20260421_200254.pdf    Formatted PDF report for sharing
  score_history.json                          All runs appended — tracks progress over time
```

---

## 5. Skill: /product-descriptions

### What it does

A two-phase workflow:

**Phase 1 — Research & Write**  
Fetches products missing descriptions from WooCommerce, researches each one across up to 6 sources, writes SEO-optimised short and long descriptions, verifies them against a 13-point QA checklist, and exports an Excel report for review.

**Phase 2 — Push**  
After you review and approve the Excel, push the descriptions live to WooCommerce with a single command.

### Commands

#### Research & write (default — 5 products)
```
/product-descriptions
```

#### Research & write — custom batch size
```
/product-descriptions 10
/product-descriptions 20
```

#### Research & write — all products missing descriptions
```
/product-descriptions --all
```

#### Reformat existing descriptions into the new SEO template (default — 10 products)
```
/product-descriptions --reformat
/product-descriptions --reformat 20
/product-descriptions --reformat --all
```

#### Reformat all products for one brand at once
```
/product-descriptions --reformat --brand "BTV"
/product-descriptions --reformat --brand "Clive Christian"
```

#### Check live progress — counts by status and image coverage across all products
```
/product-descriptions --status
```

#### List products with no images
```
/product-descriptions --no-image
/product-descriptions --no-image 20
/product-descriptions --no-image --brand "BTV"
```

#### Push approved descriptions live
```
/product-descriptions --push
```

### When to use which command

| Situation | Command |
|---|---|
| Product has NO description at all | `/product-descriptions` |
| Product HAS a description but it's in the old format | `/product-descriptions --reformat` |
| Reformat an entire brand in one go | `/product-descriptions --reformat --brand "Brand Name"` |
| Find products with no images | `/product-descriptions --no-image` |
| Check how many products still need work | `/product-descriptions --status` |
| Push all approved/staged descriptions live | `/product-descriptions --push` |

### Phase 1 in detail: Research → Write → QA → Stage → Excel

**Step 1 — Initialise**  
Clears `tools/descriptions_staging.json` to start fresh.

**Step 2 — Fetch product list**  
Queries the WooCommerce REST API for published products that have no long description. Respects the `--limit` or `--all` argument.

**Step 3 — For each product: research**  
Claude searches and fetches up to 6 sources per product:

| Source | What is extracted |
|---|---|
| Product page (scentifiedperfume.com) | Existing copy, notes, size, concentration |
| Fragrantica | Top/heart/base notes, fragrance family, longevity, sillage, launch year, perfumer |
| Brand official site | Brand story, inspiration, mood language, official note listing |
| Wikiparfum | Notes, concentration, launch year, additional storytelling |
| Basenotes | Notes, fragrance family, community performance ratings |
| Secondary retailer (fallback) | Any remaining notes from Harrods, Selfridges, Luckyscent, etc. |

All attempted URLs are recorded — including failures — so you can see exactly what was found where.

**Step 4 — Write descriptions**  
Two descriptions are written per product using only facts found in Step 3:

*Short description (plain text, 60–100 words)*
- Names the brand, key notes, concentration, bottle size
- Always includes "Nigeria", "Lagos", "West Africa", or "across West Africa" — varied across products
- Tone: confident, sensory, aspirational

*Long description (HTML, 280–400 words)*
- Structured with `<h3>` headings: Fragrance Notes, Performance, Best For, About [Brand]
- For skincare/body care products: Key Ingredients, How To Use, Best For, About [Brand]
- Ends with an authenticity + delivery tagline

**Step 5 — QA checklist (13 points)**  
Every description is verified before it is staged. If a check fails, Claude rewrites the section and re-checks. If it still fails after two rewrites, the product is flagged `qa_passed: false` and noted in the Excel.

The checklist covers:
- Notes/ingredients are specific to this product (not generic)
- Opening paragraph is unique to this product
- Brand section describes the correct brand
- Concentration and bottle size match the listing
- Every note listed was found in at least one source
- Longevity/projection match the Fragrantica ratings
- Short description is 60–100 words
- Long description is 280–400 words
- Contains "Nigeria", "Lagos", "West Africa", or "across West Africa"
- Product name in the long description opening
- Brand name appears at least twice
- No clichéd openers ("Introducing…", "Experience…")
- No generic copy ("suitable for all occasions")

**Step 6 — Export Excel**  
Generates a formatted Excel workbook at `audit_reports/product_descriptions_<timestamp>.xlsx` with four sheets:

| Sheet | Contents |
|---|---|
| Summary | One row per product: QA pass/fail, word counts, category, price |
| Research Data | Notes pyramid, longevity, projection, all sources used per product |
| Generated Copy | Plain-text readable versions of both descriptions |
| Raw HTML | HTML ready to copy-paste into WooCommerce if needed |

### Reformat mode in detail: --reformat

Use this when products already have descriptions but in the old narrative format. The store currently has ~323 products still needing reformatting into the structured SEO template.

**What it does differently from the standard research flow:**
- Notes are extracted from the existing `current_desc` / `current_short` rather than researched from scratch
- Brand information is looked up once per brand and reused across all products of that brand
- Only Performance data (longevity, projection) is freshly researched per product
- The opening narrative from the existing description is kept or lightly refined (not rewritten)
- Packaging/bottle descriptions are preserved as an additional paragraph

**Auto-detection — no skip list needed:**  
The `--reformat` command automatically detects which products are still in the old format by checking for the presence of `<h3>` tags. Products already reformatted are excluded automatically. You never need to maintain a manual skip list.

**Brand batch mode:**  
To reformat an entire brand at once without counting products manually:
```
/product-descriptions --reformat --brand "BTV"
```
This fetches every old-format product in the BTV category and processes them all in one session.

**Recommended batch size:** 10–20 products for mixed batches, or use `--brand` to clear one brand at a time.

| Session | Command | Products covered |
|---|---|---|
| Mixed batch | `/product-descriptions --reformat 20` | Next 20 old-format products |
| Full brand | `/product-descriptions --reformat --brand "Clive Christian"` | All Clive Christian |
| Check progress | `/product-descriptions --status` | Live count of remaining work |
| Push | `/product-descriptions --push` | All approved |

After each batch, review the Excel, then run `--push` before starting the next batch — or accumulate several batches in the staging file and do a single push at the end.

### Phase 2 in detail: Push live

After reviewing the Excel:

```
/product-descriptions --push
```

This runs `tools/push_descriptions.py`, which:
1. Reads `tools/descriptions_staging.json`
2. Skips any entry where `qa_passed` is `false`
3. Sends a PUT request to the WooCommerce REST API for each approved product
4. Updates `update_status` to `"success"` or `"failed"` in the staging file
5. Reports a push summary

**Nothing is ever pushed automatically.** You must explicitly run `--push` after reviewing.

---

## 6. Skill: /seo-gaps

### What it does

Generates optimised SEO titles and meta descriptions for every product and pushes them to WooCommerce via RankMath. Produces an Excel report showing current vs. proposed copy side by side before anything goes live.

**Requires:** RankMath SEO plugin installed and active on WordPress.

### Commands

#### Optimise products with no SEO title yet (default — 10 products)
```
/seo-gaps
/seo-gaps 20
```

#### Optimise all products for one brand
```
/seo-gaps --brand "BTV"
/seo-gaps --brand "Clive Christian"
```

#### Optimise specific products by ID
```
/seo-gaps --ids 123,456,789
```

#### Optimise every product regardless of current SEO status
```
/seo-gaps --all
```

#### Preview what would be pushed (no changes made)
```
/seo-gaps --dry-run
```

#### Push approved SEO titles and descriptions live
```
/seo-gaps --push
```

### What gets generated per product

**Focus Keyword (2–4 words)**  
Formula: `[Brand short name] [Product short name] [EDP/EDT/Parfum]`  
Chosen for Nigerian buyer search intent.

**SEO Title (50–60 characters)**  
Keyword-first formula: `[Focus Keyword] | Buy in Nigeria — Scentified`  
Optimised for Google's 60-character display limit and local buying intent.

**Meta Description (140–155 characters)**  
Hook + performance signal + authenticity claim + CTA.  
Always includes "Nigeria", "Lagos", or "West Africa" as the primary local intent signal.

**Content Patch**  
Embeds the focus keyword in the first paragraph of the product description, adds an internal link to the brand's category page, and adds an external DoFollow link to the brand's official website.

**Slug Optimisation**  
Proposes a cleaner URL slug only when the current one is clearly suboptimal (too long or missing the brand/product name).

**Image Alt Text**  
Formula: `[Focus Keyword] perfume Nigeria` — set on the product's primary image.

### Excel report sheets

| Sheet | Contents |
|---|---|
| Summary | QA result, character counts for current and proposed titles/descriptions |
| Side by Side | Current vs. proposed titles and descriptions for easy reading and approval |
| Research Data | Primary keyword, SERP notes, sources used per product |

### Output files

```
audit_reports/seo_gaps_<timestamp>.xlsx     Excel review report
tools/seo_staging.json                       Working file — cleared on each new run
```

---

## 7. Streamlit Web App

### Live URL

The app is deployed on Streamlit Community Cloud. Ask the project owner for the current URL, or access it via your Streamlit Cloud dashboard.

### What the web app does

The Streamlit app gives anyone on the team browser-based access to the same tools available via slash commands — no Claude Code required. It is ideal for running audits, reviewing staging data, and monitoring Market SEO Intelligence.

### Tabs

| Tab | What it does |
|---|---|
| **Audit** | Runs the full 9-point eCommerce audit. Displays a live progress log and the final scored summary. Downloadable JSON and PDF links appear on completion. |
| **Descriptions** | Shows the current `descriptions_staging.json` — all staged products with QA status, word counts, and descriptions. Push approved descriptions live directly from this tab. |
| **SEO Gaps** | Shows the current `seo_staging.json`. Displays Search Console quick wins (product pages ranking 4–10 that could reach top 3) at the top. Stage quick wins for one-click SEO improvement. Push approved SEO data live from this tab. |
| **Market SEO** | Three intelligence modules: Keyword Research (Google Autocomplete data for Nigerian perfume queries + Google Trends), Competitor SEO (scrapes competitor pages and shows title/meta/H1/keyword gaps), Search Console (top queries, Nigeria-only queries, low-CTR pages, quick wins — all pulled live from Google Search Console via OAuth). |

### Running the app locally

```bash
py -m streamlit run app.py
```

The app reads credentials from `config.py` (for WooCommerce) and `st.secrets` (for Streamlit Cloud). Locally, it falls back to `config.py` automatically.

### Credentials required for each tab

| Tab | Credentials needed |
|---|---|
| Audit | WooCommerce key + secret, PageSpeed API key |
| Descriptions | WooCommerce key + secret |
| SEO Gaps | WooCommerce key + secret |
| Market SEO — Search Console | GSC client ID, client secret, refresh token, site URL |
| Market SEO — Keyword Research | None (uses public Google Autocomplete endpoint) |
| Market SEO — Competitor SEO | None (uses public web scraping) |

### Setting up Google Search Console (one-time)

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project
2. Enable the **Google Search Console API**
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download the client secret JSON
5. Run `py get_gsc_token.py` — it opens a browser, you authenticate, it prints your `refresh_token`
6. Add `client_id`, `client_secret`, and `refresh_token` to Streamlit Cloud secrets under `[gsc]`

---

## 8. Understanding the Reports

### Audit PDF (`scentified_audit_v2_<timestamp>.pdf`)

A branded, printable report containing:
- Overall score and grade
- Score breakdown by category with colour-coded indicators
- Top issues ranked by priority
- Revenue impact estimates for each fix
- Competitor gap analysis
- Recommendations with implementation steps

Good for: sharing with stakeholders, tracking quarterly progress.

### Audit JSON (`audit_<timestamp>.json`)

Raw data from all 9 audits. Useful for:
- Debugging specific audit results
- Building dashboards or integrations
- Comparing granular scores between runs

### Score History (`score_history.json`)

An append-only log of every audit run:
```json
[
  { "date": "2026-04-15", "overall": 68, "mobile": 41, "seo": 62, ... },
  { "date": "2026-04-21", "overall": 72, "mobile": 45, "seo": 68, ... }
]
```

Used by `/audit` to show the `vs Last Run` delta automatically.

### Product Descriptions Excel (`product_descriptions_<timestamp>.xlsx`)

Four-sheet review document. The most important columns in **Sheet 1 (Summary)**:

| Column | What to check |
|---|---|
| QA | PASS = ready to push. FAIL = see qa_notes |
| QA Notes | Explains what the AI couldn't resolve |
| Short (chars) | Should be 300–600 characters |
| Long (words) | Should be 280–400 words |

**Sheet 4 (Raw HTML)** is the copy you'd paste directly into WooCommerce > Product > Description if you preferred to do it manually.

### SEO Gaps Excel (`seo_gaps_<timestamp>.xlsx`)

Three-sheet review document:

| Sheet | What to check |
|---|---|
| Summary | QA result, character counts — confirm title is 50–60 chars, description is 140–155 chars |
| Side by Side | Read both current and proposed copy — approve or note any changes needed |
| Research Data | Focus keyword, SERP notes, keyword density — useful if a title needs manual adjustment |

---

## 9. Tools Reference

These scripts are called by the skills automatically. You can also run them manually.

### fetch_no_desc.py

Fetches published WooCommerce products and outputs a JSON array to stdout.

```bash
py tools/fetch_no_desc.py                          # products missing descriptions
py tools/fetch_no_desc.py --limit 10               # cap at 10
py tools/fetch_no_desc.py --all                    # all products regardless of description status
py tools/fetch_no_desc.py --has-desc               # products that have any description (old or new format)
py tools/fetch_no_desc.py --needs-reformat         # products with old-format descriptions (no <h3> tag)
py tools/fetch_no_desc.py --needs-reformat --brand "BTV"   # old-format products for one brand only
py tools/fetch_no_desc.py --needs-reformat --limit 20      # cap old-format results
py tools/fetch_no_desc.py --no-image               # products with no images at all
py tools/fetch_no_desc.py --no-image --brand "BTV" # no-image products for one brand
```

Output: JSON array to stdout.

### status.py

Queries WooCommerce live and prints a full progress report: how many products have no description, how many are in the old format, and how many are already done — broken down by brand.

```bash
py tools/status.py
```

Output: terminal table. Also run via `/product-descriptions --status`.

### push_descriptions.py

Pushes `qa_passed: true` entries from the staging file to WooCommerce.

```bash
py tools/push_descriptions.py              # push all approved entries
py tools/push_descriptions.py --dry-run   # preview without pushing
```

### export_to_excel.py

Converts the staging JSON to the 4-sheet Excel report.

```bash
py tools/export_to_excel.py
```

Output: `audit_reports/product_descriptions_<timestamp>.xlsx`

### fetch_seo_data.py

Fetches products with their current RankMath SEO title and meta description.

```bash
py tools/fetch_seo_data.py                    # all products
py tools/fetch_seo_data.py --no-seo           # products with no RankMath title set
py tools/fetch_seo_data.py --brand "BTV"      # filter by brand
py tools/fetch_seo_data.py --no-seo --limit 20
```

### push_seo.py

Pushes `qa_passed: true` entries from `seo_staging.json` to WooCommerce by writing `rank_math_title` and `rank_math_description` to each product's meta data.

```bash
py tools/push_seo.py              # push all approved entries
py tools/push_seo.py --dry-run   # preview without pushing
```

### export_seo_excel.py

Exports `seo_staging.json` to the 3-sheet Excel report.

```bash
py tools/export_seo_excel.py
```

Output: `audit_reports/seo_gaps_<timestamp>.xlsx`

### update_product.py

Updates a single product from a JSON payload file (used by push_descriptions.py internally).

```bash
py tools/update_product.py path/to/payload.json
```

### get_gsc_token.py

One-time OAuth flow for Google Search Console. Opens a browser, you authenticate, and it prints `client_id`, `client_secret`, and `refresh_token` for Streamlit secrets.

```bash
py get_gsc_token.py
```

---

## 10. Project File Structure

```
cascades-marketing/
├── config.py                   API keys, store URL, benchmarks
├── main.py                     Audit entry point — runs all 9 audits
├── app.py                      Streamlit web UI (all 4 tabs)
├── get_gsc_token.py            One-time OAuth flow for Google Search Console
├── requirements.txt            Python dependencies for Streamlit Cloud
├── USER_MANUAL.md              This document
│
├── .claude/skills/
│   ├── audit/SKILL.md                    /audit command definition
│   ├── product-descriptions/SKILL.md     /product-descriptions command definition
│   └── seo-gaps/SKILL.md                 /seo-gaps command definition
│
├── tools/                      Product description and SEO tools
│   ├── fetch_no_desc.py        Fetch products (by desc status, format, or brand)
│   ├── fetch_seo_data.py       Fetch products with current RankMath SEO data
│   ├── status.py               Live progress report — counts by status and brand
│   ├── push_descriptions.py    Push approved descriptions to WooCommerce
│   ├── push_seo.py             Push approved SEO titles/descriptions via RankMath fields
│   ├── update_product.py       Single-product update utility
│   ├── export_to_excel.py      Export descriptions staging JSON → Excel
│   ├── export_seo_excel.py     Export SEO staging JSON → Excel
│   ├── descriptions_staging.json  Working file for /product-descriptions
│   └── seo_staging.json           Working file for /seo-gaps
│
├── audits/                     Audit modules
│   ├── pagespeed.py            Google PageSpeed (mobile + desktop)
│   ├── seo.py                  SEO health checks
│   ├── ux.py                   Store UX checks
│   ├── products.py             Product page quality
│   ├── checkout.py             Checkout flow & security
│   └── competitors.py          Competitor feature gap analysis
│
├── integrations/
│   └── woocommerce.py          WooCommerce REST API client
│
├── intelligence/
│   ├── price.py                Brand price mapping
│   ├── revenue.py              Revenue impact calculator
│   ├── keyword_research.py     Google Autocomplete + Google Trends for Nigerian keywords
│   ├── competitor_seo.py       Competitor page scraper — title/meta/H1/keyword gap analysis
│   └── search_console.py       Google Search Console API — top queries, Nigeria queries, quick wins
│
├── reporting/
│   ├── compiler.py             Assembles final report object
│   └── pdf_generator.py        Renders PDF with ReportLab
│
├── history/
│   └── tracker.py              Score history load/save/diff
│
├── utils/
│   └── helpers.py              HTTP client, logging, formatting
│
└── audit_reports/              All generated output files
    ├── audit_*.json
    ├── scentified_audit_v2_*.pdf
    ├── product_descriptions_*.xlsx
    ├── seo_gaps_*.xlsx
    └── score_history.json
```

---

## 11. Troubleshooting

### `/audit` fails with PageSpeed timeout

The PageSpeed API can take 60–90 seconds to audit a slow site. The script uses a 90-second timeout with 3 automatic retries (10s / 20s / 30s backoff). If it still fails:
- Check your PageSpeed API key in `config.py`
- Verify you have the PageSpeed Insights API enabled in Google Cloud Console
- Try again — Lighthouse failures are often transient

### `/product-descriptions` — product page returns 403

scentifiedperfume.com blocks automated fetches of its own product pages. This is expected. Claude falls back to the other 5 research sources (Fragrantica, brand site, Wikiparfum, Basenotes, retailer). All 403 failures are logged in the Excel `Sources Used` column.

### Fragrantica also returns 403

Fragrantica blocks direct WebFetch requests. Claude automatically falls back to extracting note data from Google search snippets about the Fragrantica page. Notes sourced this way are marked `(notes extracted via WebSearch snippet)` in the sources list.

### WooCommerce push fails with HTTP 401

Authentication error. Check that:
- `woo_consumer_key` and `woo_consumer_secret` in `config.py` are correct
- The API key has **Read/Write** permissions (not Read-only)
- The key is for the correct store URL

### Excel file won't open / shows garbled characters

Make sure `openpyxl` is installed:
```bash
py -m pip install openpyxl
```
Close any previously opened Excel files before re-running the export — Excel locks the file.

### `py` command not found

On some Windows setups, Python is invoked as `python` instead of `py`. Try:
```bash
python tools/export_to_excel.py
```
If neither works, reinstall Python from python.org and ensure "Add to PATH" is checked.

### How to re-push after fixing a failed product

1. Open `tools/descriptions_staging.json`
2. Find the entry with `"update_status": "failed"`
3. Fix the issue (or correct the description manually)
4. Set `"qa_passed": true`
5. Run `/product-descriptions --push`

### Search Console shows no data

- Verify `gsc.refresh_token` in Streamlit secrets is valid — tokens expire if unused for 6 months
- Re-run `py get_gsc_token.py` to get a fresh token
- Confirm `gsc.site_url` exactly matches the property URL in Search Console (including trailing slash)
- Confirm the Google account used for OAuth has access to the Search Console property

### Streamlit Cloud build fails

Check the deployment logs in the Streamlit Cloud dashboard. Common causes:
- A dependency in `requirements.txt` is incompatible with Python 3.14 (pytrends is a known issue — it is excluded for this reason)
- A secrets key is missing or misnamed — compare against the `[woocommerce]`, `[pagespeed]`, and `[gsc]` structure above

---

*Scentified Marketing Suite — built with Claude Code*
