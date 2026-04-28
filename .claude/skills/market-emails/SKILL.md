# Email Sequence Generation

Write complete, ready-to-send email sequences for Scentified's customer email channel. Sequences are grounded in real product data, Nigerian buyer psychology, and Scentified's luxury brand voice.

**Output:** Full email copy (subject line, preview text, body) for every email in the sequence — formatted for easy copy-paste into any ESP (Mailchimp, Klaviyo, Flodesk, etc.).

---

## Arguments

- `--sequence welcome`               → 4-email new subscriber welcome sequence
- `--sequence abandoned-cart`        → 3-email abandoned cart recovery sequence
- `--sequence new-arrivals`          → single announcement email for new products
- `--sequence vip`                   → 3-email VIP/loyalty sequence for repeat buyers
- `--sequence re-engagement`         → 3-email win-back sequence for inactive subscribers
- `--sequence launch --brand "Name"` → 3-email new brand launch sequence
- `--product "Name or ID"`           → single feature email for one specific product

---

## Brand Voice & Email Context

**Scentified's email tone:**
- Warm, knowledgeable, and personal — like a message from a trusted fragrance advisor
- Aspirational without being out of reach — the reader is either already a luxury buyer or aspiring to be
- Nigerian context throughout — Lagos lifestyle, local events, harmattan season, gifting culture
- Never pushy or salesy — lead with education and value, let the product speak

**Email rules:**
- Subject lines: under 50 characters (optimal for mobile preview)
- Preview text: 80–100 characters — extends the subject line, not a repeat of it
- Body length: 200–350 words per email — long enough to be substantive, short enough to read on a phone
- CTA buttons: one primary CTA per email, worded specifically (not just "Shop Now")
- Prices in ₦ (Nigerian Naira)
- Geographic: Nigeria, Lagos, West Africa — not "across Africa"
- Authenticity always mentioned — Scentified's core differentiator vs. the grey market

---

## Step 1 — Fetch product data (where relevant)

