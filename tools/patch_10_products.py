"""
Full RankMath patch for the 10 AAA / Essential Parfums test products.
Generates: focus keyword, revised title, revised meta desc, patched description
           (keyword in first sentence, Best For heading, internal link,
            external DoFollow link), image alt text, slug check.
"""
import json, re

STORE = "https://scentifiedperfume.com"
AAA_CAT_URL  = f"{STORE}/product-category/aaa/"
EP_CAT_URL   = f"{STORE}/product-category/essential-parfum/"
AAA_EXT_URL  = "https://www.nabeel.com"          # parent brand — mentioned in desc
EP_EXT_URL   = "https://essentialparfums.com"

# ── Product definitions ───────────────────────────────────────────────────────
PRODUCTS = [
    {
        "id": 6864, "name": "AAA RANYA 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-ranya-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-ranya-100ml-spray-perfume",
        "image_ids": [6854],
        "focus_keyword": "AAA Ranya EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Ranya EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Cherry, Saffron and Tuberose in a powdery 7–9 hour AAA Ranya EDP. Authentic Asghar Adam Ali, delivered across Nigeria. Buy now at Scentified.",
        "open_patch": ('With a name that evokes admiration, Ranya by Asghar Adam Ali',
                       'With a name that evokes admiration, AAA Ranya EDP by Asghar Adam Ali'),
        "current_seo_title": "AAA Ranya Perfume EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Cherry, Saffron and Tuberose bloom in a powdery Floral EDP. Authentic Asghar Adam Ali, 7–9 hours longevity. Buy AAA Ranya in Nigeria — Scentified.",
    },
    {
        "id": 6863, "name": "AAA MAZYUNA 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-mazyuna-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-mazyuna-100ml-spray-perfume",
        "image_ids": [6852],
        "focus_keyword": "AAA Mazyuna EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Mazyuna EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Raspberry, Bulgarian Rose and Oud Vanilla in a rich AAA Mazyuna EDP. 8–10 hours. Authentic Asghar Adam Ali, delivered across West Africa. Shop Scentified.",
        "open_patch": ('Mazyuna — a name that translates',
                       'AAA Mazyuna EDP — a name that translates'),
        "current_seo_title": "AAA Mazyuna 100ml EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Raspberry, Bulgarian Rose and Oud in a rich Amber Vanilla EDP. 8–10 hours. Authentic Asghar Adam Ali, delivered across West Africa. Shop Scentified.",
    },
    {
        "id": 6862, "name": "AAA HAMZA 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-hamza-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-hamza-100ml-spray-perfume",
        "image_ids": [6850],
        "focus_keyword": "AAA Hamza EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Hamza EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Bergamot, Leather and Sandalwood in a bold Woody Citrus AAA Hamza EDP. 7–9 hours, Moderate–Strong projection. Buy in Lagos — Scentified delivers fast.",
        "open_patch": ('A name born of valor, Hamza by Asghar Adam Ali symbolizes',
                       'A name born of valor, AAA Hamza EDP by Asghar Adam Ali symbolizes'),
        "current_seo_title": "AAA Hamza Perfume EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Bergamot, Leather and Sandalwood in a bold Woody Citrus EDP. 7–9 hours, Moderate–Strong projection. Buy AAA Hamza in Lagos — fast delivery, Scentified.",
    },
    {
        "id": 6861, "name": "AAA EESA 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-eesa-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-eesa-100ml-spray-perfume",
        "image_ids": [6848],
        "focus_keyword": "AAA Eesa EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Eesa EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Cardamom, Jasmine and Sandalwood in a spiced Woody Floral AAA Eesa EDP. 7–9 hours longevity. Authentic Asghar Adam Ali, buy across Nigeria — Scentified.",
        "open_patch": ('Drawing from a name steeped in purity and spirituality, Eesa by Asghar Adam Ali radiates',
                       'Drawing from a name steeped in purity and spirituality, AAA Eesa EDP by Asghar Adam Ali radiates'),
        "current_seo_title": "AAA Eesa Perfume EDP 100ml | Buy in Nigeria — Scentified",
        "current_seo_desc": "Cardamom, Jasmine and Sandalwood in a Woody Spicy Floral EDP. 7–9 hours longevity. Authentic AAA fragrance, buy in Nigeria and delivered fast — Scentified.",
    },
    {
        "id": 6860, "name": "AAA AVTAR 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-avtar-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-avtar-100ml-spray-perfume",
        "image_ids": [6847],
        "focus_keyword": "AAA Avtar EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Avtar EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Bergamot, Rose and Tonka Amber in a Woody Aromatic AAA Avtar EDP. 7–9 hours. Authentic Asghar Adam Ali, delivered across West Africa. Shop Scentified.",
        "open_patch": ('A name with profound meaning, Avtar by Asghar Adam Ali is',
                       'A name with profound meaning, AAA Avtar EDP by Asghar Adam Ali is'),
        "current_seo_title": "AAA Avtar Perfume EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Bergamot, Rose and Tonka Amber in a complex Woody Aromatic EDP. 7–9 hours. Authentic Asghar Adam Ali, delivered across West Africa. Buy at Scentified.",
    },
    {
        "id": 6859, "name": "AAA ASIYA 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-asiya-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-asiya-100ml-spray-perfume",
        "image_ids": [6845],
        "focus_keyword": "AAA Asiya EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Asiya EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Mandarin, Rose and Caramel Amber in a joyful Floral Chypre AAA Asiya EDP. 7–9 hours. Authentic Asghar Adam Ali, buy in Lagos — Scentified delivers fast.",
        "open_patch": ('Cradling in its embrace, the name Asiya whispers',
                       'Cradling in its embrace, AAA Asiya EDP whispers'),
        "current_seo_title": "AAA Asiya Perfume EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Mandarin, Rose and Caramel Amber in a joyful Floral Chypre EDP. 7–9 hours longevity. Authentic AAA fragrance, buy in Lagos — Scentified delivers fast.",
    },
    {
        "id": 6858, "name": "AAA ASHJAN 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-ashjan-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-ashjan-100ml-spray-perfume",
        "image_ids": [6843],
        "focus_keyword": "AAA Ashjan EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Ashjan EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Cherry, Jasmine and Vanilla Musk in a Fruity Gourmand AAA Ashjan EDP. 7–8 hours. Authentic Asghar Adam Ali, delivered across Nigeria. Order at Scentified.",
        "open_patch": ('A testament to intensity and desire, Ashjan by Asghar Adam Ali pulses',
                       'A testament to intensity and desire, AAA Ashjan EDP by Asghar Adam Ali pulses'),
        "current_seo_title": "AAA Ashjan 100ml EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Cherry, Jasmine and Vanilla Musk in a Fruity Gourmand EDP. 7–8 hours longevity. Authentic Asghar Adam Ali, delivered across Nigeria. Order at Scentified.",
    },
    {
        "id": 6857, "name": "AAA ABSOLUTE 100ML SPRAY PERFUME",
        "permalink": f"{STORE}/product/aaa-absolute-100ml-spray-perfume/",
        "price": "207000", "categories": ["AAA","FRAGRANCE"],
        "current_slug": "aaa-absolute-100ml-spray-perfume",
        "image_ids": [6840],
        "focus_keyword": "AAA Absolute EDP",
        "brand_display": "Asghar Adam Ali", "brand_short": "AAA",
        "cat_url": AAA_CAT_URL, "ext_url": AAA_EXT_URL, "ext_label": "Nabeel Parfums",
        "seo_title": "AAA Absolute EDP Perfume | Buy in Nigeria — Scentified",
        "seo_desc":  "Saffron, Leather and Oud Amber in a rich Citrus Leathery AAA Absolute EDP. 8–10 hours, Moderate–Strong projection. Buy in Lagos — Scentified.",
        "open_patch": ('Being wholly immersed in the essence of life itself, Absolute by Asghar Adam Ali denotes',
                       'Being wholly immersed in the essence of life itself, AAA Absolute EDP from Asghar Adam Ali denotes'),
        "current_seo_title": "AAA Absolute 100ml EDP | Buy in Nigeria — Scentified",
        "current_seo_desc": "Saffron, Leather and Oud Amber in a rich Citrus Leathery EDP. 8–10 hours, Moderate–Strong projection. Buy AAA Absolute in Lagos — Scentified.",
    },
    {
        "id": 6612, "name": "ESSENTIAL PARFUM VELVET IRIS EDP 100ML",
        "permalink": f"{STORE}/product/velvet-iris-edp-100ml/",
        "price": "190000", "categories": ["ESSENTIAL PARFUM","FRAGRANCE"],
        "current_slug": "velvet-iris-edp-100ml",
        "image_ids": [6629],
        "focus_keyword": "Essential Parfums Velvet Iris",
        "brand_display": "Essential Parfums", "brand_short": "Essential Parfums",
        "cat_url": EP_CAT_URL, "ext_url": EP_EXT_URL, "ext_label": "Essential Parfums official site",
        "seo_title": "Essential Parfums Velvet Iris | Nigeria — Scentified",
        "seo_desc":  "Iris, Leather and Sandalwood in a bold powdery Essential Parfums Velvet Iris EDP by Ropion. 8–10 hours, strong projection. Buy in Nigeria — Scentified.",
        "open_patch": ('Velvet Iris by Essential Parfums is',
                       'Essential Parfums Velvet Iris is'),
        "current_seo_title": "Essential Parfums Velvet Iris EDP | Nigeria — Scentified",
        "current_seo_desc": "Iris, Leather and Sandalwood in a bold powdery EDP by Ropion. 8–10 hours, strong projection. Buy Essential Parfums Velvet Iris in Nigeria — Scentified.",
    },
    {
        "id": 6611, "name": "ESSENTIAL PARFUM ROSE MAGNETIC EDP 100ML",
        "permalink": f"{STORE}/product/rose-magnetic-edp-100ml/",
        "price": "190000", "categories": ["ESSENTIAL PARFUM","FRAGRANCE"],
        "current_slug": "rose-magnetic-edp-100ml",
        "image_ids": [6630],
        "focus_keyword": "Essential Parfums Rose Magnetic",
        "brand_display": "Essential Parfums", "brand_short": "Essential Parfums",
        "cat_url": EP_CAT_URL, "ext_url": EP_EXT_URL, "ext_label": "Essential Parfums official site",
        "seo_title": "Essential Parfums Rose Magnetic | Nigeria — Scentified",
        "seo_desc":  "Turkish Rose, Lychee and Tonka Bean in a sustainable Essential Parfums Rose Magnetic EDP by Sophie Labbe. 6–8 hours longevity. Buy in Nigeria — Scentified.",
        "open_patch": ('Rose Magnetic by Essential Parfums is',
                       'Essential Parfums Rose Magnetic is'),
        "current_seo_title": "Essential Parfums Rose Magnetic EDP | Nigeria — Scentified",
        "current_seo_desc": "Turkish Rose, Lychee and Tonka Bean in a sustainable EDP by Sophie Labbe. 6–8 hours longevity. Buy Essential Parfums Rose Magnetic in Nigeria — Scentified.",
    },
]

