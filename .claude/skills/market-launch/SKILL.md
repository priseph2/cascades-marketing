# Product/Brand Launch Playbook Generator

Generate a complete, actionable launch playbook for Scentified when adding a new brand, a new product line, or running a major seasonal campaign. Produces a week-by-week plan with email sequences, social content, ad copy briefs, and a day-of checklist — everything needed to make a new arrival land properly in the Nigerian market.

**Output:** `audit_reports/LAUNCH-PLAYBOOK-<brand-or-product>.md`

---

## Arguments

- `--brand "Name"`          → full launch playbook for onboarding a new brand (e.g. "Fragrance du Bois")
- `--product "Name"`        → launch playbook for a hero product (single fragrance spotlight)
- `--seasonal "Campaign"`   → playbook for a seasonal campaign (e.g. "Valentine's Day", "Eid", "Christmas")
- `--restock "Brand"`       → quick restock announcement plan (2-week mini-campaign)

If no argument is provided, ask: "What are you launching? A new brand, a specific product, or a seasonal campaign?"

---

## Business Context

Every launch playbook must account for Scentified's specific situation:

- **Market:** Nigeria primarily, Ghana secondary, West Africa broadly
- **Audience:** Lagos professionals, 25–45, upper-middle to high income
- **Core objection to overcome at launch:** "Is this real? Is this available in Nigeria?"
- **Key channels:** Instagram (primary discovery), Email (conversion), Google Search (high-intent)
- **No Product Hunt. No press releases to tech media.** This is luxury retail, not a startup.
- **Nigerian launch timing:** Avoid major religious holidays for initial push. Best launch days: Tuesday–Thursday.
- **Currency:** ₦ (Nigerian Naira) throughout

---

## Step 1 — Gather Launch Context

Before building the playbook, collect or confirm these details:

**For brand launch:**
1. Brand name and country of origin
2. Number of products being listed at launch
3. Price range (lowest to highest SKU)
4. Brand's existing global reputation (niche, established luxury, ultra-premium?)
5. Any exclusivity arrangement? (Is Scentified the only Nigerian stockist?)
6. Target launch date (or "as soon as possible")
7. Available assets: product images? brand press kit? official brand copy?

**For product launch:**
1. Product name and brand
2. Key notes (top/heart/base)
3. Concentration and bottle size
4. Price in ₦
5. What makes it worth a dedicated campaign (rarity, demand, occasion-fit)?

