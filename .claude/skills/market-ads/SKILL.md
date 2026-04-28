# Ad Creative & Copy Generation

Generate complete, ready-to-run ad campaigns for scentifiedperfume.com across Meta (Facebook + Instagram) and Google. Every ad is grounded in real products from the WooCommerce catalogue, Nigerian buyer psychology, and the luxury perfume market.

**Output:** Complete ad copy with all variations, audience targeting, budget guidance, and creative direction — saved to `audit_reports/ad-campaigns_<timestamp>.md`.

---

## Arguments

- No args                         → full campaign brief: Meta + Google ads for the store overall
- `--product "Name or ID"`        → ad set for one specific product
- `--brand "Name"`                → campaign for all products from one brand (e.g. "BTV", "Clive Christian")
- `--platform meta`               → Meta (Facebook + Instagram) only
- `--platform google`             → Google Search + Performance Max only
- `--retargeting`                 → retargeting ad sequences only (for warm audiences)
- `--new-arrivals`                → ads announcing new products to the catalogue

---

## Business Context: Scentified

Before writing any ads, internalise this context — it must inform every ad:

**What Scentified is:** West Africa's destination for luxury and niche perfumery. Ships to Nigeria, Ghana, and partner countries across West Africa.

**Primary audience:**
- Nigerian professionals, 25–45, Lagos-based or other major cities
- Household income: upper-middle to high (can spend ₦150,000–₦2,000,000 on a fragrance)
- Already interested in luxury lifestyle — fashion, watches, cars, travel
- Secondary: gift buyers (birthdays, weddings, Owambe events, Valentine's Day, corporate gifts)

**Core buying objections to address in every campaign:**
1. "Is it authentic?" — Nigerian buyers deeply distrust fakes. Authenticity is the #1 purchase barrier.
2. "Will delivery actually work?" — Scepticism about Nigerian e-commerce delivery
3. "Can I smell it first?" — Can't try before buying online

**Unique selling propositions:**
- 100% authentic, directly sourced (not grey market)
- Niche and luxury brands not easily found in Nigeria elsewhere
- Fast, reliable delivery to Lagos and major Nigerian cities
- Knowledgeable team that can guide fragrance selection

**Tone:** Luxury but grounded. Aspirational but Nigerian. Never condescending. Use ₦ (Naira) for prices.

---

## Step 1 — Fetch products to feature (if needed)

For `--product`, `--brand`, or `--new-arrivals`:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py tools/fetch_no_desc.py --all --limit 20
```

Select the most relevant products. Prioritise those with complete descriptions (they have the richest copy to draw from). If no product is specified, select 3 flagship products across different price tiers for the general campaign.

---

## Step 2 — Meta Ads (Facebook + Instagram)

### Audience Targeting

Define three audience tiers:

**Cold Audience (new reach):**
- Location: Nigeria (Lagos, Abuja, Port Harcourt primary; other cities secondary)
- Age: 25–45
- Interests: Luxury goods, fragrance, international fashion brands, high-end lifestyle, travel
- Behaviours: Online shoppers, luxury brand engagers
- Income signals: Engaged shoppers, luxury lifestyle interests

**Warm Audience (retargeting):**
- Website visitors (last 30 days)
- Instagram/Facebook page engagers (last 60 days)
- Video viewers (watched 50%+ of any video)

**Lookalike:**
- 1–2% lookalike of purchasers or email list (if data available)
- Based on: Nigeria

### Ad Formats to Generate

For each product or campaign, write copy for:
1. **Single Image Feed Ad** — hero product shot
2. **Carousel Ad** — 3–4 cards (product, notes, brand story, CTA)
3. **Instagram Story Ad** — vertical, 15-second format
4. **Reels/Video Ad** — script for 15–30 second video

### Copy Template per Ad

For each ad, provide:
- **Primary text** (3 variations: short 1–2 lines, medium 3–4 lines, long 5–7 lines)
- **Headline** (5 variations — 40 characters max)
- **Description** (30 characters — appears below headline)
- **CTA button** (choose from: Shop Now, Learn More, Order Now, Contact Us, Send Message)
- **Visual direction** (describe what the image/video should show)

### Copy Angles — write at least 5 per campaign

Use these angles, adapted for the Nigerian luxury perfume buyer:

**Angle 1 — Authenticity (highest priority)**
```
Headline: "100% Authentic. Delivered to Lagos."
Primary: You shouldn't have to wonder if your perfume is real.
Every bottle at Scentified is sourced directly — not from the grey market,
not from an unknown supplier. Guaranteed authentic. Delivered fast.
[Product Name] from [Brand] — now available in Nigeria.
CTA: Order Now
```

**Angle 2 — Scarcity / Exclusivity**
```
Headline: "Not easy to find in Nigeria"
Primary: [Brand] doesn't sell through just anyone.
That's exactly why we went directly to the source.
[Product Name] — one of the world's finest fragrances, now in Lagos.
Stock is limited. Order yours before it sells out.
CTA: Shop Now
```

**Angle 3 — Gifting**
```
Headline: "The gift that tells them everything"
Primary: Some gifts say "I thought of you."
This one says "I know you."
[Product Name] by [Brand] — authentic luxury fragrance, gift-wrapped and
delivered anywhere in Nigeria within [X] days.
Because some moments deserve more than a voucher.
CTA: Order Now
```

**Angle 4 — Sensory / Product Story**
```
Headline: "[Key note] meets [key note]"
Primary: [Product Name] opens with [top note].
Then [heart note] settles in — [brief evocative description].
[Base note] anchors everything for [X–Y hours].
An EDP for people who know what they want.
Authentic [Brand], delivered in Nigeria. Link in bio.
CTA: Learn More
```

**Angle 5 — Social Proof / Credibility**
```
Headline: "West Africa's finest fragrance store"
Primary: Thousands of Nigerians trust Scentified for one reason:
every fragrance is exactly what it claims to be.
No fakes. No compromises. Just the real thing.
Browse [Brand] fragrances — delivered to your door.
CTA: Shop Now
```

**Angle 6 — Price Anchoring (for high-value products)**
```
Headline: "Worth every Naira"
Primary: [Product Name] costs ₦[price].
Here's what you're paying for: [X years] of brand heritage.
[X–Y hours] of longevity. Notes of [key notes].
And the knowledge that what you're wearing is 100% real.
Some things are worth it.
CTA: Order Now
```

**Angle 7 — Occasion / Lifestyle**
```
Headline: "Dress it. Then scent it."
Primary: You've sorted the Agbada. The shoes are done.
Now the finishing touch — the one people remember after you've left the room.
[Product Name] by [Brand]. Owambe-ready. Office-ready. You-ready.
₦[price]. Authentic. Delivered in Nigeria.
CTA: Shop Now
```

### Carousel Card Structure

For a 4-card carousel:
- **Card 1:** Product hero shot — product name, brand, headline
- **Card 2:** Key fragrance notes — top/heart/base as simple visual list
- **Card 3:** Brand story — 1 sentence on the brand's heritage and why it matters
- **Card 4:** CTA — "Authentic. Sourced directly. Delivered in Nigeria." + Shop Now

### Story Ad Structure (5 seconds per frame, 3 frames)

```
Frame 1: Product close-up + brand name (2 seconds)
Frame 2: 2-3 key notes + "X–Y hours longevity" (2 seconds)
Frame 3: "100% Authentic. Order at scentifiedperfume.com" (1 second)
Overlay text throughout: product name + price in ₦
```

---

## Step 3 — Google Ads

### Campaign Type: Search Ads

**Target keywords (adapt per product/brand):**

High-intent Nigerian buyers:
- `buy [brand] perfume Nigeria`
- `[brand] [product] EDP Lagos`
- `[brand] perfume price Nigeria`
- `authentic [brand] fragrance Nigeria`
- `niche perfume Nigeria`
- `luxury perfume Lagos`
- `[brand] perfume where to buy Nigeria`

**Ad structure — Responsive Search Ad:**

Generate at least 10 headlines (30 characters each) covering:
- Brand + product name
- "Authentic" signal
- Nigeria/Lagos delivery
- Price signal (e.g. "From ₦[price]")
- Niche/luxury positioning
- Speed of delivery
- CTA ("Order Today", "Shop Now", "Get Yours")

Generate 4 descriptions (90 characters each) covering:
- Authenticity + sourcing promise
- Delivery speed and coverage
- Product notes or brand heritage
- Trust + risk reduction ("Every bottle guaranteed authentic")

**Negative keywords:**
- free, cheap, discount, fake, replica, imitation, smell like, dupe, alternative, similar to
- (these attract the wrong buyer for a luxury brand)

### Campaign Type: Performance Max

**Asset group:** Provide per brand or product:
- 5 short headlines (30 chars)
- 5 long headlines (90 chars)
- 5 descriptions (90 chars)
- Image specs: 1200×1200 (square), 1200×628 (landscape)
- Video concept: 15–30 second script

**Audience signals:**
- Custom intent: people who searched for the brand or product
- In-market: luxury goods, fragrance
- Customer list (email subscribers if available)

---

## Step 4 — Budget Allocation

Recommend budget split based on Scentified's e-commerce model:

| Platform | % of Budget | Rationale |
|---|---|---|
| Meta (Instagram primary) | 55% | Nigerian luxury buyers discover on Instagram first |
| Google Search | 30% | Captures high-intent "buy [brand] Nigeria" searches |
| Google Performance Max | 15% | Retargeting and discovery via Shopping / YouTube |

**Minimum viable budget:** ₦150,000/month (≈$100) to get meaningful data
**Recommended budget:** ₦750,000–₦1,500,000/month for real scale

**Funnel allocation:**
- Cold (awareness + discovery): 40%
- Warm (retargeting): 35%
- Hot (abandoned cart, direct intent): 25%

---

## Step 5 — Retargeting Sequences

Three-stage sequence for Nigerian buyers (who often need more touchpoints before a high-value luxury purchase):

**Stage 1 — Visited product page, did not add to cart (Days 1–3):**
Lead with the sensory/story angle. Not pushy. Remind them of the product.

**Stage 2 — Added to cart, did not purchase (Days 1–7):**
Lead with authenticity + delivery confidence. Address the "is it real?" objection directly.

**Stage 3 — Purchased once — upsell / cross-sell (Days 14–30):**
"You chose well. Here's what people who love [purchased product] also wear." Feature 2–3 complementary products from the same brand or fragrance family.

---

## Step 6 — Creative Brief for Visual Production

For each campaign, provide a one-paragraph brief for the designer or photographer:

```
PRODUCT: [Product Name] by [Brand]
SHOT TYPE: [Flat lay / Studio / Lifestyle / Close-up]
BACKGROUND: [Clean white / Dark luxury / Natural setting]
PROPS: [Flowers matching key notes / Nothing / Fabric / Nigerian lifestyle context]
LIGHTING: [Hard shadows = bold/masculine | Soft diffused = feminine/floral]
COLOUR PALETTE: [Based on bottle colour and brand aesthetic]
TEXT OVERLAY: [Product name | Brand | Price in ₦]
FEEL: [Aspirational but grounded. Nigerian luxury. Not European catalogue.]
```

---

## Step 7 — Output

Save the complete campaign to `audit_reports/ad-campaigns_<timestamp>.md`.

Print this summary:

```
=== AD CAMPAIGNS GENERATED ===

Campaign: [Product/Brand/Store — specify]
Platforms: Meta + Google
Total ad variations: [count]

Meta:
  Cold audience ads    : [X] variations across [X] angles
  Retargeting ads      : [X] variations
  Story/Reels scripts  : [X]
  Carousel sets        : [X]

Google:
  Search ad headlines  : [X]
  Descriptions         : [X]
  Performance Max sets : [X]

Budget recommendation: ₦[X]/month
  Meta: ₦[X] | Google Search: ₦[X] | P.Max: ₦[X]

Saved to: audit_reports/ad-campaigns_<timestamp>.md
```

---

## Important Rules

- All prices in ₦ (Nigerian Naira) — never USD
- Geographic: Nigeria, Lagos, West Africa — never "across Africa"
- Authenticity must appear in at least one ad per campaign — it is the #1 objection
- Never fabricate reviews, star ratings, or customer numbers
- Never use false urgency ("only 2 left") — use genuine scarcity ("niche brands restock on their own schedule")
- Instagram is the primary discovery channel for this audience — prioritise Instagram placements
- All copy must pass the "would a Lagos professional share this?" test — nothing embarrassing or tacky
- Do not use: "Introducing", "Experience the", "Elevate your", "Indulge in" — these are overused luxury clichés