# ── Descriptions (fetched from WooCommerce) ───────────────────────────────────
# These are the full current descriptions keyed by product ID.
DESCS = {
    6864: '<p>With a name that evokes admiration, Ranya by Asghar Adam Ali is an ode to beauty that is charming, delightful, and impossible to look away from. This 100ml Eau de Parfum opens with a delectable symphony of Cherry, Saffron, and Pink Pepper — a prelude that is delicate yet intriguing — before the heart blooms with Tuberose, Peony, Rose, and Violet, draped in White Flowers and caressed by Cashmere Wood. The base closes with a soft, indulgent accord of Sandalwood, Musk, Ambroxan, and Pink Praline, leaving behind an intoxicating trail.</p>\n<p>Encased in a gradient bottle of rich purple, crowned with a rose-gold cap, and housed in a marble-textured purple box, Ranya is a vision of grace and splendour.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Leaf, Cherry, Saffron, Pink Pepper<br />\n<strong>Heart Notes:</strong> Tuberose, White Flowers, Rose, Peony, Violet, Cashmere Wood<br />\n<strong>Base Notes:</strong> Sandalwood, Musk, Ambroxan, Pink Praline</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–9 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Ranya suits evening celebrations, festive gatherings, and any occasion in Lagos where a warm, powdery floral presence speaks before you do. Its Floriental warmth makes it equally at home at intimate dinners, weddings, and vibrant social events — a fragrance that draws admiration from every direction.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6863: '<p>Mazyuna — a name that translates to ‘beautiful and adorable’ — is the epitome of elegance, warmth, and grace. This 100ml Eau de Parfum from Asghar Adam Ali opens with a decadent overture of Raspberry, Almond, Cassis, Chocolate, Bergamot, and Cinnamon. The heart glows with Rose Oil Bulgarian, Geranium Oil Egypt, Magnolia, Orris, and Chestnut. At the base, a divine accord of Tonka Bean, Pure Rare Vanilla, Leather Oud, Oud Saafi, Sandalwood, Musk, Praline, and Oak Wood reveals the full measure of its opulence.</p>\n<p>Presented in a glossy red bottle crowned with a gold cap and housed in a marble-textured red box, Mazyuna reflects its fragrance’s sensual richness — bold in character and timeless in elegance.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Almond, Raspberry, Chocolate, Cassis, Bergamot, Cinnamon<br />\n<strong>Heart Notes:</strong> Rose Oil Bulgarian, Geranium Oil Egypt, Magnolia, Orris, Floral Notes, Chestnut<br />\n<strong>Base Notes:</strong> Pure Rare Vanilla, Tonka Bean, Sandalwood, Musk, Leather Oud, Oud Saafi, Praline, Oak Wood</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 8–10 hours<br />\n<strong>Projection:</strong> Moderate–Strong<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Mazyuna was made for cool evenings, intimate dinners, and occasions in Lagos where warmth and depth signal refined taste. Its Amber Vanilla Gourmand character makes it particularly compelling in the harmattan season — a fragrance that lingers in memory long after you have left the room.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6862: '<p>A name born of valor, Hamza by Asghar Adam Ali symbolizes unflinching courage, untamed strength, and a commanding silence — the spirit of one who never yields. This 100ml Eau de Parfum opens with the crisp allure of Pear, Bergamot, Grapefruit, Black Pepper, and Juniper — a sharp, decisive declaration of intent. The heart delves deeper with Leather, Incense, Magnolia, Rose, and Oak Bark, while the base anchors the composition in the warm embrace of Sandalwood, Patchouli, Vetiver, Labdanum, and Amberwood.</p>\n<p>From its grey matte finish to its matching grey cap and marble-textured grey box, the presentation is as dignified as the fragrance — understated, resolute, and built to command respect.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Pear, Bergamot, Ginger, Grapefruit, Orange, Black Pepper, Juniper<br />\n<strong>Heart Notes:</strong> Rose, Incense, Magnolia, Leather, Orris, Oak Bark<br />\n<strong>Base Notes:</strong> Vanilla, Sandalwood, Ambroxan, Vetiver, Patchouli, Labdanum, Amberwood</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–9 hours<br />\n<strong>Projection:</strong> Moderate–Strong<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Hamza is a fragrance for formal occasions, boardrooms, and evening events in Lagos where authority and sophistication must be felt before a word is spoken. Its Woody Citrus profile makes it a strong choice for professional settings and black-tie affairs — a scent that wears as well as the man.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6861: '<p>Drawing from a name steeped in purity and spirituality, Eesa by Asghar Adam Ali radiates grace, depth, and divine strength. This 100ml Eau de Parfum awakens the senses with the warmth of Nutmeg, Cardamom, Lemon, Cumin, Bergamot, and Pink Pepper — an opening that is deeply spiced yet luminously bright. The heart intertwines Ginger, Jasmine, Orange Blossom, Leather, Juniper, and Rose in a complex accord of rare beauty, while the base lays a majestic foundation of Sandalwood, Musk, Vanilla, Cedarwood, Ambergris, and Patchouli.</p>\n<p>Housed in a transparent green bottle adorned with a sculpted black cap and encased in a marble-finish green box, Eesa is as elegant in form as it is in character.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Nutmeg, Cardamom, Lemon, Pink Pepper, Cumin, Bergamot, Grapefruit<br />\n<strong>Heart Notes:</strong> Ginger, Jasmine, Orange Blossom, Leather, Juniper, Rose<br />\n<strong>Base Notes:</strong> Sandalwood, Musk, Vanilla, Cedarwood, Ambergris, Patchouli, Vetiver</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–9 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Eesa suits formal occasions, evening events, and moments of personal significance — equally at home in a quiet setting as on a polished social stage in Lagos. Its Woody Floral Spicy character speaks to those who carry their values with elegance and wear their fragrance with intention.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6860: '<p>A name with profound meaning, Avtar by Asghar Adam Ali is a powerful personification of principles and the very essence of existence. This 100ml Eau de Parfum opens with a cascade of Bergamot, Lavandin, Mandarin, Pink Peppercorn, Cardamom, Clove, and Ginger — a complex, aromatic prelude of exceptional depth. The heart unfolds with Rose, Iris, Geranium, Ambrette, and Fig Leaves. At the base, Tonka, Leather, Amber, Balsam, Benzoin, and Patchouli anchor this composition in a rich, musky warmth that lingers long into the evening.</p>\n<p>Its deep blue hue is reminiscent of a twilight sky — brimming with mystery and depth — and the sculptured bottle form is a prelude to the fragrance within.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Bergamot, Mandarin, Lavandin, Pink Peppercorn, Cedarwood, Cardamom, Pepper, Clove, Ginger<br />\n<strong>Heart Notes:</strong> Orris, Geranium, Rose, White Floral, Iris, Ambrette, Fig Leaves<br />\n<strong>Base Notes:</strong> Tonka, Vanilla, Musk, Ambroxan, Labdanum, Balsam, Amber, Benzoin, Leather, Patchouli</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–9 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Avtar is a fragrance for those who embrace complexity and refuse to be defined by simplicity. Its multifaceted Woody Aromatic Floral character works beautifully across evening occasions, cultural events, and dinner gatherings in Lagos where presence, depth, and individuality speak volumes.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6859: '<p>Cradling in its embrace, the name Asiya whispers of consolation and the warmth of sunlit lands. Asiya by Asghar Adam Ali is a 100ml Eau de Parfum that begins with a burst of Mandarin, Bergamot, Pear, and White Floral — further adorned with Basil, Pepper, and Clove. The heart reveals an opulent core of Rose, Caramel, Orange Blossom, Narcissus, and Heliotrope, while the journey concludes with a majestic base of Labdanum, Sandalwood, Amber, Vanilla, and Musk.</p>\n<p>The bright pink and white packaging, with its intricate patterns and layered textures, mirrors the playful spirit and timeless purity of the fragrance within.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Mandarin, Bergamot, Pear, White Floral, Basil, Pepper, Clove<br />\n<strong>Heart Notes:</strong> Rose, Caramel, Gourmand Notes, Orange Blossom, Narcissus, Heliotrope, Patchouli<br />\n<strong>Base Notes:</strong> Labdanum, Sandalwood, Amber, Vanilla, Musk</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–9 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Asiya is a fragrance for women who carry joy and warmth wherever they go. Its Ambery Floral Chypre character makes it well-suited to afternoon gatherings, weddings, and social celebrations in Lagos — soft enough for daytime, rich enough for evening, and joyful enough for every occasion in between.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6858: '<p>A testament to intensity and desire, Ashjan by Asghar Adam Ali pulses with passion and stirs the soul. This 100ml Eau de Parfum opens with a bold symphony of Cherry, Chocolate, Coconut, and Ginger — a Fruity Floral Gourmand declaration that commands attention from the first spray. The heart opens into the floral mystic of Jasmine, Lily of the Valley, Heliotrope, and Ylang-Ylang, before a final accord of White Musk, Vanilla, Ambrette Seeds, and Rose anchors the fragrance with an addictive, lasting warmth.</p>\n<p>A vision of orange and rose gold brilliance, the packaging features sophisticated geometric patterns and sculptural detail that mirror the fragrance’s passionate character.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Cherry, Coconut, Chocolate, Ginger<br />\n<strong>Heart Notes:</strong> Lily of the Valley, Jasmine, Ylang-Ylang, Heliotrope<br />\n<strong>Base Notes:</strong> White Musk, Vanilla, Ambrette Seeds, Rose</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 7–8 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Ashjan was made for evenings that demand presence and passion — dinner dates, upscale parties, and Lagos nights where a gourmand floral trail leaves an unforgettable impression. Its warmth and sensuality make it a natural signature scent for those who embrace their allure with confidence.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6857: '<p>Being wholly immersed in the essence of life itself, Absolute by Asghar Adam Ali denotes ultimate fulfilment and everything exquisite. This 100ml Eau de Parfum greets with a vibrant burst of Orange, Bergamot, Saffron, Mandarin, and Coriander — a radiant, spiced citrus opening of exceptional clarity. The heart is layered with sensual accords of Leather, Incense, Cashmeran, Violet, Brown Sugar, and Orange Blossom. At the base, Musk, Patchouli, Oud Accord, Benzoin, Labdanum, and Amber linger with a profound and lasting richness.</p>\n<p>From its pristine white colour to its dazzling silver embellishments, the bottle transforms the act of wearing perfume into a ritual of beauty and indulgence.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Orange, Lemon, Pink Pepper, Bergamot, Mandarin, Cardamom, Saffron, Ginger, Coriander<br />\n<strong>Heart Notes:</strong> Incense, Leather, Cashmeran, Violet, Plum, Pineapple, Orange Blossom, Jasmine, Brown Sugar<br />\n<strong>Base Notes:</strong> Patchouli, Sandalwood, Guaiac Wood, Oud Accord, Labdanum, Musk, Benzoin, Balsam, Amber</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 8–10 hours<br />\n<strong>Projection:</strong> Moderate–Strong<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Absolute is the signature scent for the connoisseur — an evening fragrance for Lagos’s finest moments: gallery openings, gala dinners, and occasions where only the extraordinary will do. Its Citrus Leathery Woody depth builds from a fresh spiced opening to a commanding oud and amber finish that defines the room.</p>\n<h3>About Asghar Adam Ali</h3>\n<p>Asghar Adam Ali Parfums is a luxury fragrance house bearing the name of its founder, Asghar Adam Ali Al Attar — a master perfumer who established Nabeel Perfumes in 1969 and has shaped Arabian perfumery for over five decades. Drawing from Arab heritage and the cosmopolitan spirit of Dubai, the brand crafts fragrances for those who value opulence, sophistication, and individuality. As the founder’s philosophy states: you don’t just wear a fragrance — you embody it.</p>\n<p><em>Authentic Asghar Adam Ali fragrances, sourced directly and delivered across Nigeria. Shop the full Asghar Adam Ali collection at Scentified.</em></p>\n',
    6612: '<p>Velvet Iris by Essential Parfums is a bold, vibrant interpretation of nature’s most architectural floral, crafted by master perfumer Dominique Ropion. This 100ml Eau de Parfum opens with the assertive green energy of Buchu Leaf, Galbanum, Lentisque, and Pink Pepper — an earthy, electric prelude that sets the stage for the iris to unfold. The heart reveals Orris Root, Violet, and the nuanced facets of Irones in a powdery, deeply textured iris accord. A commanding base of Leather, Labdanum, Sandalwood, and Tamarind closes the composition with warmth and authority. This long-lasting formula makes an unmistakable statement about personality, lingering powerfully until the final moments of the day.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Buchu Leaf, Galbanum, Lentisque, Pink Pepper<br />\n<strong>Heart Notes:</strong> Orris Root, Violet, Irones<br />\n<strong>Base Notes:</strong> Leather, Labdanum, Sandalwood, Tamarind</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 8–10 hours<br />\n<strong>Projection:</strong> Good–Strong<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Velvet Iris suits bold personalities and occasions that reward presence — from professional settings and gallery openings to evening events across Lagos where a refined, non-conformist fragrance makes a statement without saying a word. Its character is equally compelling on men and women, making it a standout unisex choice for the discerning nose.</p>\n<h3>About Essential Parfums</h3>\n<p>Essential Parfums is a modern Paris-based niche fragrance house founded in 2018, built on the philosophy that true beauty lies in the essential — the absence of excess and the pursuit of fundamental nature. The brand collaborates exclusively with world-class perfumers including Dominique Ropion, Anne Flipo, and Sophie Labbe to create accessible yet sophisticated Eau de Parfum compositions. Every bottle in the collection is refillable, reflecting the brand’s commitment to sustainable development at the heart of luxury.</p>\n<p><em>Authentic Essential Parfums fragrances, sourced directly and delivered across Nigeria. Shop the full Essential Parfums collection at Scentified.</em></p>\n',
    6611: '<p>Rose Magnetic by Essential Parfums is a fragrance of captivating allure — a sustainably crafted, multidimensional rose composed by perfumer Sophie Labbe. This 100ml Eau de Parfum opens with the bright tartness of Grapefruit and Lychee, softened by a burst of fresh Mint, before a lush heart of Turkish Rose and natural Rose Essential LMR — both certified ‘For Life’ and sustainably sourced — takes full command. Tonka Bean, Vanilla Bean, Cedarwood, and Musk round out the base with an approachable warmth that makes Rose Magnetic as wearable as it is beautiful.</p>\n<h3>Fragrance Notes</h3>\n<p><strong>Top Notes:</strong> Grapefruit, Lychee, Mint<br />\n<strong>Heart Notes:</strong> Turkish Rose, Rose Essential<br />\n<strong>Base Notes:</strong> Tonka Bean, Vanilla Bean, Cedarwood, Musk</p>\n<h3>Performance</h3>\n<p><strong>Longevity:</strong> 6–8 hours<br />\n<strong>Projection:</strong> Moderate<br />\n<strong>Concentration:</strong> Eau de Parfum (EDP)</p>\n<h3>Best For</h3>\n<p>Rose Magnetic is the ideal everyday rose for warm Lagos mornings, afternoon meetings, and social occasions where you want to leave a subtle, magnetic impression without overpowering the room. Its bright, fruity opening and velvety dry-down make it a versatile signature scent that transitions effortlessly from day to evening across every season.</p>\n<h3>About Essential Parfums</h3>\n<p>Essential Parfums is a modern Paris-based niche fragrance house founded in 2018, built on the philosophy that true beauty lies in the essential — the absence of excess and the pursuit of fundamental nature. The brand collaborates exclusively with world-class perfumers including Dominique Ropion, Anne Flipo, and Sophie Labbe to create accessible yet sophisticated Eau de Parfum compositions. Every bottle in the collection is refillable, reflecting the brand’s commitment to sustainable development at the heart of luxury.</p>\n<p><em>Authentic Essential Parfums fragrances, sourced directly and delivered across Nigeria. Shop the full Essential Parfums collection at Scentified.</em></p>\n',
}