For sequences that feature specific products (`new-arrivals`, `launch`, `--product`):

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 10
```

Select the most relevant products for the sequence. Prioritise products with complete descriptions (have `<h3>` tags — these have the richest content to draw from).

If fetching fails or no argument requires product data, write the sequence with clear `[PRODUCT NAME]`, `[PRICE]`, `[KEY NOTES]` placeholders — explain to the user which fields to fill in before sending.

---

## Sequence: Welcome (--sequence welcome)

**Trigger:** New subscriber signs up to the mailing list.

**Goal:** Build trust, educate on Scentified's unique value (authenticity, curation, expertise), and get the first purchase.

**4-email sequence:**

### Email 1 — Sent immediately: Welcome
- Subject: Welcome to Scentified — [first name]
- Preview: Here's what makes us different.
- Content:
  - Warm welcome — who Scentified is, what they stand for
  - The authenticity promise (direct sourcing, no fakes)
  - Brief intro to what the email list gets: early access, fragrance education, exclusive offers
  - Light product tease — "Here's what's turning heads in Lagos right now"
  - CTA: "Browse the collection" → scentifiedperfume.com

### Email 2 — Sent Day 3: Fragrance Education
- Subject: How to find your signature scent
- Preview: Most people are wearing the wrong concentration.
- Content:
  - Educational: fragrance concentrations explained (EDP vs EDT vs Parfum)
  - Why this matters for the Nigerian climate (heat = EDP holds better)
  - 3 questions to discover your fragrance personality
  - Product recommendation tied to a "fragrance type" (e.g. "If you love something that announces your arrival...")
  - CTA: "Find your signature scent" → curated collection or quiz page

### Email 3 — Sent Day 7: Social Proof + Bestsellers
- Subject: What Lagos is wearing right now
- Preview: These 3 fragrances keep selling out.
- Content:
  - Lead with social proof framing (no need for actual reviews if not available)
  - Feature 3 bestsellers: name, key notes, price, 1-sentence description each
  - "Why people keep coming back" — 2–3 reasons (curation, authenticity, fast delivery)
  - CTA: "Shop bestsellers" → most popular products

### Email 4 — Sent Day 14: First-purchase nudge
- Subject: A note before you go
- Preview: Still looking for the right scent?
- Content:
  - Acknowledges they haven't bought yet — no pressure framing
  - Offer to help personally ("Reply to this email and tell us what you're looking for")
  - Feature one entry-level product (most accessible price point)
  - Reinforce the authenticity + delivery promise
  - CTA: "Let's find your scent" → contact or shop page

---

## Sequence: Abandoned Cart (--sequence abandoned-cart)

**Trigger:** Customer adds to cart but doesn't complete purchase.

**Goal:** Recover the sale — address objections without discounting immediately.

**3-email sequence:**

### Email 1 — Sent 1 hour after abandonment: Gentle reminder
- Subject: You left something behind
- Preview: Your [PRODUCT NAME] is still waiting.
- Content:
  - Keep it light — not accusatory
  - Remind them what they had in the cart (product name, key notes, price)
  - One reassurance: "Every bottle is 100% authentic and ships within [X] days"
  - CTA: "Complete your order" → direct link back to cart

### Email 2 — Sent 24 hours after abandonment: Handle objections
- Subject: Still thinking about it?
- Preview: Here's why thousands of Nigerians trust Scentified.
- Content:
  - Acknowledge that buying a luxury fragrance online is a considered decision
  - Address the top 3 objections: authenticity, delivery reliability, "will it suit me"
  - Offer: "Not sure about the scent? Reply to this email — describe what you like and we'll guide you"
  - CTA: "Order with confidence" → cart or product page

### Email 3 — Sent 72 hours after abandonment: Urgency / scarcity
- Subject: Last chance — stock is limited
- Preview: We can't hold [PRODUCT NAME] forever.
- Content:
  - Create urgency with genuine scarcity framing (niche perfumes genuinely do sell out)
  - Note: do NOT fabricate false urgency — use "we restock in limited quantities" framing
  - Feature the product one more time: bottle image (placeholder), notes, price
  - Optional: offer free gift wrapping or a sample with this order (only if Scentified offers this)
  - CTA: "Secure your bottle now" → cart

---

## Sequence: New Arrivals (--sequence new-arrivals)

**Trigger:** New products added to the store. Run this as a one-time broadcast.

**Goal:** Drive traffic and first purchases for newly listed products.

**Single email:**

- Subject: Just landed at Scentified — [Brand or Product Name]
- Preview: [Key note or brand claim in 10 words or fewer]
- Content:
  - Opening: set the scene — why this brand/product is special, what makes it worth attention
  - Feature 2–4 new products: name, key notes, concentration, price, 2-sentence description
  - Authenticity and sourcing note
  - CTA: "Shop new arrivals" → new arrivals page or specific product pages

Fetch the newest products via:
```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 10
```
Use products with the most recent IDs as the "new arrivals" for this email.

---

## Sequence: VIP (--sequence vip)

**Trigger:** Customer has made 2+ purchases. Segment: repeat buyers.

**Goal:** Deepen loyalty, make them feel recognised, encourage higher-value purchases.

**3-email sequence:**

### Email 1 — VIP recognition
- Subject: You're one of our best customers
- Preview: We see you — and we appreciate you.
- Content:
  - Personal, warm acknowledgement — they've bought before and Scentified values that
  - What VIP means: first access to new arrivals, personalised recommendations, priority support
  - Feature one high-value product they haven't bought (if data available — use `[PREMIUM PRODUCT]` placeholder)
  - CTA: "Explore your VIP picks" → curated collection

### Email 2 — Sent Day 7: Personalised recommendation
- Subject: Based on what you love...
- Preview: You might want to try this next.
- Content:
  - Introduce a complementary or "next step up" fragrance
  - Use fragrance family logic: if they bought a floral EDP, suggest a deeper floral or a contrast
  - Frame it as a personal recommendation, not a mass email
  - CTA: "Try [Recommended Product]" → product page

### Email 3 — Sent Day 21: Exclusive offer
- Subject: Something just for you
- Preview: A small thank-you from Scentified.
- Content:
  - Exclusive benefit — early access to a new arrival, complimentary gift wrapping, or a loyalty note
  - Note: do not promise discounts you can't deliver — use access/experience perks instead
  - Reiterate the authenticity and curation promise
  - CTA: "Shop before everyone else" → early access link or general shop

---

## Sequence: Re-engagement (--sequence re-engagement)

**Trigger:** Subscriber has not opened an email or visited the store in 90+ days.

**Goal:** Re-activate interest or clean the list.

**3-email sequence:**

### Email 1 — Gentle check-in
- Subject: Still interested in luxury fragrance?
- Preview: We've missed you — here's what's new.
- Content:
  - Light, no-pressure tone
  - What's new at Scentified since they last visited (new brands, new products, service improvements)
  - Feature 2 new or popular products briefly
  - CTA: "See what's new" → new arrivals or homepage

### Email 2 — Sent Day 5: Value reminder
- Subject: Why Scentified is different
- Preview: Real luxury. Real authenticity. Real delivery.
- Content:
  - Remind them of the core value proposition
  - Address the "I can find this cheaper elsewhere" objection with the authenticity angle
  - Feature one product at an accessible price point
  - CTA: "Come back and browse"

### Email 3 — Sent Day 10: Last email
- Subject: Should we stay in touch?
- Preview: We'll respect your decision either way.
- Content:
  - Honest: "If you're not interested anymore, no hard feelings — you can unsubscribe below"
  - But if they are interested: one last product feature + clear CTA
  - This honesty approach often re-engages better than aggressive sales emails
  - CTA: "Yes, keep me updated" → re-confirm subscription, or link to shop

---

## Sequence: Brand Launch (--sequence launch --brand "Name")

**Trigger:** Scentified adds a new brand to the catalogue.

**Goal:** Introduce the brand, build excitement, drive first purchases.

**3-email sequence:**

Fetch products for the brand:
```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 20
```
Filter for products matching the brand name. Use their descriptions and notes.

### Email 1 — Day 1: The announcement
- Subject: [Brand Name] has arrived at Scentified
- Preview: [Brand's defining characteristic in 10 words]
- Content:
  - Who the brand is: founding story, positioning, what makes it exceptional
  - Why Scentified chose to carry this brand
  - Feature 2–3 hero products with notes, prices, and 1-sentence descriptions
  - CTA: "Shop [Brand Name]" → brand category page

### Email 2 — Day 3: Education deep-dive
- Subject: The story behind [Brand Name]
- Preview: [Intriguing fact about the brand or its founder]
- Content:
  - Deeper brand education: founder, philosophy, signature olfactory style
  - Feature the brand's most distinctive or controversial fragrance
  - Customer framing: "This is for you if..."
  - CTA: "Find your [Brand] signature" → product listing

### Email 3 — Day 7: Urgency close
- Subject: [Brand Name] — first come, first served
- Preview: Niche brands restock on their own schedule.
- Content:
  - Scarcity is real for niche brands — reinforce this genuinely
  - Feature all available products in a compact grid format (name + price + 1 note)
  - Authenticity + delivery promise
  - CTA: "Order before it sells out"

---

## Step: Export

After writing any sequence, format the output clearly in this structure for every email:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL [N] of [TOTAL] — [Sequence Name]
Send timing: [Immediately / Day X after trigger]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUBJECT LINE: [subject — max 50 characters]
PREVIEW TEXT: [preview — 80–100 characters]

---

[Full email body — written as finished copy, not a brief]

---

PRIMARY CTA BUTTON TEXT: [button label]
CTA LINK: [URL or placeholder]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then save to `audit_reports/emails_<sequence>_<timestamp>.md` — a markdown file the user can open, review, and copy from directly.

---

## Final summary

```
=== EMAIL SEQUENCE COMPLETE ===

Sequence   : [name]
Emails     : [N] emails written
Products   : [products featured, or "none — add your own"]
Placeholders: [list any [PLACEHOLDER] fields that need filling before sending]

Saved to: audit_reports/emails_<sequence>_<timestamp>.md

Next steps:
1. Review copy and fill in any [PLACEHOLDER] fields
2. Add product images and links in your ESP
3. Load into Mailchimp / Klaviyo / Flodesk as an automation or campaign
4. Set the trigger condition as described in the sequence header
```

---

## Important rules

- Never fabricate reviews, testimonials, or social proof numbers
- Never promise discounts or free shipping unless Scentified has confirmed they offer it
- Never use false urgency ("only 2 left!") — use genuine scarcity framing only
- Authenticity must be mentioned in at least one email per sequence
- Geographic signal: Nigeria, Lagos, West Africa — not "across Africa"
- Prices always in ₦
- All CTAs must be specific — "Shop BTV Collection" beats "Shop Now"
- Subject lines must be under 50 characters — count exactly before finalising
