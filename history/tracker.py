import os
import json
from datetime import datetime, timedelta
from config import CONFIG
from utils.helpers import log


def load_history():
    path = CONFIG["history_file"]
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_history(history, new_entry):
    history.append(new_entry)
    history = history[-20:]
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    with open(CONFIG["history_file"], "w") as f:
        json.dump(history, f, indent=2)
    return history


def compute_run_diff(history, current):
    if not history:
        return {"available": False, "summary": "First audit run - no previous data to compare."}
    prev    = history[-1]
    metrics = ["overall_score", "mobile_speed", "ux_score", "seo_score", "checkout_score"]
    labels  = {
        "overall_score":  "Overall",
        "mobile_speed":   "Mobile Speed",
        "ux_score":       "Store UX",
        "seo_score":      "SEO",
        "checkout_score": "Checkout",
    }
    diffs = {}
    for m in metrics:
        cur_val  = current.get(m, 0)
        prev_val = prev.get(m, 0)
        delta    = cur_val - prev_val
        diffs[m] = {
            "label":     labels[m],
            "current":   cur_val,
            "previous":  prev_val,
            "delta":     delta,
            "arrow":     "^" if delta > 0 else ("v" if delta < 0 else "="),
            "direction": "up" if delta > 0 else ("down" if delta < 0 else "unchanged"),
        }
    improved = [d for d in diffs.values() if d["delta"] > 0]
    declined = [d for d in diffs.values() if d["delta"] < 0]
    parts = []
    if improved:
        parts.append(f"{len(improved)} area(s) improved: " + ", ".join(f"{d['label']} +{d['delta']}" for d in improved))
    if declined:
        parts.append(f"{len(declined)} area(s) declined: " + ", ".join(f"{d['label']} {d['delta']}" for d in declined))
    if not improved and not declined:
        parts.append("No change from last run")
    ov_delta = diffs["overall_score"]["delta"]
    summary  = (
        f"Overall score {'improved by '+str(ov_delta) if ov_delta>0 else 'declined by '+str(abs(ov_delta)) if ov_delta<0 else 'unchanged'} "
        f"vs last run ({prev.get('date','?')[:10]}). " + ". ".join(parts) + "."
    )
    return {
        "available":       True,
        "previous_date":   prev.get("date", "")[:10],
        "diffs":           diffs,
        "improved_count":  len(improved),
        "declined_count":  len(declined),
        "summary":         summary,
    }


def compute_weekly_summary(history):
    if len(history) < 2:
        return {"available": False, "note": "Need at least 2 runs to produce weekly summary."}
    now       = datetime.now()
    week_ago  = now - timedelta(days=7)
    current   = history[-1]
    prev_week = None
    for entry in reversed(history[:-1]):
        try:
            entry_dt = datetime.strptime(entry["date"][:16], "%Y-%m-%d %H:%M")
            if entry_dt <= week_ago:
                prev_week = entry
                break
        except Exception:
            continue
    if not prev_week:
        return {"available": False, "note": "No run found from 7+ days ago yet. Weekly summary appears after second week of auditing."}
    metrics = ["overall_score", "mobile_speed", "ux_score", "seo_score", "checkout_score"]
    labels  = {
        "overall_score":  "Overall",
        "mobile_speed":   "Mobile Speed",
        "ux_score":       "Store UX",
        "seo_score":      "SEO",
        "checkout_score": "Checkout",
    }
    weekly_diffs = {}
    for m in metrics:
        cur  = current.get(m, 0)
        prev = prev_week.get(m, 0)
        d    = cur - prev
        weekly_diffs[m] = {
            "label":      labels[m],
            "this_week":  cur,
            "last_week":  prev,
            "delta":      d,
            "arrow":      "^" if d > 0 else ("v" if d < 0 else "="),
            "pct_change": round((d / prev * 100), 1) if prev > 0 else 0,
        }
    ov_delta = weekly_diffs["overall_score"]["delta"]
    if ov_delta > 5:    health = "Strong improvement this week"
    elif ov_delta > 0:  health = "Marginal improvement this week"
    elif ov_delta == 0: health = "No change this week - review roadmap"
    else:               health = "Score declined this week - investigate"
    result = {
        "available":        True,
        "week_start":       prev_week.get("date", "")[:10],
        "week_end":         current.get("date", "")[:10],
        "health":           health,
        "overall_delta":    ov_delta,
        "diffs":            weekly_diffs,
        "top_improvement":  max(weekly_diffs.values(), key=lambda x: x["delta"])["label"],
        "top_decline":      min(weekly_diffs.values(), key=lambda x: x["delta"])["label"] if ov_delta < 0 else None,
    }
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    ws_path = os.path.join(CONFIG["output_dir"], "weekly_summary.json")
    with open(ws_path, "w") as f:
        json.dump({"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "summary": result, "full_history": history}, f, indent=2)
    log(f"Weekly summary saved: {ws_path}", "OK")
    return result