BANNED_GEO = ["across africa", "across the continent"]


def patch_description(desc, p):
    fk   = p["focus_keyword"]
    old, new = p["open_patch"]

    # 1. Keyword in first sentence of opening <p>
    desc = desc.replace(old, new, 1)

    # 2. Best For heading — append focus keyword
    desc = desc.replace("<h3>Best For</h3>", f"<h3>Best For — {fk}</h3>", 1)

    # 3. Closing tagline — fix Nigeria→West Africa + add internal link
    brand_d = p["brand_display"]
    brand_s = p["brand_short"]
    cat_url = p["cat_url"]
    old_tag = (
        f'<p><em>Authentic {brand_d} fragrances, sourced directly and delivered across Nigeria. '
        f'Shop the full {brand_d} collection at Scentified.</em></p>'
    )
    new_tag = (
        f'<p><em>Authentic {brand_d} fragrances, sourced directly and delivered across West Africa. '
        f'Shop the full <a href="{cat_url}">{brand_s} collection</a> at Scentified.</em></p>'
    )
    desc = desc.replace(old_tag, new_tag, 1)

    # Fallback for Essential Parfums (brand_d == brand_s)
    if old_tag in desc or new_tag not in desc:
        alt_old = (
            f'<p><em>Authentic {brand_s} fragrances, sourced directly and delivered across Nigeria. '
            f'Shop the full {brand_s} collection at Scentified.</em></p>'
        )
        desc = desc.replace(alt_old, new_tag, 1)

    # 4. External DoFollow link — append to last sentence of About <p>
    ext_url   = p["ext_url"]
    ext_label = p["ext_label"]
    ext_link  = f' <a href="{ext_url}" target="_blank" rel="noopener noreferrer">Visit the {ext_label}</a>.'
    # Find the last </p> before the closing tagline and inject link before it
    # We target the About section paragraph ending
    desc = re.sub(
        r'(you embody it\.)</p>',
        rf'\1{ext_link}</p>',
        desc, count=1
    )
    # For Essential Parfums (different closing phrase)
    desc = re.sub(
        r'(at the heart of luxury\.)</p>',
        rf'\1{ext_link}</p>',
        desc, count=1
    )

    return desc


