# Social Media Content Calendar & Generation

Generate a structured social media content calendar and ready-to-post captions for Scentified's Instagram and TikTok channels. Content is grounded in real products from the WooCommerce catalogue, Scentified's brand voice, and the Nigerian luxury market.

**Output:** A formatted content calendar + ready-to-use captions, hashtag sets, and visual direction notes — exported as an Excel file and printed as a summary.

---

## Arguments

- No args / `--week`        → 7-day content calendar (one post per day)
- `--month`                 → 28-day content calendar (4 weeks)
- `--product "Name or ID"` → 5 posts dedicated to one specific product
- `--brand "Name"`          → 7 posts showcasing one brand (e.g. "BTV", "Clive Christian")
- `--reels`                 → generate only Reels/TikTok video scripts (15–30 second)
- `--stories`               → generate only Instagram Stories sequences (5-frame sequences)

---

## Brand Voice & Context

Always write from this perspective:

**Scentified is West Africa's destination for luxury and niche perfumery.** The tone is:
- Knowledgeable but never snobbish — a trusted guide, not a gatekeeper
- Aspirational but grounded in Nigerian reality (Lagos traffic, harmattan season, Owambe events, office culture)
- Warm and engaging — not corporate
- Sensory and evocative — describe how fragrances feel, not just what they smell like

**Geographic signals:** Nigeria, Lagos, West Africa. Never "across Africa" or "across the continent."

**Price framing:** Scentified sells luxury items. Never apologise for the price. Frame it as investment, value, authenticity.

**Authenticity:** Always note that fragrances are genuine/sourced directly. This matters deeply to Nigerian buyers who distrust fakes.

---

## Content Pillars

Distribute posts across these 5 pillars. Never run the same pillar two days in a row.

| Pillar | % of calendar | What it does |
|---|---|---|
| **Product Spotlight** | 30% | Features a specific product — bottle, notes, who it's for |
| **Brand Story** | 20% | Educates on the brand heritage (BTV, Clive Christian, etc.) |
| **Fragrance Education** | 20% | Tips: how to layer, fragrance families, longevity, application spots |
| **Lifestyle & Occasions** | 15% | Ties fragrances to Nigerian life — Owambe, office, date night, travel |
| **Social Proof & Promotions** | 15% | Testimonials format, "recently restocked", gift ideas, seasonal offers |

---

## Step 1 — Fetch products to feature (unless `--product` or `--brand` specified)

If generating a calendar (no specific product/brand), fetch recent products to populate Product Spotlight days:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 20
```

From the output, select 2–3 products per week to feature as Product Spotlights. Prioritise:
1. Products with complete descriptions and images (best to showcase)
2. Mix of price points — at least one premium (₦300,000+) and one accessible (under ₦200,000) per week
3. Mix of brands — don't feature the same brand twice in one week

If the fetch fails or returns empty, select 3 fictional but realistic Scentified products for the draft (note: "placeholder — replace with actual product from your catalogue").

---

## Step 2 — Plan the calendar

Build a day-by-day plan in this format before writing any captions:

```
Day 1 (Monday)   | Platform: Instagram Feed  | Pillar: Product Spotlight  | Product: [Name]
Day 2 (Tuesday)  | Platform: Instagram Story | Pillar: Fragrance Education| Topic: How to find your signature scent
Day 3 (Wednesday)| Platform: Instagram Feed  | Pillar: Brand Story        | Brand: Clive Christian
...
```

**Platform rotation for a 7-day week:**
- Monday: Instagram Feed (high-quality product image)
- Tuesday: Instagram Stories (interactive — poll, quiz, or swipe-up)
- Wednesday: Instagram Feed (brand or lifestyle content)
- Thursday: TikTok / Reels (video concept)
- Friday: Instagram Feed (product spotlight or promotion)
- Saturday: Instagram Stories (behind-the-scenes or customer story)
- Sunday: Instagram Feed (aspirational lifestyle or education)

---

## Step 3 — Write captions

Write a complete caption for every day in the calendar.

### Instagram Feed caption structure

```
[Hook — 1 line. Must stop the scroll. Question, bold claim, or sensory opener.]

[Body — 3–5 lines. Tell the story: notes, occasion, feeling, who this is for. Use line breaks for readability. No walls of text.]

[CTA — 1 line. Specific action: "Link in bio to shop", "DM us to order", "Comment your favourite note below".]

.
.
[Hashtags — 20–25. Grouped: brand-specific + niche perfume + Nigeria lifestyle + Scentified branded]
```

**Caption rules:**
- Hook must be under 125 characters (shows before "more" cut-off on mobile)
- Body uses short paragraphs (2–3 lines max each)
- Emojis: 1–2 maximum per caption — this is luxury, not fast fashion
- Never use: "Introducing", "Experience", "Elevate your", "Step into", "Indulge in" — these are overused
- Nigerian references welcome but not forced — mention Lagos, Aso-Ebi, harmattan, etc. only when it fits naturally

**Example (Product Spotlight):**

```
What does ₦400,000 smell like?

