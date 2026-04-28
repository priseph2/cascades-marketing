# Brand Voice Analysis and Guidelines Generation

Analyse Scentified's brand voice across all available channels — website, product descriptions, social media, and any other copy — and produce a definitive brand voice guidelines document that any writer, freelancer, or team member can use to write consistently on-brand.

**Output:** `audit_reports/BRAND-VOICE.md` — a complete, actionable brand voice guide specific to Scentified.

---

## Arguments

- No args        → full brand voice analysis and guidelines document
- `--quick`      → condensed version: voice summary, do's/don'ts, and copy samples only (no competitor comparison)
- `--compare`    → include competitor voice analysis (compares Scentified against 3 Nigerian/African luxury retailers)

---

## Business Context

**Scentified** is West Africa's destination for luxury and niche perfumery. Operates primarily in Nigeria and Ghana. Sells brands including BTV (Boadicea the Victorious), Clive Christian, Spirit of Dubai, Essential Parfums, Fragrance du Bois, Strangelove NYC, and others.

**Price range:** ₦150,000–₦2,000,000+ per bottle.

**Target customer:** Nigerian professional, 25–45, Lagos-based or other major cities, upper-middle to high income, interested in genuine luxury (not status symbols for their own sake).

**Core differentiator:** Authenticity and curation. Scentified carries brands that are genuinely hard to find in Nigeria and guarantees every bottle is directly sourced.

---

## Step 1 — Gather Source Material

Fetch and analyse Scentified's existing copy from these sources in order:

**Primary (must analyse):**

1. **Homepage** — fetch `https://scentifiedperfume.com/`
   Extract: tagline, hero copy, brand promise, navigation labels, CTA text

2. **About page** — fetch `https://scentifiedperfume.com/about/` (or similar)
   Extract: origin story, mission statement, how they describe themselves

3. **Product descriptions** — read `tools/descriptions_staging.json` if it exists and has entries
   Extract: 5–10 product descriptions that are marked `qa_passed: true` — these represent the current written voice

4. **Product category pages** — fetch `https://scentifiedperfume.com/product-category/` (or similar)
   Extract: any copy on category landing pages

**Secondary (analyse if accessible):**

5. **Instagram bio and recent posts** — `WebSearch`: `Scentified perfume Nigeria Instagram`
   Extract: bio text, caption style, hashtag approach, tone

6. **Google/Facebook ad copy** — `WebSearch`: `Scentified perfume Nigeria ad`
   Extract: any visible ad copy and headlines

If any URL returns 403 or is unreachable, note it and continue with available sources.

---

## Step 2 — Voice Dimension Analysis

Score Scentified's voice along four spectrums. Provide 3 specific quoted examples from the source material for each.

### Formal ←————→ Casual (1=formal, 10=casual)

| Signal | What to look for in Scentified's copy |
|---|---|
| Contractions | Do they use "it's", "you'll", "we're"? |
| Sentence length | Long, structured sentences vs short punchy ones |
| Pronouns | Do they address the reader directly ("you") or speak in third person? |
| Vocabulary | Elevated/sophisticated vs everyday words |

### Serious ←————→ Playful (1=serious, 10=playful)

| Signal | What to look for |
|---|---|
| Levity | Any humour, wordplay, or lightness? |
| Exclamation use | How often? |
| Metaphor creativity | Predictable comparisons vs unexpected ones |

### Technical ←————→ Simple (1=technical, 10=simple)

| Signal | What to look for |
|---|---|
| Fragrance jargon | Do they explain "sillage", "EDP", "base notes" — or assume the reader knows? |
| Detail depth | In-depth note breakdowns vs high-level impressions |
| Audience assumption | Expert perfume collector vs curious first-time luxury buyer |

### Reserved ←————→ Bold (1=reserved, 10=bold)

| Signal | What to look for |
|---|---|
| Claims | Hedged ("one of the finest") vs direct ("the finest") |
| Nigerian market confidence | Do they lean into their market leadership or stay humble? |
| Competitive stance | Do they mention the grey market / fake perfume problem directly? |