def strip_html(html):
    return re.sub(r'<[^>]+>', '', html)


def keyword_density(desc_html, fk):
    text  = strip_html(desc_html).lower()
    words = text.split()
    kw    = fk.lower()
    count = text.count(kw)
    # RankMath measures occurrences / total words (not multiplied by keyword length)
    density = count / max(len(words), 1) * 100
    return count, round(density, 1)


results = []
all_pass = True

for p in PRODUCTS:
    fk    = p["focus_keyword"]
    t     = p["seo_title"]
    d     = p["seo_desc"]
    t_len = len(t)
    d_len = len(d)

    desc_patched = patch_description(DESCS[p["id"]], p)
    img_alt      = f"{fk} perfume Nigeria"
    kw_count, kw_density = keyword_density(desc_patched, fk)

    # Keyword at beginning of title (startswith is accurate for long focus keywords)
    fk_in_first30 = t.lower().startswith(fk.lower())

    fails = []

    # Title
    if not (50 <= t_len <= 60):
        fails.append(f"Title length {t_len} (need 50–60)")
    if not fk_in_first30:
        fails.append(f"Focus keyword not in first 30 chars of title: '{t[:30]}'")
    if not any(g.lower() in t.lower() for g in ["Nigeria", "Scentified"]):
        fails.append("Title missing Nigeria or Scentified")

    # Meta desc
    if not (140 <= d_len <= 155):
        fails.append(f"Desc length {d_len} (need 140–155)")
    if fk.lower() not in d.lower():
        fails.append(f"Focus keyword '{fk}' not verbatim in meta desc")
    if not any(g.lower() in d.lower() for g in ["nigeria", "lagos", "west africa"]):
        fails.append("Desc missing geographic signal")
    if not any(c.lower() in d.lower() for c in ["shop", "buy", "order"]):
        fails.append("Desc missing CTA")
    for bad in BANNED_GEO:
        if bad in d.lower() or bad in t.lower():
            fails.append(f"Banned geo: '{bad}'")

    # Content
    if fk.lower() not in strip_html(desc_patched[:500]).lower():
        fails.append("Focus keyword not in first paragraph of description")
    if f"Best For — {fk}" not in desc_patched:
        fails.append("Focus keyword not in Best For heading")
    if p["cat_url"] not in desc_patched:
        fails.append("Internal link missing")
    if p["ext_url"] not in desc_patched:
        fails.append("External DoFollow link missing")
    if not (0.5 <= kw_density <= 2.0):
        fails.append(f"Keyword density {kw_density}% (aim 0.5–2%)")

    qa = len(fails) == 0
    if not qa:
        all_pass = False

    results.append({
        "id":                 p["id"],
        "name":               p["name"],
        "permalink":          p["permalink"],
        "price":              p["price"],
        "categories":         p["categories"],
        "focus_keyword":      fk,
        "current_seo_title":  p["current_seo_title"],
        "current_seo_desc":   p["current_seo_desc"],
        "current_slug":       p["current_slug"],
        "proposed_seo_title": t,
        "proposed_seo_desc":  d,
        "proposed_slug":      "",
        "proposed_description": desc_patched,
        "image_ids":          p["image_ids"],
        "image_alt_text":     img_alt,
        "research": {
            "primary_keyword":  fk,
            "brand_site_url":   p["ext_url"],
            "sources_used":     ["existing product description"],
            "serp_notes":       "Optimised from existing on-site data. No external SERP fetch required.",
            "keyword_density":  f"{kw_density}%",
            "keyword_in_h3":    True,
        },
        "qa_passed":    qa,
        "qa_notes":     "; ".join(fails),
        "update_status":"draft",
        "update_error": "",
    })

    status = "PASS" if qa else "FAIL"
    print(f"[{status}] {p['name']}")
    print(f"        FK       : {fk}")
    print(f"        Title ({t_len}): {t}")
    print(f"        Desc  ({d_len}): {d}")
    print(f"        Density  : {kw_density}% ({kw_count} occurrences)")
    if fails:
        for f in fails:
            print(f"        !! {f}")
    print()

with open("tools/seo_staging.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, ensure_ascii=False, indent=2)

passed = sum(1 for r in results if r["qa_passed"])
print(f"--- {passed}/{len(results)} passed QA ---")
print("Written to tools/seo_staging.json")
