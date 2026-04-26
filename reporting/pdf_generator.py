import os
import math
from datetime import datetime
from config import CONFIG
from intelligence.price import BRAND_PRICE_MAP
from utils.helpers import log, sl, ngn


def generate_pdf(report, history, output_dir):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as rcolors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, PageBreak, KeepTogether, Flowable)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
    from reportlab.graphics import renderPDF

    GOLD     = rcolors.HexColor("#C9A84C")
    DARK     = rcolors.HexColor("#0D0D0D")
    CHARCOAL = rcolors.HexColor("#1A1A1A")
    LBGR     = rcolors.HexColor("#F5F0E8")
    MGRAY    = rcolors.HexColor("#6B6B6B")
    WHITE    = rcolors.white
    RED      = rcolors.HexColor("#D94040")
    GREEN    = rcolors.HexColor("#3A9E5F")
    AMBER    = rcolors.HexColor("#E8943A")
    BLUE     = rcolors.HexColor("#4A90D9")
    CW       = 170 * mm

    def scol(s):
        return GREEN if s >= 80 else (AMBER if s >= 50 else RED)

    def mst(n="Normal", **kw):
        b = getSampleStyleSheet().get(n, getSampleStyleSheet()["Normal"])
        return ParagraphStyle(f"p{abs(hash(frozenset(kw.items())))}", parent=b, **kw)

    TH_L  = mst(fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_LEFT)
    TH_C  = mst(fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
    BODY  = mst(fontSize=9,  textColor=CHARCOAL, fontName="Helvetica",      spaceAfter=3, leading=14)
    SM    = mst(fontSize=8,  textColor=MGRAY,    fontName="Helvetica",      spaceAfter=2, leading=12)
    H1    = mst(fontSize=15, textColor=GOLD,     fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=5)
    H2    = mst(fontSize=11, textColor=CHARCOAL, fontName="Helvetica-Bold", spaceBefore=6,  spaceAfter=3)
    OK    = mst(fontSize=9,  textColor=GREEN,    fontName="Helvetica-Bold")
    ERR   = mst(fontSize=9,  textColor=RED,      fontName="Helvetica-Bold")
    SOL   = mst(fontSize=9,  textColor=BLUE,     fontName="Helvetica-Bold", leading=13)

    def hr():
        return HRFlowable(width=CW, thickness=0.5, color=GOLD, spaceAfter=6, spaceBefore=6)

    def score_banner(label, score):
        col = scol(score)
        lbl = sl(score)
        row = [[
            Paragraph(label, H2),
            Paragraph(f"{score}/100", mst(fontSize=16, textColor=col, fontName="Helvetica-Bold", alignment=TA_RIGHT)),
            Paragraph(lbl, mst(fontSize=9, textColor=col, fontName="Helvetica-Bold", alignment=TA_RIGHT)),
        ]]
        t = Table(row, colWidths=[90*mm, 45*mm, 35*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LBGR),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (0,0),   8),
            ("ROUNDEDCORNERS", [4]),
        ]))
        return t

    def findings_table(items, col_w=CW):
        header = [Paragraph("", TH_C), Paragraph("FINDING", TH_L), Paragraph("SOLUTION", TH_L)]
        rows   = [header]
        for item in items:
            kind = item[0]; text_ = item[1]; sol = item[2] if len(item) > 2 else "—"
            if kind == "pass":
                rows.append([Paragraph("✓", OK), Paragraph(text_, BODY), Paragraph("—", SM)])
            else:
                rows.append([Paragraph("✗", ERR), Paragraph(text_, BODY), Paragraph(f"→ {sol}", SOL)])
        ca = 6*mm; cb = col_w * 0.43; cc = col_w - ca - cb
        t = Table(rows, colWidths=[ca, cb, cc])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),  (-1,0),  DARK),
            ("ROWBACKGROUNDS",(0,1),  (-1,-1), [WHITE, LBGR]),
            ("GRID",          (0,0),  (-1,-1), 0.25, rcolors.HexColor("#E0D8CC")),
            ("VALIGN",        (0,0),  (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0),  (-1,-1), 4),
            ("BOTTOMPADDING", (0,0),  (-1,-1), 4),
            ("LEFTPADDING",   (1,0),  (2,-1),  5),
        ]))
        return t

    def score_trend_chart(history, current_score, w=CW, h=55*mm):
        d          = Drawing(w, h)
        runs       = history[-7:] if len(history) >= 7 else history
        all_scores = [e.get("overall_score", 0) for e in runs] + [current_score]
        all_labels = [e.get("date", "")[:10] for e in runs] + ["Today"]
        n          = len(all_scores)
        pad        = 20; bar_area_w = float(w) - 2*pad; bar_area_h = float(h) - 30
        bar_w      = bar_area_w / (n * 1.5)
        spacing    = bar_area_w / n
        d.add(Line(pad, 20, pad, float(h)-10, strokeColor=rcolors.HexColor("#444"), strokeWidth=0.5))
        d.add(Line(pad, 20, float(w)-pad, 20, strokeColor=rcolors.HexColor("#444"), strokeWidth=0.5))
        for val in [25, 50, 75, 100]:
            y = 20 + (val/100)*bar_area_h
            d.add(Line(pad, y, float(w)-pad, y, strokeColor=rcolors.HexColor("#333"), strokeWidth=0.3, strokeDashArray=[2,3]))
            d.add(String(2, y-3, str(val), fontSize=6, fillColor=rcolors.HexColor("#666"), fontName="Helvetica"))
        for i, (score, label) in enumerate(zip(all_scores, all_labels)):
            x   = pad + i*spacing + spacing/2 - bar_w/2
            bh  = (score/100)*bar_area_h
            col = GREEN if score >= 80 else (AMBER if score >= 50 else RED)
            if i == len(all_scores) - 1:
                d.add(Rect(x-1, 20, bar_w+2, bh, fillColor=col, strokeColor=GOLD, strokeWidth=1))
            else:
                d.add(Rect(x, 20, bar_w, bh, fillColor=col, strokeColor=rcolors.HexColor("#333"), strokeWidth=0.3))
            d.add(String(x + bar_w/2, 20+bh+2, str(score), fontSize=6, fillColor=WHITE, fontName="Helvetica-Bold", textAnchor="middle"))
            short = label[-5:] if len(label) > 5 else label
            d.add(String(x + bar_w/2, 8, short, fontSize=5.5, fillColor=rcolors.HexColor("#888"), fontName="Helvetica", textAnchor="middle"))
        return d

    def radar_chart(scores_dict, w=80*mm, h=80*mm):
        d      = Drawing(float(w), float(h))
        cx     = float(w)/2; cy = float(h)/2
        r_max  = min(cx, cy) - 15
        items  = list(scores_dict.items())
        n      = len(items)
        if n < 3:
            return d
        angles = [math.pi/2 + 2*math.pi*i/n for i in range(n)]
        for ring in [0.25, 0.5, 0.75, 1.0]:
            pts = []
            for a in angles:
                pts += [cx + r_max*ring*math.cos(a), cy + r_max*ring*math.sin(a)]
            pts += [pts[0], pts[1]]
            for j in range(0, len(pts)-2, 2):
                d.add(Line(pts[j], pts[j+1], pts[j+2], pts[j+3], strokeColor=rcolors.HexColor("#333"), strokeWidth=0.4))
        for a in angles:
            d.add(Line(cx, cy, cx+r_max*math.cos(a), cy+r_max*math.sin(a), strokeColor=rcolors.HexColor("#444"), strokeWidth=0.4))
        data_pts = []
        for i, (label, score) in enumerate(items):
            a = angles[i]; r = r_max*(score/100)
            data_pts += [cx+r*math.cos(a), cy+r*math.sin(a)]
        poly_pts = list(zip(data_pts[0::2], data_pts[1::2]))
        for j in range(len(poly_pts)):
            x1,y1 = poly_pts[j]; x2,y2 = poly_pts[(j+1)%len(poly_pts)]
            d.add(Line(x1, y1, x2, y2, strokeColor=GOLD, strokeWidth=1.5))
        for i, (label, score) in enumerate(items):
            a  = angles[i]; r = r_max*(score/100)
            px = cx+r*math.cos(a); py = cy+r*math.sin(a)
            d.add(Circle(px, py, 3, fillColor=GOLD, strokeColor=DARK, strokeWidth=0.5))
            lx = cx+(r_max+10)*math.cos(a); ly = cy+(r_max+10)*math.sin(a)
            d.add(String(lx, ly, f"{label[:12]}\n{score}", fontSize=6, fillColor=WHITE, fontName="Helvetica-Bold", textAnchor="middle"))
        return d

    class DrawingFlowable(Flowable):
        def __init__(self, d):
            self.drawing = d; self.width = d.width; self.height = d.height
        def draw(self):
            renderPDF.draw(self.drawing, self.canv, 0, 0)

    # ── BUILD PDF ──────────────────────────────────────────────
    os.makedirs(output_dir, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(output_dir, f"scentified_audit_v2_{ts}.pdf")
    doc      = SimpleDocTemplate(pdf_path, pagesize=A4,
                   leftMargin=20*mm, rightMargin=20*mm,
                   topMargin=15*mm, bottomMargin=15*mm)
    story = []

    # Cover
    story.append(Spacer(1, 18*mm))
    banner = Table([[Paragraph("SCENTIFIED PERFUME", mst(fontSize=26, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER))]], colWidths=[CW])
    banner.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),("ROUNDEDCORNERS",[6])]))
    story.append(banner)
    story.append(Spacer(1, 3*mm))
    sub = Table([[Paragraph("PHASE 1 — ENHANCED STORE AUDIT  v2.0", mst(fontSize=12, textColor=CHARCOAL, fontName="Helvetica", alignment=TA_CENTER))]], colWidths=[CW])
    sub.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story.append(sub)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("scentifiedperfume.com", mst(fontSize=10, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph(f"Generated: {report['meta']['generated_at']}", mst(fontSize=10, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)))
    story.append(Spacer(1, 8*mm))

    ov     = report["overall_score"]; ov_col = scol(ov)
    ov_tbl = Table([
        [Paragraph("OVERALL AUDIT SCORE", mst(fontSize=11, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER))],
        [Paragraph(str(ov), mst(fontSize=52, textColor=ov_col, fontName="Helvetica-Bold", alignment=TA_CENTER))],
        [Paragraph(f"out of 100  —  {sl(ov)}", mst(fontSize=10, textColor=MGRAY, alignment=TA_CENTER))],
    ], colWidths=[CW])
    ov_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),LBGR),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),("ROUNDEDCORNERS",[8]),("BOX",(0,0),(-1,-1),1.5,ov_col)]))
    story.append(ov_tbl)

    if history:
        last  = history[-1]
        diff  = ov - last.get("overall_score", ov)
        arrow = "▲" if diff > 0 else ("▼" if diff < 0 else "—")
        col   = GREEN if diff > 0 else (RED if diff < 0 else MGRAY)
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(
            f"{arrow} {abs(diff)} points {'up' if diff>0 else 'down' if diff<0 else 'unchanged'} from last audit ({last.get('date','')[:10]})",
            mst(fontSize=10, textColor=col, fontName="Helvetica-Bold", alignment=TA_CENTER)
        ))

    story.append(Spacer(1, 6*mm))

    ps_mob = report["pagespeed"].get("mobile",  {}).get("performance", 0)
    ps_dsk = report["pagespeed"].get("desktop", {}).get("performance", 0)
    ux_s   = report["ux_audit"].get("score", 0)
    co_s   = report["checkout"].get("score", 0)
    seo_s  = report["seo_audit"].get("score", 0)
    pp_s   = round(sum(p["score"] for p in report["product_pages"]) / len(report["product_pages"])) if report["product_pages"] else 0

    sum_rows = [[Paragraph("AREA", TH_C), Paragraph("SCORE", TH_C), Paragraph("STATUS", TH_C)]]
    for area, s_ in [("Mobile Speed", ps_mob), ("Desktop Speed", ps_dsk), ("Store UX", ux_s), ("SEO", seo_s), ("Product Pages (avg)", pp_s), ("Checkout", co_s)]:
        sum_rows.append([
            Paragraph(area, BODY),
            Paragraph(str(s_), mst(fontSize=10, textColor=scol(s_), fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(sl(s_), mst(fontSize=9,  textColor=scol(s_), fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ])
    st_ = Table(sum_rows, colWidths=[90*mm, 40*mm, 40*mm])
    st_.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8),("ROUNDEDCORNERS",[4])]))
    story.append(st_)
    story.append(PageBreak())

    # Score trend + radar
    story.append(Paragraph("PERFORMANCE TRACKING", H1))
    story.append(hr())
    story.append(Paragraph("Score history across all audit runs — track your progress over time.", BODY))
    story.append(Spacer(1, 3*mm))
    story.append(DrawingFlowable(score_trend_chart(history, ov, w=CW, h=55*mm)))
    story.append(Spacer(1, 4*mm))

    radar_scores = {"Mobile Speed": ps_mob, "Desktop": ps_dsk, "UX": ux_s, "SEO": seo_s, "Products": pp_s, "Checkout": co_s}
    radar        = radar_chart(radar_scores, w=80*mm, h=70*mm)
    radar_tbl    = Table([[DrawingFlowable(radar),
        Paragraph("The radar chart shows your performance across all 6 audit dimensions. A perfect score would fill the entire hexagon. Currently the store has significant gaps in Speed and Products which are your highest leverage areas to fix first.",
                  mst(fontSize=9, textColor=CHARCOAL, fontName="Helvetica", leading=14))]],
        colWidths=[82*mm, 88*mm])
    radar_tbl.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(1,0),(1,0),8)]))
    story.append(radar_tbl)
    story.append(Spacer(1, 5*mm))

    # Run-over-run diff
    rd = report.get("run_diff", {})
    if rd.get("available"):
        story.append(Paragraph("SCORE CHANGE — THIS RUN VS LAST RUN", H2))
        rd_header = [Paragraph("METRIC",TH_L), Paragraph("LAST RUN",TH_C), Paragraph("THIS RUN",TH_C), Paragraph("CHANGE",TH_C)]
        rd_rows   = [rd_header]
        for m, d in rd["diffs"].items():
            delta = d["delta"]
            col   = GREEN if delta > 0 else (RED if delta < 0 else MGRAY)
            rd_rows.append([
                Paragraph(d["label"], BODY),
                Paragraph(str(d["previous"]), mst(fontSize=9, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)),
                Paragraph(str(d["current"]),  mst(fontSize=9, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(f"{d['arrow']} {abs(delta)}" if delta != 0 else "—",
                          mst(fontSize=9, textColor=col, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            ])
        rd_t = Table(rd_rows, colWidths=[70*mm, 33*mm, 33*mm, 34*mm])
        rd_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
        story.append(rd_t)
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(rd["summary"], SM))
    story.append(PageBreak())

    # Weekly summary
    ws = report.get("weekly_summary", {})
    story.append(Paragraph("WEEKLY PERFORMANCE SUMMARY", H1))
    story.append(hr())
    if not ws.get("available"):
        story.append(Paragraph(ws.get("note", "Weekly summary not yet available — run the audit again next week to see week-over-week comparison."), BODY))
    else:
        health_col = GREEN if "Strong" in ws["health"] else (AMBER if "Marginal" in ws["health"] or "No change" in ws["health"] else RED)
        story.append(Paragraph(ws["health"], mst(fontSize=14, textColor=health_col, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)))
        story.append(Paragraph(f"Comparison period: {ws['week_start']}  →  {ws['week_end']}", SM))
        story.append(Spacer(1, 4*mm))
        ws_header = [Paragraph("METRIC",TH_L), Paragraph("LAST WEEK",TH_C), Paragraph("THIS WEEK",TH_C), Paragraph("CHANGE",TH_C), Paragraph("% CHANGE",TH_C)]
        ws_rows   = [ws_header]
        for m, d in ws["diffs"].items():
            delta = d["delta"]
            col   = GREEN if delta > 0 else (RED if delta < 0 else MGRAY)
            pct   = f"{'+' if d['pct_change']>0 else ''}{d['pct_change']}%"
            ws_rows.append([
                Paragraph(d["label"], BODY),
                Paragraph(str(d["last_week"]), mst(fontSize=9, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)),
                Paragraph(str(d["this_week"]), mst(fontSize=9, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(f"{d['arrow']} {abs(delta)}" if delta != 0 else "—", mst(fontSize=9, textColor=col, fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(pct, mst(fontSize=9, textColor=col, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            ])
        ws_t = Table(ws_rows, colWidths=[55*mm, 28*mm, 28*mm, 28*mm, 31*mm])
        ws_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
        story.append(ws_t)
        story.append(Spacer(1, 6*mm))
        story.append(Paragraph("WHAT MOVED THIS WEEK", H2))
        best  = ws.get("top_improvement", "")
        worst = ws.get("top_decline", "")
        story.append(Paragraph(f"Biggest improvement: {best}" if best else "No improvements recorded.", mst(fontSize=10, textColor=GREEN, fontName="Helvetica-Bold")))
        if worst:
            story.append(Paragraph(f"Biggest decline: {worst} — investigate immediately.", mst(fontSize=10, textColor=RED, fontName="Helvetica-Bold")))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("This summary is also saved as weekly_summary.json in your audit_reports folder. Share it with your team every Monday as a progress tracker.", SM))
    story.append(PageBreak())

    # Revenue impact
    ri = report["revenue_impact"]
    story.append(Paragraph("REVENUE IMPACT ESTIMATES", H1))
    story.append(hr())
    story.append(Paragraph(f"Based on {ri['assumptions']['monthly_visitors']:,} monthly visitors, {ri['assumptions']['current_cr_pct']} baseline conversion rate, and {ri['assumptions']['avg_order_value']} average order value.", BODY))
    curr_rev = ri["current_estimated_monthly_ngn"]
    pot_lift = ri["total_potential_uplift_ngn"]
    rev_sum  = Table([[
        Paragraph("Est. Current Monthly Revenue",  mst(fontSize=10, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)),
        Paragraph("Potential Monthly Uplift",       mst(fontSize=10, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)),
    ],[
        Paragraph(ngn(curr_rev), mst(fontSize=20, textColor=AMBER, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"+{ngn(pot_lift)}", mst(fontSize=20, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]], colWidths=[85*mm, 85*mm])
    rev_sum.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),LBGR),("GRID",(0,0),(-1,-1),0.5,rcolors.HexColor("#E0D8CC")),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),("ROUNDEDCORNERS",[6])]))
    story.append(Spacer(1, 4*mm))
    story.append(rev_sum)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Note: Estimates based on luxury eCommerce industry benchmarks. Actual results depend on implementation quality and market conditions.", SM))
    story.append(Spacer(1, 4*mm))
    ri_header = [Paragraph("FIX",TH_L), Paragraph("CR LIFT",TH_C), Paragraph("EST. MONTHLY ₦",TH_C), Paragraph("EFFORT",TH_C), Paragraph("PRIORITY",TH_C)]
    ri_rows   = [ri_header]
    pri_c     = {"Critical": RED, "High": AMBER, "Medium": GOLD}
    for item in ri["items"]:
        ri_rows.append([
            Paragraph(item["fix"],       BODY),
            Paragraph(item["cr_lift"],   mst(fontSize=9, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(ngn(item["monthly_ngn"]), mst(fontSize=9, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(item["effort"],    SM),
            Paragraph(item["priority"],  mst(fontSize=8, textColor=pri_c.get(item["priority"], GOLD), fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ])
    ri_t = Table(ri_rows, colWidths=[55*mm, 22*mm, 28*mm, 40*mm, 25*mm])
    ri_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),5)]))
    story.append(ri_t)
    story.append(PageBreak())

    # Speed audit
    story.append(Paragraph("SPEED & PERFORMANCE AUDIT", H1))
    story.append(hr())
    for strategy, label in [("mobile", "Mobile"), ("desktop", "Desktop")]:
        sd = report["pagespeed"].get(strategy, {})
        if "error" in sd:
            story.append(Paragraph(f"{label}: Data unavailable — {sd['error']}", BODY))
            continue
        perf = sd.get("performance", 0)
        story.append(KeepTogether([score_banner(f"{label} Performance", perf), Spacer(1, 3*mm)]))
        metrics  = [["METRIC","VALUE"],["Largest Contentful Paint (LCP)",sd.get("lcp","N/A")],["Total Blocking Time (TBT)",sd.get("tbt","N/A")],["Cumulative Layout Shift (CLS)",sd.get("cls","N/A")],["Speed Index",sd.get("speed_index","N/A")],["SEO Score",str(sd.get("seo","N/A"))],["Accessibility",str(sd.get("accessibility","N/A"))]]
        mt_rows  = []
        for i, row in enumerate(metrics):
            if i == 0:
                mt_rows.append([Paragraph(row[0], TH_L), Paragraph(row[1], TH_C)])
            else:
                mt_rows.append([Paragraph(row[0], BODY), Paragraph(str(row[1]), mst(fontSize=9, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_RIGHT))])
        mt = Table(mt_rows, colWidths=[120*mm, 50*mm])
        mt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),6)]))
        story.append(mt)
        story.append(Spacer(1, 5*mm))

    speed_items = [
        ("pass",  "HTTPS/SSL active — secure connection confirmed"),
        ("pass",  "Server responds and site is publicly accessible"),
        ("issue", "Mobile performance ~22/100 — pages take 8-15s on mobile",               "Install WP Rocket (₦30k/yr) or LiteSpeed Cache (free). Enable page caching, lazy loading, and GZIP. Target: 70+ within 2 weeks."),
        ("issue", "RevSlider hero plugin loading dummy images — major render-blocker",       "Remove RevSlider entirely. Replace with a static HTML/CSS hero section. RevSlider adds 400KB+ overhead on every page load."),
        ("issue", "No image compression — PNG/JPG files instead of WebP",                   "Install Imagify or ShortPixel plugin. Bulk-convert all existing images to WebP. Enable lazy loading for below-fold images. Expected page weight reduction: 50-65%."),
        ("issue", "No CDN detected — all assets served from single origin",                  "Sign up for Cloudflare free plan at cloudflare.com. Point your domain through Cloudflare. Enables global CDN, free SSL, and DDoS protection. Setup: 30 minutes."),
        ("issue", "Multiple render-blocking JavaScript files",                               "In WP Rocket: enable 'Delay JavaScript Execution'. Defer all non-critical JS. This alone can improve mobile score by 10-15 points."),
    ]
    story.append(findings_table(speed_items))
    story.append(PageBreak())

    # SEO audit
    seo = report["seo_audit"]
    story.append(Paragraph("SEO KEYWORD AUDIT", H1))
    story.append(hr())
    story.append(score_banner("SEO Score", seo.get("score", 0)))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Target Keyword Presence on Homepage", H2))
    kw_header = [Paragraph("KEYWORD",TH_L), Paragraph("FOUND ON HOMEPAGE",TH_C), Paragraph("ACTION",TH_L)]
    kw_rows   = [kw_header]
    for kw, found in seo.get("keyword_presence", {}).items():
        kw_rows.append([
            Paragraph(kw, BODY),
            Paragraph("✓ Yes" if found else "✗ No", mst(fontSize=9, textColor=GREEN if found else RED, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("—" if found else "Add this keyword naturally in homepage copy, H2 tags, or product category descriptions.", SM),
        ])
    kw_t = Table(kw_rows, colWidths=[55*mm, 30*mm, 85*mm])
    kw_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
    story.append(kw_t)
    story.append(Spacer(1, 5*mm))
    seo_items  = [("pass", x) for x in seo.get("passes", [])]
    seo_items += [("issue", x[0], x[1]) if isinstance(x, tuple) else ("issue", x, "See Yoast SEO plugin.") for x in seo.get("issues", [])]
    if seo_items:
        story.append(findings_table(seo_items))
    story.append(PageBreak())

    # UX audit
    ux = report["ux_audit"]
    story.append(Paragraph("STORE UX AUDIT", H1))
    story.append(hr())
    story.append(score_banner("Homepage & UX", ux.get("score", 0)))
    story.append(Spacer(1, 4*mm))
    ux_items  = [("pass", x) for x in ux.get("passes", [])]
    ux_items += [("issue", x[0], x[1]) if isinstance(x, tuple) else ("issue", x, "See recommendations.") for x in ux.get("issues", [])]
    story.append(findings_table(ux_items))
    if ux.get("seo"):
        s = ux["seo"]
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(f"Page Title: {s.get('title','Not found')[:80]}", SM))
        story.append(Paragraph(f"Meta Desc: {'Present' if s.get('has_meta_description') else 'Missing — add via Yoast SEO'}", SM))
    story.append(PageBreak())

    # Product pages
    story.append(Paragraph("PRODUCT PAGE AUDIT", H1))
    story.append(hr())
    if not report["product_pages"]:
        story.append(Paragraph("No product pages audited. Add WooCommerce API credentials to enable this section.", BODY))
    else:
        for i, page in enumerate(report["product_pages"]):
            story.append(KeepTogether([
                Paragraph(f"{i+1}. {page.get('title', page.get('url',''))[:70]}", H2),
                score_banner("Product Page Score", page["score"]),
                Spacer(1, 2*mm),
            ]))
            pp_items  = [("pass", x) for x in page.get("passes", [])]
            pp_items += [("issue", x[0], x[1]) if isinstance(x, tuple) else ("issue", x, "Fix as per audit recommendations.") for x in page.get("issues", [])]
            story.append(findings_table(pp_items))
            story.append(Spacer(1, 5*mm))
    story.append(PageBreak())

    # Checkout
    co = report["checkout"]
    story.append(Paragraph("CHECKOUT FLOW AUDIT", H1))
    story.append(hr())
    story.append(score_banner("Checkout Score", co.get("score", 0)))
    story.append(Spacer(1, 4*mm))
    co_items  = [("pass", x) for x in co.get("passes", [])]
    co_items += [("issue", x[0], x[1]) if isinstance(x, tuple) else ("issue", x, "Fix immediately.") for x in co.get("issues", [])]
    story.append(findings_table(co_items))
    story.append(PageBreak())

    # Competitor analysis
    story.append(Paragraph("COMPETITOR ANALYSIS", H1))
    story.append(hr())
    comp_header     = [Paragraph("FEATURE",TH_L), Paragraph("SCENTIFIED",TH_C), Paragraph("FRAGRANCES.COM.NG",TH_C), Paragraph("EDGARS.CO.ZA",TH_C)]
    feat_rows_data  = [
        ("Structured Frag. Notes","Partial","Yes","Yes"),
        ("Multiple Images (3+)","Partial","Yes","Yes"),
        ("Customer Reviews","No","Yes","Yes"),
        ("Local Currency Default","No","Yes","N/A"),
        ("WhatsApp Contact","No","Yes","No"),
        ("Newsletter","Yes","Yes","Yes"),
        ("Discovery/Sample Sets","No","Partial","Yes"),
        ("Bundle/Gift Sets","No","No","Yes"),
        ("Free Delivery","No","Yes","Yes"),
        ("Mobile Speed","Poor","Average","Good"),
        ("Video Content","No","No","Partial"),
        ("Loyalty Programme","No","No","Yes"),
        ("Abandoned Cart","No","Unknown","Yes"),
        ("Payment Trust Icons","No","Yes","Yes"),
    ]
    STATUS_COL = {"Yes": GREEN, "No": RED, "Partial": AMBER, "Poor": RED, "Average": AMBER, "Good": GREEN, "Unknown": MGRAY, "N/A": MGRAY}
    comp_rows  = [comp_header]
    for feat, s1, s2, s3 in feat_rows_data:
        def cp(v):
            return Paragraph(v, mst(fontSize=9, textColor=STATUS_COL.get(v, CHARCOAL), fontName="Helvetica-Bold", alignment=TA_CENTER))
        comp_rows.append([Paragraph(feat, BODY), cp(s1), cp(s2), cp(s3)])
    comp_t = Table(comp_rows, colWidths=[62*mm, 36*mm, 38*mm, 34*mm])
    comp_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
    story.append(comp_t)
    story.append(PageBreak())

    # Price intelligence
    pi = report["price_intel"]
    story.append(Paragraph("COMPETITOR PRICE INTELLIGENCE", H1))
    story.append(hr())
    story.append(Paragraph(f"Exchange rate used: $1 = ₦{pi['rate_used']:,}. {pi['insight']}", BODY))
    story.append(Spacer(1, 4*mm))
    for brand in BRAND_PRICE_MAP.keys():
        brand_prods = [r for r in pi["comparison"] if r["brand"] == brand]
        if not brand_prods:
            continue
        story.append(Paragraph(brand, H2))
        bp_header = [Paragraph("PRODUCT",TH_L), Paragraph("YOUR USD",TH_C), Paragraph("YOUR NGN",TH_C), Paragraph("COMP. EST. NGN",TH_C), Paragraph("POSITION",TH_C)]
        bp_rows   = [bp_header]
        for row in brand_prods:
            pos_col = GREEN if row["positioning"] == "Competitive" else AMBER
            bp_rows.append([
                Paragraph(row["product"],                  BODY),
                Paragraph(f"${row['your_price_usd']:,.2f}", SM),
                Paragraph(ngn(row["your_price_ngn"]),       mst(fontSize=9, textColor=GOLD,    fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(ngn(row["comp_est_ngn"]),         mst(fontSize=9, textColor=MGRAY,   fontName="Helvetica",      alignment=TA_CENTER)),
                Paragraph(row["positioning"],               mst(fontSize=8, textColor=pos_col, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            ])
        bp_t = Table(bp_rows, colWidths=[55*mm, 22*mm, 30*mm, 32*mm, 31*mm])
        bp_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),5)]))
        story.append(bp_t)
        story.append(Spacer(1, 5*mm))
    story.append(Paragraph(f"Note: {pi['note']}", SM))
    story.append(PageBreak())

    # WooCommerce store data
    if report.get("woo_data"):
        wd = report["woo_data"]
        story.append(Paragraph("WOOCOMMERCE STORE DATA", H1))
        story.append(hr())
        woo_items = [
            [Paragraph("METRIC", TH_L), Paragraph("VALUE", TH_C)],
            [Paragraph("Total Products", BODY),            Paragraph(str(wd.get("total_products","N/A")),  mst(fontSize=10, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Orders This Month", BODY),         Paragraph(str(wd.get("orders_this_month","N/A")), mst(fontSize=10, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Revenue This Month", BODY),        Paragraph(ngn(wd.get("revenue_ngn_this_month",0)), mst(fontSize=10, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Avg Order Value", BODY),           Paragraph(ngn(wd.get("aov_ngn",0)),             mst(fontSize=10, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Products w/o Images", BODY),       Paragraph(str(len(wd.get("products_no_image",[]))),       mst(fontSize=10, textColor=RED if wd.get("products_no_image") else GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Products w/o Description", BODY),  Paragraph(str(len(wd.get("products_no_description",[]))), mst(fontSize=10, textColor=RED if wd.get("products_no_description") else GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Out of Stock", BODY),              Paragraph(str(len(wd.get("out_of_stock",[]))),  mst(fontSize=10, textColor=RED if wd.get("out_of_stock") else GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph("Products w/ Zero Reviews", BODY),  Paragraph(str(len(wd.get("products_no_reviews",[]))), mst(fontSize=10, textColor=RED if wd.get("products_no_reviews") else GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER))],
        ]
        woo_t = Table(woo_items, colWidths=[120*mm, 50*mm])
        woo_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8)]))
        story.append(woo_t)
        story.append(PageBreak())

    # 60-day roadmap
    story.append(Paragraph("60-DAY FIX ROADMAP", H1))
    story.append(hr())
    road_header = [Paragraph("WK",TH_C), Paragraph("TASK",TH_L), Paragraph("WHO",TH_C), Paragraph("₦ IMPACT",TH_C), Paragraph("PRI",TH_C)]
    roadmap = [
        ("1","Run full test purchase — fix checkout 503 errors","Dev","Critical","Critical"),
        ("1","Switch all prices to ₦ Naira (Currency Switcher plugin)","Dev",f"+{ngn(round(500*0.005*0.12*220000))}","Critical"),
        ("1","Install WP Rocket + page caching + lazy loading","Dev",f"+{ngn(round(500*0.20*220000*0.005))}","Critical"),
        ("1","Remove RevSlider — replace with static hero image","Dev/Design","Speed fix","High"),
        ("1","Fix footer placeholder email","Dev","Trust fix","High"),
        ("2","Set up Cloudflare free CDN","Dev","Speed fix","High"),
        ("2","Bulk-convert images to WebP (Imagify plugin)","Dev","Speed fix","High"),
        ("2","Add WhatsApp floating button","Dev","Conversion","High"),
        ("2","Fix or remove broken nav links","Dev","UX fix","Medium"),
        ("2","Add payment trust icons to homepage + checkout","Dev","Trust","High"),
        ("3","Rewrite all product pages — Top/Heart/Base notes","Marketing","CR lift","High"),
        ("3","Add longevity + projection to all products","Marketing","CR lift","High"),
        ("3","Add 'Best For' occasion section to all products","Marketing","CR lift","High"),
        ("4","Shoot 5-image sets for top 10 products","Photographer","CR lift","High"),
        ("4","Set up Klaviyo abandoned cart sequence (3 emails)","Marketing",f"+{ngn(round(500*0.07*0.12*220000))}","High"),
        ("4","Enable guest checkout in WooCommerce","Dev",f"+{ngn(round(500*0.005*0.25*220000))}","High"),
        ("4","Install Yoast SEO — add meta descriptions","Marketing","SEO","Medium"),
        ("5","Collect reviews — email past in-store customers","Marketing",f"+{ngn(round(500*0.005*0.18*220000))}","High"),
        ("5","Create Discovery Kit product (5 x 2ml samples @ ₦15k)","Operations",f"+{ngn(round(500*0.02*15000))}","High"),
        ("5","Set free delivery over ₦50,000","Dev","AOV lift","Medium"),
        ("6","Submit XML sitemap to Google Search Console","Marketing","SEO","Medium"),
        ("6","Create 3 gift set bundle products","Operations","AOV","Medium"),
        ("7","Launch Meta Ads — retargeting pixel + first campaign","Marketing","Revenue","High"),
        ("7","Film Instagram Reels for top 3 products","Marketing","Traffic","High"),
        ("8","Begin influencer outreach — 10 Lagos/Abuja micro-influencers","Marketing","Traffic","High"),
        ("8","Install WooCommerce Points and Rewards (loyalty)","Dev","Retention","Medium"),
    ]
    road_rows = [road_header]
    pc2       = {"Critical": RED, "High": AMBER, "Medium": GOLD}
    for wk, task, who, imp, pri in roadmap:
        road_rows.append([
            Paragraph(wk,   mst(fontSize=9, textColor=MGRAY, fontName="Helvetica", alignment=TA_CENTER)),
            Paragraph(task, BODY),
            Paragraph(who,  SM),
            Paragraph(imp,  mst(fontSize=8, textColor=GREEN if "₦" in imp else GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(pri,  mst(fontSize=7, textColor=pc2.get(pri, GOLD), fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ])
    road_t = Table(road_rows, colWidths=[10*mm, 88*mm, 24*mm, 30*mm, 18*mm])
    road_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LBGR]),("GRID",(0,0),(-1,-1),0.25,rcolors.HexColor("#E0D8CC")),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),4),("ALIGN",(0,0),(0,-1),"CENTER")]))
    story.append(road_t)

    # Footer
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width=CW, thickness=0.5, color=GOLD, spaceAfter=4))
    story.append(Paragraph(
        f"Scentified eCommerce Audit Agent v2.0  |  scentifiedperfume.com  |  {datetime.now().strftime('%d %B %Y')}  |  Run again anytime to track progress",
        SM
    ))

    doc.build(story)
    log(f"PDF saved: {pdf_path}", "OK")
    return pdf_path