---

## Step 3 — Brand Archetype

Map Scentified to the most fitting archetype from these five:

| Archetype | Characteristics | Fit for Scentified? |
|---|---|---|
| **The Authority** | Expert, trustworthy, educational, data-driven | High — they know perfume better than anyone in the market |
| **The Guide** | Knowledgeable, supportive, clear, methodical | High — they guide buyers to the right fragrance |
| **The Rebel** | Bold, challenges conventions, opinionated | Medium — they challenge fake perfume norms |
| **The Friend** | Warm, approachable, relatable, encouraging | Medium — luxury but not cold |
| **The Innovator** | Forward-thinking, visionary, disruptive | Low |

Identify the primary archetype and, if applicable, a secondary one. Explain the evidence.

---

## Step 4 — Vocabulary Analysis

Extract from all analysed sources:

**Words Scentified uses frequently:**
Organise by type:
- Action words (verbs they favour)
- Descriptive words (adjectives that recur)
- Value words (words reflecting what they stand for)
- Fragrance-specific language (how they talk about notes, performance, longevity)

**Words they avoid or that feel off-brand:**
- Words too casual for their positioning
- Words that belong to a mass-market fragrance retailer (not Scentified)
- Clichés that appear in competitor copy

**Signature phrases:**
- Any recurring patterns (e.g. "sourced directly", "authentic", "West Africa")
- Linguistic patterns (do they start sentences with verbs? Use dashes? Favour short paragraphs?)

---

## Step 5 — Tone Mapping by Context

Map how Scentified's tone should shift across different contexts (even if current copy is inconsistent — this section recommends the right tone per context):

| Context | Recommended Tone | Example |
|---|---|---|
| Product description | Sensory, specific, confident | Details notes, performance, occasion — no fluff |
| Homepage hero | Aspirational, bold, welcoming | Captures the store's identity in one breath |
| Instagram caption | Warm, evocative, community-minded | Speaks to the reader, not at them |
| Email subject line | Curious or direct, never clickbait | Earns the open, delivers the promise |
| Meta ad copy | Direct, benefit-led, authentic-first | Addresses the authenticity objection early |
| Google ad headline | Keyword-anchored, Nigerian-intent | "Buy [Brand] Perfume Nigeria" approach |
| Customer reply / DM | Warm, knowledgeable, human | Like a trusted friend who knows fragrance |
| Error/policy message | Clear, professional, warm | Not robotic, not over-apologetic |

---

## Step 6 — Competitor Voice Comparison (if `--compare` passed)

Compare Scentified's voice against 3 Nigerian or African luxury/lifestyle retailers:

`WebSearch`: `luxury perfume store Nigeria` — identify 2–3 active competitors
`WebFetch` their homepages and about pages

**Voice Comparison Matrix:**

| Dimension | Scentified | Competitor 1 | Competitor 2 | Competitor 3 |
|---|---|---|---|---|
| Formal / Casual | X/10 | X/10 | X/10 | X/10 |
| Serious / Playful | X/10 | X/10 | X/10 | X/10 |
| Technical / Simple | X/10 | X/10 | X/10 | X/10 |
| Reserved / Bold | X/10 | X/10 | X/10 | X/10 |
| Primary Archetype | — | — | — | — |

**Differentiation assessment:**
- Where is the voice white space in this market?
- What tone territory is unoccupied that Scentified could own?

---

## Step 7 — Brand Voice Chart

Produce the definitive Scentified voice chart:

```
SCENTIFIED'S VOICE IS:              SCENTIFIED'S VOICE IS NOT:
────────────────────────────────────────────────────────────────
Knowledgeable                       Condescending
Aspirational                        Unattainable
Warm                                Salesy
Confident                           Arrogant
Authentic                           Boastful
Grounded in Nigerian reality        Pretending to be European
Sensory and evocative               Vague and generic
```

