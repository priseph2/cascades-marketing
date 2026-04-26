"""
Scentified Marketing Suite — Streamlit Web UI

Access: py app.py   (local dev)
Deploy: streamlit cloud — connect github.com/your-repo

Auth: password set in .streamlit/secrets.toml  [auth.app_password]
Credentials: set in .streamlit/secrets.toml   [credentials.*]
"""
import os
import sys
import json
import time
import threading
from datetime import datetime
from pathlib import Path

import streamlit as st

# ── Project root ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from config import CONFIG
from integrations.woocommerce import woo_api


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_creds():
    """Return credentials from Streamlit secrets (deployed) or env vars (local)."""
    try:
        return st.secrets["credentials"]
    except Exception:
        return {
            "store_url":           os.environ.get("STORE_URL",           "https://scentifiedperfume.com"),
            "woo_consumer_key":    os.environ.get("WOO_CONSUMER_KEY",    ""),
            "woo_consumer_secret": os.environ.get("WOO_CONSUMER_SECRET", ""),
            "pagespeed_api_key":    os.environ.get("PAGESPEED_API_KEY",   ""),
        }


def require_auth():
    """Simple password gate. Call once at app start."""
    try:
        app_password = st.secrets["auth"]["app_password"]
    except Exception:
        app_password = os.environ.get("APP_PASSWORD", "")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("## 🔒 Scentified Marketing Suite")
        st.markdown("Enter your access password to continue.")
        pw = st.text_input("Password", type="password", label_visibility="collapsed",
                           placeholder="Enter password...")
        col1, col2 = st.columns([1, 1])
        with col1:
            if pw == app_password and pw:
                st.session_state["authenticated"] = True
                st.rerun()
        with col2:
            if pw and pw != app_password:
                st.error("Incorrect password.")
        st.stop()


def call_woo_api(endpoint, params=None, creds=None):
    base = creds["store_url"].rstrip("/")
    url  = f"{base}/wp-json/wc/v3/{endpoint}"
    auth = (creds["woo_consumer_key"], creds["woo_consumer_secret"])
    import requests
    try:
        r = requests.get(url, auth=auth, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None


def test_connection(creds):
    result = call_woo_api("system_status", creds=creds)
    return result is not None


def run_background(target, args=(), kwargs=None):
    """Run `target(*args, **kwargs)` in a background thread with session_state updates."""
    if kwargs is None:
        kwargs = {}
    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as e:
            st.session_state["_bg_error"] = str(e)
        finally:
            st.session_state["_bg_running"] = False
            st.session_state["_bg_done"] = True
    st.session_state["_bg_running"] = True
    st.session_state["_bg_done"] = False
    st.session_state["_bg_error"] = None
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()


def poll_until_done(sleep_sec=2, progress_template="Processing..."):
    """Poll _bg_running until background thread finishes. Show live progress."""
    placeholder = st.empty()
    while st.session_state.get("_bg_running", False):
        msg = st.session_state.get("_progress_msg", progress_template)
        st.session_state.get("_progress_pct", 0)
        placeholder.info(f"⏳ {msg}")
        time.sleep(sleep_sec)
    placeholder.empty()
    if st.session_state.get("_bg_error"):
        st.error(f"Error: {st.session_state['_bg_error']}")


def load_score_history():
    """Load audit run history. Returns list of dicts."""
    history_file = PROJECT_ROOT / CONFIG.get("history_file", "audit_reports/score_history.json")
    if history_file.exists():
        with open(history_file) as f:
            return json.load(f)
    return []


def load_staging(stem):
    """Load a staging JSON file. stem='descriptions' or 'seo'."""
    path = PROJECT_ROOT / "tools" / f"{stem}_staging.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Scentified Marketing Suite",
    page_icon="✨",
    layout="wide",
)

