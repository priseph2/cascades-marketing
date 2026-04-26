# Scentified eCommerce Audit

Run the full eCommerce audit for scentifiedperfume.com and produce a scored report.

## Steps

1. Run the audit script from the project root:

```bash
cd "C:/Users/princ/Downloads/cascades-marketing" && py main.py
```

2. Wait for it to complete — it runs 9 audits in sequence (allow up to 3 minutes).

3. When done, display a formatted summary:

```
=== SCENTIFIED AUDIT COMPLETE ===

Overall Score:  [X]/100  ([Critical / Needs Work / Good])
vs Last Run:    [▲/▼ X pts] (or "First run")

Score Breakdown:
  Mobile Speed:    [XX]/100
  Desktop Speed:   [XX]/100
  Store UX:        [XX]/100
  SEO:             [XX]/100
  Products (avg):  [XX]/100
  Checkout:        [XX]/100

Top Issues Found:
  1. [highest priority issue]
  2. [second priority issue]
  3. [third priority issue]

Files Generated:
  JSON:  audit_reports/audit_<timestamp>.json
  PDF:   audit_reports/scentified_audit_v2_<timestamp>.pdf
```

4. If the script fails, show the full error and diagnose the cause (missing dependency, network error, API key issue, etc.).

## Notes

- Entry point: `main.py`
- Config & credentials: `config.py`
- All output goes to `audit_reports/`
- Score history: `audit_reports/score_history.json`
