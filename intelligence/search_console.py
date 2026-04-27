import json
from datetime import datetime, timedelta


def get_gsc_service(gsc_secrets):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(
        token=None,
        refresh_token=gsc_secrets["refresh_token"],
        client_id=gsc_secrets["client_id"],
        client_secret=gsc_secrets["client_secret"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def _query(service, site_url, days, dimensions, filters=None, row_limit=500):
    end_date   = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    body = {
        "startDate":  start_date,
        "endDate":    end_date,
        "dimensions": dimensions,
        "rowLimit":   row_limit,
        "dataState":  "all",
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    resp = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    return resp.get("rows", [])


def _fmt(rows, key_index=0):
    return [
        {
            "query":       r["keys"][key_index] if r.get("keys") else "",
            "clicks":      r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr":         round(r.get("ctr", 0) * 100, 2),
            "position":    round(r.get("position", 0), 1),
        }
        for r in rows
    ]


def run_search_console_analysis(gsc_secrets, site_url, days=90):
    service = get_gsc_service(gsc_secrets)

    # All queries sorted by clicks
    all_rows = _query(service, site_url, days, ["query"])
    top_queries = _fmt(sorted(all_rows, key=lambda x: x.get("clicks", 0), reverse=True)[:50])

    # Nigeria-only queries
    ng_rows = _query(service, site_url, days, ["query"], filters=[
        {"dimension": "country", "operator": "equals", "expression": "nga"}
    ])
    nigeria_queries = _fmt(sorted(ng_rows, key=lambda x: x.get("clicks", 0), reverse=True)[:50])

    # Pages by impressions
    page_rows = _query(service, site_url, days, ["page"])

    # Low CTR: ranking (position ≤ 20) but barely clicked (CTR < 3%)
    low_ctr = [
        {
            "page":        r["keys"][0] if r.get("keys") else "",
            "impressions": r.get("impressions", 0),
            "ctr":         round(r.get("ctr", 0) * 100, 2),
            "position":    round(r.get("position", 0), 1),
        }
        for r in page_rows
        if r.get("impressions", 0) >= 50
        and r.get("ctr", 1) < 0.03
        and r.get("position", 99) <= 20
    ]
    low_ctr.sort(key=lambda x: x["impressions"], reverse=True)

    # Position 4–10 product pages: fix title/meta to climb to top 3
    quick_wins = [
        {
            "page":        r["keys"][0] if r.get("keys") else "",
            "clicks":      r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr":         round(r.get("ctr", 0) * 100, 2),
            "position":    round(r.get("position", 0), 1),
        }
        for r in page_rows
        if 4 <= r.get("position", 99) <= 10
        and r.get("impressions", 0) >= 10
        and "/product/" in (r["keys"][0] if r.get("keys") else "")
    ]
    quick_wins.sort(key=lambda x: x["impressions"], reverse=True)

    return {
        "top_queries":     top_queries,
        "nigeria_queries": nigeria_queries,
        "low_ctr_pages":   low_ctr[:20],
        "quick_wins":      quick_wins[:20],
        "summary": {
            "total_queries":    len(all_rows),
            "nigeria_queries":  len(ng_rows),
            "low_ctr_pages":    len(low_ctr),
            "quick_wins":       len(quick_wins),
            "date_range_days":  days,
        },
    }