**For seasonal campaign:**
1. Which occasion? (Valentine's Day, Eid al-Fitr, Eid al-Adha, Christmas, New Year, Mother's Day, Father's Day)
2. Products to feature (ask user, or fetch from WooCommerce)
3. Any offer or incentive? (gift wrapping, complimentary sample, free delivery threshold)

Fetch existing product data if needed:
```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 30
```

---

## Step 2 — Positioning Statement

Draft the launch positioning before anything else:

```
For [Nigerian fragrance buyer] who [wants genuine luxury they can trust],
[Brand/Product] at Scentified is [the only place in Nigeria to get it authentically].
Unlike [grey market sellers or generic retailers],
Scentified [sources directly and guarantees every bottle is 100% real].
```

Adapt this into the launch narrative — the single through-line that all launch content will reference.

---

## Step 3 — Launch Playbook by Type

### BRAND LAUNCH (--brand)

#### Week 1–2: Foundation & Content Creation

**Tasks:**
- [ ] Ensure all products are listed in WooCommerce with complete descriptions (run `/product-descriptions --brand "Name"` if not done)
- [ ] Ensure all products have SEO titles and meta descriptions (run `/seo-gaps --brand "Name"` if not done)
- [ ] Confirm all product images are uploaded and high quality
- [ ] Draft the brand story (2–3 paragraphs on heritage, founding, what makes them exceptional)
- [ ] Create the brand-level Instagram highlight cover
- [ ] Write the Instagram bio update (if adding the brand to the featured list)
- [ ] Build the brand launch email sequence (see Email Templates below)
- [ ] Schedule 7 days of launch social content (see Social Content below)
- [ ] Brief any photographer/videographer if product shoots are needed
- [ ] Identify the 3 hero products — the ones to lead with in all launch communications

**Deliverables by end of Week 2:**
- All products live on the site with descriptions and SEO
- Launch email sequence ready to activate
- 7 days of social content scheduled or drafted
- Hero products identified

#### Week 3: Teaser Phase

**Goal:** Build awareness and curiosity before the official announcement.

**Social content (3 posts):**

*Post 1 (Day 15):*
- Type: Feed post — close-up product shot, no text on image
- Caption: "[Brand name] is coming to Scentified. That's all we'll say for now."
- No price, no link. Pure intrigue.

*Post 2 (Day 17):*
- Type: Story — poll
- Text: "Can you name this fragrance house?"
- Show the brand logo (partially obscured) or a signature note
- Poll options: "[Brand name]" / "Guess below ↓"

*Post 3 (Day 19):*
- Type: Feed — brand heritage teaser
- Caption: "Founded in [year]. Worn by [type of person, not celebrity names unless confirmed]. Now available in Lagos for the first time."
- End with: "Launch this [day/week]. Follow to be first."

**Email (1 teaser):**
- Subject: "Something rare is coming to Scentified"
- Preview: "You'll want to be first."
- Body: Tease the brand without fully revealing it. 100–120 words. One CTA: "Stay tuned."

#### Week 4: Launch Week

**Monday — VIP/Early Access:**
- Send launch email to most engaged subscribers first
- Post on Instagram: Full product reveal
- Caption: "It's here. [Brand name] — now available in Nigeria. Authentic. Sourced directly. Limited stock." + product list with prices in ₦

**Tuesday — Main Announcement:**
- Send full list launch email
- Instagram Stories: Swipe through all products with prices
- Consider a Reel: unboxing or brand introduction

**Wednesday — Education:**
- Feed post: Brand story — who founded it, what makes it different, why Scentified chose to carry it
- Stories: Q&A or "ask us about [brand]" sticker

**Thursday — Product Spotlight:**
- Deep-dive on the #1 hero product
- Full caption: notes, performance, who it's for, price

**Friday — Social Proof / Scarcity:**
- "First orders have gone out."
- "Niche brands like [Brand] restock on their own schedule. Once this batch is gone, we don't know when the next arrives."
- CTA: Order while stock lasts

---

### PRODUCT LAUNCH (--product)

A focused 2-week campaign for a single hero product.

#### Week 1: Build

**Day 1 — Announce:**
- Feed post: Product hero shot
- Caption: Lead with the most evocative note. Who this fragrance is for. Price. Authenticity signal. CTA.

**Day 3 — Education:**
- Fragrance breakdown post: Top notes, heart notes, base notes. Performance (longevity/projection). Concentration.

**Day 5 — Brand Context:**
- Post about the brand behind the fragrance. Why it matters. Global reputation.

**Day 7 — Story:**
- Instagram Stories: 5-frame sequence (product, notes, performance, occasion, order CTA)

#### Week 2: Convert

**Day 8 — Lifestyle:**
- "This is for the [occasion]. The [type of person]." Evocative, specific.

**Day 10 — Objection Handling:**
- "We know buying fragrance online is a leap of faith." Address authenticity, delivery, and "what if I don't like it?"

**Day 12 — Urgency:**
- Limited quantity angle. "When it's gone, it's gone."

**Email sequence:** 3 emails over 10 days (announcement, education, urgency close)

---

### SEASONAL CAMPAIGN (--seasonal)

Build around the Nigerian calendar — occasions where gifting and personal luxury purchasing spike:

| Occasion | Launch prep start | Key angle |
|---|---|---|
| Valentine's Day (Feb 14) | Jan 20 | Gifting — "the gift that says everything" |
| Mother's Day (second Sunday, May) | April 20 | Appreciation — "for the woman who deserves the real thing" |
| Eid al-Fitr (date varies) | 3 weeks before | Celebration — new beginnings, special occasions |
| Father's Day (third Sunday, June) | June 1 | Gifting for men — confidence, sophistication |
| Eid al-Adha (date varies) | 3 weeks before | Same as Eid al-Fitr |
| Christmas (Dec 25) | Dec 1 | Gifting season — gift guides, bundles |
| New Year (Jan 1) | Dec 26 | New chapter — "start the year with your signature scent" |

**Seasonal campaign structure (3 weeks):**
- **Week 1:** Awareness — "The occasion is coming. Here's what to consider."
- **Week 2:** Product showcase — gift guide format. Feature 3–5 products at different price tiers.
- **Week 3:** Urgency — delivery deadline. "Order by [date] to receive before [occasion]."

**Seasonal email sequence:** 4 emails (awareness, product showcase, delivery deadline warning, last chance)

---

### RESTOCK ANNOUNCEMENT (--restock)

A quick 2-week mini-campaign for when a popular brand or product comes back in stock.

**Day 1 (Announcement):**
- Feed: "[Brand] is back."
- Simple. Confident. Product image. Price. Link.
- Email: Subject: "[Brand] is back in stock" — one email, no sequence needed.

**Day 3:**
- Stories: Products with prices. Swipe to shop.

**Day 7:**
- "Last chance" if stock is genuinely running low. Use only if true.

---

## Step 4 — Email Templates

### Brand Launch Sequence (4 emails)

**Email 1 — Teaser (1 week before launch)**
- Subject: Something rare is coming to Scentified (under 50 chars)
- Preview: You'll want to be first.
- Body: Hint at the brand — its reputation, what makes it special — without naming it yet. 100 words. CTA: "Stay tuned — follow us for the reveal."

**Email 2 — The Reveal (Launch Day)**
- Subject: [Brand name] is now at Scentified
- Preview: Authentic. Directly sourced. Delivered in Nigeria.
- Body: Brand introduction (2 sentences). List hero products with names and prices. Authenticity and delivery promise. CTA: "Shop [Brand] now →"

**Email 3 — Education (Day 3)**
- Subject: The story behind [Brand name]
- Preview: Founded in [year]. Here's what makes them different.
- Body: Brand heritage in 150 words. Feature one product in depth (notes, performance, who it's for). CTA: "Try [hero product] →"

**Email 4 — Urgency (Day 7)**
- Subject: [Brand] — first come, first served
- Preview: Niche brands restock on their own schedule.
- Body: Scarcity is real (niche brands genuinely have limited production). Feature all available products in compact list format (name + ₦price). Delivery promise. CTA: "Order before it sells out →"

---

## Step 5 — Social Content Calendar

Produce a full social content table for the launch period:

| Day | Platform | Post Type | Content Summary | Caption Hook |
|---|---|---|---|---|
| [Day] | Instagram Feed | Product hero | [describe] | [first line of caption] |
| [Day] | Instagram Story | [type] | [describe] | [frame 1 text] |
| [Day] | Reels/TikTok | [video concept] | [describe] | [opening line / text overlay] |

Include at least:
- 5 Instagram feed posts
- 3 Instagram Story sequences (5 frames each)
- 2 Reels/TikTok video concepts (with script outline)

---

## Step 6 — Launch Day Checklist

```
LAUNCH DAY CHECKLIST — [Brand/Product Name]

Pre-launch (night before):
  [ ] All products live and purchasable on site
  [ ] All product descriptions complete and QA passed
  [ ] All product images uploaded
  [ ] Launch email scheduled in ESP (correct send time)
  [ ] Launch social posts scheduled or ready to post manually
  [ ] WhatsApp/DM auto-response updated to mention new brand

Launch day:
  [ ] Send launch email (if not scheduled)
  [ ] Post feed announcement (7–9pm Lagos time for best reach)
  [ ] Post Stories sequence
  [ ] Monitor DMs and comments — respond within 1 hour on launch day
  [ ] Check site is loading and products are in stock

Post-launch (Days 2–7):
  [ ] Send education email (Day 3)
  [ ] Post brand story content (Day 3)
  [ ] Post product spotlight (Day 4–5)
  [ ] Monitor orders and update stock count
  [ ] Send urgency email if stock running low (Day 7)
```

---

## Output

Save the complete playbook to `audit_reports/LAUNCH-PLAYBOOK-<name>-<timestamp>.md`.

Print this summary:

```
=== LAUNCH PLAYBOOK COMPLETE ===

Launch type   : [Brand / Product / Seasonal / Restock]
Subject       : [name]
Launch date   : [date or "TBD"]

Plan summary:
  Pre-launch weeks  : [X weeks of prep]
  Launch week       : [Day-by-day breakdown]
  Post-launch       : [Week 2+ activities]

Content produced:
  Emails            : [X] (see playbook for full copy)
  Feed posts        : [X]
  Story sequences   : [X]
  Reels scripts     : [X]
  Checklist items   : [X]

Saved to: audit_reports/LAUNCH-PLAYBOOK-<name>-<timestamp>.md

Recommended pre-launch steps:
  1. /product-descriptions --brand "[name]" — ensure all products have descriptions
  2. /seo-gaps --brand "[name]" — ensure all products have SEO titles
  3. /market-ads --brand "[name]" — generate paid ad copy for the launch
```

---

## Important Rules

- All prices in ₦ (Nigerian Naira)
- Geographic: Nigeria, Lagos, West Africa — never "across Africa"
- Launch timing: Tuesday–Thursday for main announcements (avoid Mondays and Fridays for high-value launches)
- Never fabricate early customer results or testimonials
- Never use false urgency — only use scarcity language if the product genuinely has limited stock (niche brands almost always do)
- Every launch plan must include the authenticity signal at least once in every email and the main social announcement
- Descriptions used in launch copy must match what's on the actual product page — no separate copy that contradicts the listing
