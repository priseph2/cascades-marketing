import sys
import requests
from config import HEADERS


def log(msg, level="INFO"):
    icons = {"INFO": "[i]", "OK": "[OK]", "WARN": "[!]", "ERROR": "[ERR]", "RUN": "[>>]"}
    line = f"{icons.get(level, '')}{msg}"
    print(line.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"))


def safe_get(url, timeout=15, auth=None):
    try:
        kwargs = {"headers": HEADERS, "timeout": timeout}
        if auth:
            kwargs["auth"] = auth
        r = requests.get(url, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        log(f"Fetch failed {url}: {e}", "ERROR")
        return None


def sc(s):
    return "green" if s >= 80 else ("amber" if s >= 50 else "red")


def sl(s):
    return "Good" if s >= 80 else ("Needs Work" if s >= 50 else "Critical")


def ngn(amount):
    return f"NGN {amount:,.0f}"