require_auth()

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #16213E;
        border-radius: 4px 4px 0 0;
        padding: 6px 16px;
        color: #C9A84C;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"]:hover { background: #1A1A2E; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #C9A84C;
        color: #1A1A2E;
    }
    .stButton button[data-baseweb="button"] {
        background-color: #C9A84C;
        color: #1A1A2E;
        font-weight: 700;
        border: none;
        border-radius: 4px;
    }
    .stButton button[data-baseweb="button"]:hover {
        background-color: #E5B84C;
    }
    .stMetric { background: #16213E; border-radius: 8px; padding: 12px; }
    .stProgress > div > div { background-color: #C9A84C; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ✨ Scentified")
    st.markdown("**Marketing Suite**")
    st.divider()

    st.markdown("#### 🔑 Credentials")
    creds = get_creds()

    def cred_status(val):
        return "✅ Configured" if val else "❌ Missing"

    st.markdown(f"**Store URL**  \n{creds['store_url']}")
    st.markdown(f"**WC Key**  \n{cred_status(creds.get('woo_consumer_key'))}")
    st.markdown(f"**WC Secret**  \n{cred_status(creds.get('woo_consumer_secret'))}")
    st.markdown(f"**PageSpeed Key**  \n{cred_status(creds.get('pagespeed_api_key'))}")

    if st.button("🔗 Test Connection", use_container_width=True):
        with st.spinner("Testing WooCommerce connection..."):
            ok = test_connection(creds)
        if ok:
            st.success("✅ Connected to WooCommerce")
        else:
            st.error("❌ Connection failed — check credentials")

    st.divider()
    st.markdown("#### 📊 Store")
    try:
        store_data = call_woo_api("products?per_page=1", creds=creds)
        if store_data is not None:
            total = call_woo_api("products?per_page=1", creds=creds)
            st.success(f"🛒 WooCommerce connected")
        else:
            st.warning("⚠️ Could not fetch store data")
    except Exception:
        st.warning("⚠️ Could not fetch store data")

    st.divider()
    st.markdown("#### 🔗 Quick Links")
    st.markdown(f"[📦 WooCommerce Admin]({creds['store_url']}/wp-admin)")
    st.markdown(f"[🌐 Store Frontend]({creds['store_url']})")

    st.divider()
    st.caption("Powered by Scentified AI")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: FULL AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

def render_audit_tab(creds):
    st.markdown("## 📊 Full eCommerce Audit")
    st.markdown("Run a 9-dimension audit of your store: PageSpeed, UX, SEO, Products, Checkout, Competitors, Revenue, and more.")

    col_run, col_dl_pdf, col_dl_json = st.columns([1, 1, 1])

    with col_run:
        run_audit = st.button("🚀 Run Full Audit", use_container_width=True,
                              disabled=st.session_state.get("_bg_running", False))

    if run_audit:
        from datetime import datetime
        from history.tracker import load_history, save_history, compute_run_diff, compute_weekly_summary
        from audits.pagespeed import run_pagespeed_audit
        from audits.ux import audit_store_ux
        from audits.seo import run_seo_audit
        from audits.products import audit_product_pages
        from audits.checkout import audit_checkout
        from audits.competitors import audit_competitors
        from integrations.woocommerce import get_woo_store_data
        from intelligence.revenue import calculate_revenue_impact
        from intelligence.price import run_price_intelligence
        from reporting.compiler import compile_full_report
        from reporting.pdf_generator import generate_pdf

        store_url = creds["store_url"].rstrip("/")
        history   = load_history()

        modules = [
            ("📱 PageSpeed (mobile)",    lambda: run_pagespeed_audit(store_url, creds["pagespeed_api_key"])),
            ("🖥️ PageSpeed (desktop)",  lambda: run_pagespeed_audit(store_url, creds["pagespeed_api_key"])),
            ("🎨 UX Audit",             lambda: audit_store_ux(store_url)),
            ("🔍 SEO Audit",            lambda: run_seo_audit(store_url)),
            ("📦 Product Pages",        lambda: audit_product_pages(store_url, creds["woo_consumer_key"], creds["woo_consumer_secret"])),
            ("🛒 Checkout Flow",        lambda: audit_checkout(store_url)),
            ("🏆 Competitor Analysis",  lambda: audit_competitors(CONFIG["known_competitors"])),
            ("🛍️ WooCommerce Data",     lambda: get_woo_store_data()),
            ("💰 Revenue Impact",       lambda: calculate_revenue_impact(None, None, None, None, None)),
            ("💲 Price Intelligence",   lambda: run_price_intelligence()),
        ]

        results = {}
        with st.status("Running full audit…", expanded=True) as status:
            for i, (name, fn) in enumerate(modules):
                st.write(f"{name}")
                try:
                    results[name] = fn()
                except Exception as e:
                    results[name] = {"error": str(e)}
                    st.warning(f"⚠️ {name}: {e}")
            st.write("📝 Compiling report…")
            status.update(label="✅ Audit complete!", state="complete")

        pagespeed  = results.get("📱 PageSpeed (mobile)", {})
        ux         = results.get("🎨 UX Audit", {})
        seo        = results.get("🔍 SEO Audit", {})
        products   = results.get("📦 Product Pages", [])
        checkout   = results.get("🛒 Checkout Flow", {})
        comps      = results.get("🏆 Competitor Analysis", [])
        woo_data   = results.get("🛍️ WooCommerce Data", {})
        rev_imp    = results.get("💰 Revenue Impact", {})
        price_int  = results.get("💲 Price Intelligence", {})

        report, overall = compile_full_report(
            store_url, pagespeed, ux, products, checkout,
            comps, seo, woo_data, rev_imp, price_int
        )

        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(CONFIG["output_dir"], f"audit_{ts}.json")
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2)

        history_entry = {
            "date":           datetime.now().strftime("%Y-%m-%d %H:%M"),
            "overall_score":  overall,
            "mobile_speed":   pagespeed.get("mobile", {}).get("performance", 0),
            "ux_score":       ux.get("score", 0),
            "seo_score":      seo.get("score", 0),
            "checkout_score": checkout.get("score", 0),
        }

        run_diff       = compute_run_diff(history, history_entry)
        weekly_summary = compute_weekly_summary(history + [history_entry])
        report["run_diff"]       = run_diff
        report["weekly_summary"] = weekly_summary

        history  = save_history(history, history_entry)
        pdf_path = generate_pdf(report, history[:-1], CONFIG["output_dir"])

        st.session_state["audit_result"] = {
            "report":    report,
            "json_path": json_path,
            "pdf_path":  pdf_path,
            "overall":   overall,
            "pagespeed": pagespeed,
            "ux":        ux,
            "seo":       seo,
            "products":  products,
            "checkout":  checkout,
            "comps":     comps,
        }

    # Show results if we have them
    result = st.session_state.get("audit_result")
    if result:
        overall  = result["overall"]
        pagespeed = result["pagespeed"]
        ux        = result["ux"]
        seo       = result["seo"]
        checkout  = result["checkout"]
        pdf_path  = result["pdf_path"]
        json_path = result["json_path"]

        score_label = (
            "🟢 Excellent" if overall >= 80 else
            "🟡 Good"      if overall >= 60 else
            "🟠 Needs Work" if overall >= 40 else
            "🔴 Critical"
        )

        st.success(f"✅ Audit complete — Overall Score: **{overall}/100** {score_label}")

        cols = st.columns(4)
        with cols[0]:
            mp = pagespeed.get("mobile", {})
            st.metric("Mobile Speed", f"{mp.get('performance', 0)}/100",
                      delta=None)
        with cols[1]:
            st.metric("UX Score", f"{ux.get('score', 0)}/75")
        with cols[2]:
            st.metric("SEO Score", f"{seo.get('score', 0)}/100")
        with cols[3]:
            st.metric("Checkout Score", f"{checkout.get('score', 0)}/70")

        st.divider()
        d1, d2 = st.columns(2)
        with d1:
            if Path(pdf_path).exists():
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF Report", f,
                                       file_name=Path(pdf_path).name,
                                       mime="application/pdf",
                                       use_container_width=True)
        with d2:
            if Path(json_path).exists():
                with open(json_path, "r") as f:
                    st.download_button("📋 Download JSON", f.read().encode(),
                                       file_name=Path(json_path).name,
                                       mime="application/json",
                                       use_container_width=True)

        # Score history chart
        history = load_score_history()
        if history:
            st.divider()
            st.markdown("#### 📈 Score History")
            import pandas as pd
            df = pd.DataFrame(history)
            if "date" in df.columns and "overall_score" in df.columns:
                df = df.tail(10)
                st.line_chart(df.set_index("date")["overall_score"], height=220)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB: PRODUCT DESCRIPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def render_descriptions_tab(creds):
    st.markdown("## ✍️ Product Descriptions")
    st.markdown("Generate SEO-optimised descriptions for WooCommerce products. "
                "Each description is researched from 6 sources and verified against a 13-point QA checklist.")

    # Sub-trigger buttons
    st.markdown("#### 🔍 Research & Write")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

    limit_val = st.number_input("Products per batch", min_value=1, max_value=20, value=5,
                                 label_visibility="collapsed")

    with c1:
        st.caption("Write new descriptions")
        new_btn = st.button("📝 New Products", use_container_width=True,
                            disabled=st.session_state.get("_bg_running", False))
    with c2:
        st.caption("Reformat old descriptions")
        ref_btn = st.button("♻️ Reformat Existing", use_container_width=True,
                            disabled=st.session_state.get("_bg_running", False))
    with c3:
        st.caption("Reformat all with old format")
        all_btn = st.button("🔄 Reformat All", use_container_width=True,
                            disabled=st.session_state.get("_bg_running", False))
    with c4:
        st.caption("Push QA-passed entries live")
        push_disabled = st.session_state.get("_bg_running", False)
        push_btn = st.button("🚀 Push to WooCommerce", use_container_width=True,
                             disabled=push_disabled)

    if new_btn:
        _run_descriptions_workflow(creds, mode="new", limit=limit_val)
    if ref_btn:
        _run_descriptions_workflow(creds, mode="reformat", limit=limit_val)
    if all_btn:
        _run_descriptions_workflow(creds, mode="reformat_all")

    if push_btn:
        _run_push_descriptions(creds)

    # Show current staging if available
    staging = load_staging("descriptions")
    if staging:
        st.divider()
        st.markdown(f"#### 📋 Staging ({len(staging)} products)")
        qa_passed  = sum(1 for p in staging if p.get("qa_passed"))
        qa_failed  = len(staging) - qa_passed
        p1, p2, p3 = st.columns(3)
        p1.metric("Total", len(staging))
        p2.metric("✅ QA Passed", qa_passed)
        p3.metric("❌ QA Failed", qa_failed)

        rows = []
        for p in staging:
            rows.append({
                "Product": p.get("name", ""),
                "Brand": ", ".join(p.get("categories", [])),
                "QA": "✅ PASS" if p.get("qa_passed") else "❌ FAIL",
                "Update Status": p.get("update_status", "pending"),
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        xlsx_files = sorted((PROJECT_ROOT / "audit_reports").glob("product_descriptions_*.xlsx"),
                            reverse=True)
        if xlsx_files:
            latest = xlsx_files[0]
            with open(latest, "rb") as f:
                st.download_button("📥 Download Latest Excel Report", f,
                                   file_name=latest.name,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)


def _run_descriptions_workflow(creds, mode="new", limit=5):
    """Kick off the descriptions workflow — in a real deployment this would call
    the /product-descriptions skill. Here we provide the UI shell."""
    st.info(f"🔍 Starting: {mode} descriptions (limit={limit}). "
            "This workflow runs via Claude Code — use `/product-descriptions` in your terminal.")
    st.markdown("""
    **How to run in Claude Code:**
    ```
    /product-descriptions           # write new descriptions (5 products)
    /product-descriptions 10         # write new for 10 products
    /product-descriptions --reformat 10   # reformat 10 existing products
    /product-descriptions --reformat --all # reformat all old-format products
    ```
    After the Excel report is generated, return here to review and push.
    """)


def _run_push_descriptions(creds):
    """Run push_descriptions.py in a background thread."""
    staging = load_staging("descriptions")
    qa_passed = [p for p in staging if p.get("qa_passed")]
    if not qa_passed:
        st.warning("No QA-passed entries in staging. Run a description batch first.")
        return

    st.warning("⚠️ **Push is destructive** — this will write directly to your WooCommerce store.")
    confirm = st.checkbox("I have reviewed the Excel report and confirm I want to push live.")
    if not confirm:
        return

    def do_push():
        import subprocess
        result = subprocess.run(
            [sys.executable, "tools/push_descriptions.py"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        st.session_state["_push_output"] = result.stdout + result.stderr

    if confirm:
        run_background(do_push)
        poll_until_done()
        output = st.session_state.get("_push_output", "")
        st.code(output or "Push complete.")
        # Refresh
        staging = load_staging("descriptions")
        pushed  = [p for p in staging if p.get("update_status") == "success"]
        failed  = [p for p in staging if p.get("update_status") == "failed"]
        st.success(f"✅ Pushed: {len(pushed)} | Failed: {len(failed)}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: SEO GAPS
# ═══════════════════════════════════════════════════════════════════════════════

def render_seo_tab(creds):
    st.markdown("## 🔍 SEO Gaps")
    st.markdown("Find products missing RankMath SEO metadata and generate SEO titles, "
                "meta descriptions, and image alt text.")

    brand_input = st.text_input("Filter by brand (optional)", placeholder="e.g. BTV, Clive Christian")
    limit_seo   = st.number_input("Products per batch", min_value=1, max_value=50, value=10,
                                   label_visibility="collapsed")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("Find products with no SEO title")
        gap_btn = st.button("🔎 Find SEO Gaps", use_container_width=True,
                           disabled=st.session_state.get("_bg_running", False))
    with c2:
        st.caption("Find SEO gaps filtered by brand")
        brand_btn = st.button("🏷️ Find by Brand", use_container_width=True,
                             disabled=st.session_state.get("_bg_running", False))
    with c3:
        st.caption("Push QA-passed SEO data live")
        push_btn = st.button("🚀 Push SEO Data", use_container_width=True,
                            disabled=st.session_state.get("_bg_running", False))

    if gap_btn:
        _run_seo_workflow(creds, mode="no_seo", limit=limit_seo)
    if brand_btn and brand_input:
        _run_seo_workflow(creds, mode="brand", brand=brand_input, limit=limit_seo)
    if brand_btn and not brand_input:
        st.warning("Enter a brand name to filter by.")

    if push_btn:
        _run_push_seo(creds)

    # Show current staging
    staging = load_staging("seo")
    if staging:
        st.divider()
        st.markdown(f"#### 📋 SEO Staging ({len(staging)} products)")
        qa_passed = sum(1 for p in staging if p.get("qa_passed"))
        qa_failed = len(staging) - qa_passed
        p1, p2, p3 = st.columns(3)
        p1.metric("Total", len(staging))
        p2.metric("✅ QA Passed", qa_passed)
        p3.metric("❌ QA Failed", qa_failed)

        rows = []
        for p in staging:
            rows.append({
                "Product": p.get("name", ""),
                "Brand": ", ".join(p.get("categories", [])),
                "Focus Keyword": p.get("focus_keyword", ""),
                "QA": "✅ PASS" if p.get("qa_passed") else "❌ FAIL",
                "Status": p.get("update_status", "pending"),
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        xlsx_files = sorted((PROJECT_ROOT / "audit_reports").glob("seo_gaps_*.xlsx"),
                            reverse=True)
        if xlsx_files:
            latest = xlsx_files[0]
            with open(latest, "rb") as f:
                st.download_button("📥 Download Latest SEO Excel", f,
                                   file_name=latest.name,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)


def _run_seo_workflow(creds, mode="no_seo", brand=None, limit=10):
    st.info(f"🔍 Starting SEO gaps workflow: mode={mode}, limit={limit}. "
            "Use `/seo-gaps` in Claude Code to run the full pipeline.")
    st.markdown("""
    **How to run in Claude Code:**
    ```
    /seo-gaps                    # find products missing SEO titles (10 products)
    /seo-gaps --no-seo --limit 20  # find 20 products with no SEO
    /seo-gaps --brand "BTV"     # find SEO gaps for brand BTV
    ```
    After the Excel report is generated, return here to review and push.
    """)


def _run_push_seo(creds):
    staging = load_staging("seo")
    qa_passed = [p for p in staging if p.get("qa_passed")]
    if not qa_passed:
        st.warning("No QA-passed entries in staging. Run an SEO batch first.")
        return

    st.warning("⚠️ **Push is destructive** — this will update RankMath meta fields on your WooCommerce products.")
    confirm = st.checkbox("I have reviewed the Excel report and confirm I want to push live.")
    if not confirm:
        return

    def do_push():
        import subprocess
        result = subprocess.run(
            [sys.executable, "tools/push_seo.py"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        st.session_state["_seo_push_output"] = result.stdout + result.stderr

    if confirm:
        run_background(do_push)
        poll_until_done()
        output = st.session_state.get("_seo_push_output", "")
        st.code(output or "Push complete.")
        staging = load_staging("seo")
        pushed  = [p for p in staging if p.get("update_status") == "success"]
        failed  = [p for p in staging if p.get("update_status") == "failed"]
        st.success(f"✅ Pushed: {len(pushed)} | Failed: {len(failed)}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: PRODUCT STATUS
# ═══════════════════════════════════════════════════════════════════════════════

def render_status_tab(creds):
    st.markdown("## 📦 Product Status")
    st.markdown("Overview of all WooCommerce products by description and SEO status.")

    with st.spinner("Fetching product list..."):
        all_prods = []
        page = 1
        while True:
            prods = call_woo_api(f"products?per_page=100&status=publish&page={page}", creds=creds)
            if not prods:
                break
            all_prods.extend(prods)
            page += 1
            if len(prods) < 100:
                break

    total = len(all_prods)
    no_desc   = [p for p in all_prods if not p.get("description", "").strip()]
    no_short  = [p for p in all_prods if not p.get("short_description", "").strip()]
    no_image  = [p for p in all_prods if not p.get("images")]
    no_stock  = [p for p in all_prods if p.get("stock_status") == "outofstock"]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Products", total)
    c2.metric("❌ No Description", len(no_desc))
    c3.metric("⚠️ No Short Desc", len(no_short))
    c4.metric("🖼️ No Images", len(no_image))
    c5.metric("📦 Out of Stock", len(no_stock))

    st.divider()

    tab_no_desc, tab_reformat, tab_all = st.tabs(["Missing Descriptions", "Needs Reformat", "All Products"])

    with tab_no_desc:
        if no_desc:
            rows = [{"ID": p["id"], "Name": p["name"],
                    "Price": p.get("price", ""), "Stock": p.get("stock_status", "")}
                    for p in no_desc]
            import pandas as pd
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.success("✅ All products have descriptions!")

    with tab_reformat:
        needs_ref = [p for p in all_prods
                     if p.get("description") and "<h3>" not in p.get("description", "")]
        if needs_ref:
            rows = [{"ID": p["id"], "Name": p["name"],
                    "Price": p.get("price", ""), "Categories": ", ".join(c["name"] for c in p.get("categories", []))}
                    for p in needs_ref]
            import pandas as pd
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("No products need reformatting — all descriptions are in the new SEO format.")

    with tab_all:
        rows = [{"ID": p["id"], "Name": p["name"],
                "Price": p.get("price", ""),
                "Has Desc": "✅" if p.get("description", "").strip() else "❌",
                "Has Short": "✅" if p.get("short_description", "").strip() else "❌",
                "Images": len(p.get("images", [])),
                "Stock": p.get("stock_status", "")}
                for p in all_prods[:100]]
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        if total > 100:
            st.caption(f"Showing first 100 of {total} products.")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

st.title("✨ Scentified Marketing Suite")
st.caption(f"Store: {get_creds()['store_url']}  |  Today: {datetime.now().strftime('%d %B %Y')}")

tab_audit, tab_desc, tab_seo, tab_status = st.tabs(
    ["📊 Audit", "✍️ Descriptions", "🔍 SEO Gaps", "📦 Status"]
)

with tab_audit:
    render_audit_tab(creds)
with tab_desc:
    render_descriptions_tab(creds)
with tab_seo:
    render_seo_tab(creds)
with tab_status:
    render_status_tab(creds)