(Adapt based on the actual analysis — do not use this verbatim if the source material shows something different.)

---

## Step 8 — Writing Guidelines

**DO:**
- Lead with the sensory experience, then the product details
- Use second person — address the reader as "you" throughout
- Name specific fragrance notes rather than saying "a floral scent"
- Include a geographic signal (Nigeria, Lagos, West Africa) in product copy and ads
- Use "authentic" and "directly sourced" — these are credibility anchors for Nigerian buyers
- Write short paragraphs (2–3 lines maximum) — the audience reads on mobile
- Use specific occasions when recommending fragrances (Owambe, office, date night, travel)
- Frame price as investment, not cost

**DON'T:**
- Open with "Introducing", "Experience", "Elevate your", or "Indulge in" — these are overused
- Write generic luxury copy that could apply to any perfume retailer anywhere in the world
- Use "across Africa" or "across the continent" — Scentified operates in Nigeria, Ghana, and West Africa specifically
- Use passive voice in headlines or CTAs
- Make claims about fragrances that aren't grounded in actual research (don't invent notes)
- Write for a European or American audience — write for Lagos professionals
- Use more than 2 emojis in any single piece of written content
- Promise free shipping, discounts, or offers that Scentified doesn't actually provide

---

## Step 9 — Brand Messaging Hierarchy

Document Scentified's core messages from most distilled to most expanded:

**Tagline (under 10 words):**
Assess the current tagline if one exists. Suggest an alternative if it doesn't capture the brand well.

**Value Propositions (1 sentence each, 3–5 props):**
1. Authenticity: [sentence]
2. Curation: [sentence]
3. Market access: [sentence]
4. Expertise: [sentence]
5. Delivery/reliability: [sentence]

**Elevator Pitch (75 words):**
A conversational explanation of what Scentified is and why it matters — specifically for someone in Lagos who has never heard of it.

**Boilerplate (100–150 words):**
Standard "about Scentified" paragraph for use in press materials, email footers, and bio sections.

---

## Step 10 — Copy Samples in Scentified's Voice

Provide 8 ready-to-use copy samples that demonstrate the voice across different contexts:

1. **Homepage headline** (under 12 words)
2. **Homepage subheadline** (under 25 words)
3. **Product description opening paragraph** (2–3 sentences, for a fictional flagship fragrance)
4. **Instagram feed caption** (with hook, body, CTA, and hashtags)
5. **Email subject line** (for a "new arrivals" announcement)
6. **Meta ad primary text** (medium length — 3–4 sentences)
7. **Google Search ad headline** (30 characters)
8. **Customer DM response** (when someone asks "is this perfume original?")

---

## Output

Save to `audit_reports/BRAND-VOICE.md`.

Print this summary:

```
=== BRAND VOICE GUIDELINES COMPLETE ===

Analysis sources: [list what was successfully fetched]

Voice dimensions:
  Formal / Casual      : [X]/10
  Serious / Playful    : [X]/10
  Technical / Simple   : [X]/10
  Reserved / Bold      : [X]/10

Primary archetype: [name]
Overall consistency: [X]/10

Key findings:
  [1 sentence on what's working well]
  [1 sentence on the biggest consistency gap]
  [1 sentence on the biggest differentiation opportunity]

Saved to: audit_reports/BRAND-VOICE.md

Recommended next steps:
  1. Share BRAND-VOICE.md with anyone who writes for Scentified
  2. Run /market-social to generate a content calendar using this voice
  3. Run /market-ads to create ad copy using these guidelines
```

---

## Important Rules

- Only quote copy that was actually found in the source material — do not invent examples
- If a source is inaccessible (403, timeout), note it and continue with what was available
- The guidelines must be specific to Scentified — not generic luxury brand advice
- If current copy is inconsistent, document what the voice SHOULD be (aspirational guidelines), clearly distinguished from what was found
- All copy samples must pass the Scentified voice test: would a Lagos professional trust this? Does it feel like Scentified?