Like oud aged for decades. Like leather warmed by skin.
Like the kind of confidence that doesn't need a room to notice you.

Clive Christian No. 1 EDP — one of the world's most expensive perfumes, now available in Lagos.
Authentic. Sourced directly. Delivered to your door.

Shop via the link in bio — or DM us to reserve your bottle.

.
.
#CliveChristian #No1Perfume #LuxuryPerfumeNigeria #NichePerfumeNigeria #PerfumeLagos #ScentsOfNigeria #FragranceNigeria #OudPerfume #LuxuryFragrance #NigerianLuxury #LagosLuxury #ScentifiedPerfume #WestAfricaFragrance #PerfumeCollection #FragranceCommunity #PerfumeAddict #OudLovers #NichePerfume #LuxuryLifestyleNigeria #AfricanLuxury #PerfumeOfTheDay #POTD #FragranceOfTheDay #FOTD #BuyPerfumeNigeria
```

### Instagram Stories structure (5 frames)

```
Frame 1: Hook / Question (text overlay on product image)
Frame 2: Answer / Education point (text-heavy, 2–3 bullet points)
Frame 3: Product reveal or tip detail
Frame 4: Interactive element — Poll ("Which would you choose?"), Quiz, or Slider
Frame 5: CTA — "Tap link to shop" / "DM to order" / "Swipe to see more"
```

Write the text overlay content for each frame. Keep each frame to 15 words or fewer.

### TikTok / Reels script structure (15–30 seconds)

```
[HOOK — 0:00–0:03] On-screen text or spoken line. Must create curiosity or controversy.
[CONTENT — 0:03–0:20] 3–5 quick cuts. Describe each: what's shown, what's said/text.
[CTA — 0:20–0:30] Spoken or text: "Link in bio", "Comment for price", "Follow for more".
```

Include:
- Suggested audio type (trending sound / voiceover / ambient / no sound)
- Hook text that would appear as on-screen text
- Visual suggestions (bottle close-up, spray shot, unboxing, notes listed on screen, etc.)

---

## Step 4 — Generate hashtag sets

Create 3 reusable hashtag sets that can be rotated across posts. Each set: 20–25 tags.

**Set A — Niche Perfume Focus**
Core: #NichePerfumeNigeria #NichePerfume #PerfumeCommunity #FragranceNerd
Add: brand-specific + Scentified branded + Nigeria lifestyle

**Set B — Luxury Lifestyle Focus**
Core: #LuxuryLifestyleNigeria #NigerianLuxury #LagosLuxury #LuxuryGifts
Add: occasion-based + aspirational + Nigeria location tags

**Set C — Education / Discovery Focus**
Core: #FragranceEducation #PerfumeTips #HowToWearPerfume #ScentProfile
Add: note-specific (e.g. #OudLovers #FloralPerfume) + discovery tags

---

## Step 5 — Export

Export the full calendar to Excel:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/export_social_calendar.py
```

If `export_social_calendar.py` does not exist, generate the Excel inline using Python (openpyxl) and save to `audit_reports/social_calendar_<timestamp>.xlsx`.

The Excel should have two sheets:

**Sheet 1 — Calendar**

| Day | Date | Platform | Post Type | Pillar | Product/Topic | Hook | Caption | Visual Direction | Hashtag Set |
|---|---|---|---|---|---|---|---|---|---|

**Sheet 2 — Hashtag Sets**
Three hashtag sets in full, ready to copy-paste.

---

## Step 6 — Final summary

```
=== SOCIAL CALENDAR DRAFT COMPLETE ===

Platform split:
  Instagram Feed    : X posts
  Instagram Stories : X sequences
  TikTok / Reels    : X scripts

Content pillars:
  Product Spotlights    : X posts  (products: [list names])
  Brand Stories         : X posts  (brands: [list names])
  Fragrance Education   : X posts
  Lifestyle/Occasions   : X posts
  Social Proof/Promos   : X posts

Excel: audit_reports/social_calendar_<timestamp>.xlsx

Tips:
- Schedule feed posts Tuesday–Friday, 7–9pm Lagos time (peak Nigerian Instagram hours)
- Reels/TikTok: post Thursday or Friday afternoon for weekend reach
- Stories: daily is fine — they expire in 24 hours and don't crowd the feed
- Batch-shoot product content once a week so you always have images ready
```

---

## Important rules

- Never invent product details — only use notes and facts confirmed from the product catalogue or descriptions
- If a product has no description yet, use only the product name, brand, and price — do not guess notes
- All prices in ₦ (Nigerian Naira)
- Geographic signal: Nigeria, Lagos, West Africa — not "across Africa"
- No more than 2 emojis per feed caption
- Stories and Reels can be more casual in tone than feed posts
- Always include one practical CTA per post (DM, link in bio, comment, save for later)
