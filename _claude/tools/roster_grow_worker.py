#!/usr/bin/env python3
"""Grow ROSTER (src/atlas.html) with real, web-search-grounded organizations
found by Gemini, for exactly one queue item per run.

Unlike the generic `gemini_worker.py` (Brain skill `gemini-delegate`, pure
text-in/text-out with no web access), this script enables Gemini's Google
Search grounding tool so it can actually look things up instead of recalling
plausible-sounding names/URLs from training data. Every candidate is then
independently liveness-checked over HTTP before being trusted — grounding
reduces hallucination, it does not eliminate it, so the liveness check is the
real gate, not the grounding metadata.

Usage:
  export GEMINI_API_KEY="your-key"   # shell only, never written to a file
  python3 roster_grow_worker.py \
    --queue-item "AUTM member directory (autm.net) - North America TTOs" \
    --roster-html ../../src/atlas.html \
    --output candidates.json \
    --max-new 15

Exit codes (the calling routine relies on these):
  0 = ran fine (candidates.json written, possibly an empty list)
  1 = a real error (bad args, all models failed with a non-quota error,
      output couldn't be parsed as JSON after retries) - worth investigating
  2 = every model hit a quota/overload error (429/503) - normal "stop for
      today", not a bug
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.error

MODEL_FALLBACK_CHAIN = ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-pro-latest"]
RETRYABLE_STATUS = (429, 503)
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usage.log")

SYSTEM_INSTRUCTION = """Ban la mot nha nghien cuu dang tra cuu danh sach cac to chuc/don vi
chuyen giao cong nghe (Technology Transfer Office - TTO), trung tam doi moi sang tao,
vuon uom/tang toc khoi nghiep gan voi truong dai hoc hoac vien nghien cuu, tu MOT nguon
cu the duoc giao. Dung cong cu tim kiem de tra cuu nguon do that su - KHONG duoc liet ke
mot to chuc neu ban khong tim thay URL chinh thuc that qua ket qua tim kiem. Khong tu suy
doan hay nho lai tu kien thuc san co neu khong tra ra duoc URL that.

Tra ve DUNG MOT JSON array thuan tuy (khong markdown fence, khong loi giai thich truoc/sau),
moi phan tu la mot object voi cac truong:
  name (string, ten to chuc/don vi, ten goc - khong dich),
  host (string, truong dai hoc/vien nghien cuu chu quan - de trong "" neu to chuc do doc lap),
  country (string, ten quoc gia bang tieng Anh, vi du "Malaysia"),
  url (string, trang web chinh thuc cua chinh to chuc do - bat buoc, khong duoc de trong),
  lat (number, vi do gan dung cua thanh pho dat tru so - uoc luong tu kien thuc dia ly, khong can tim kiem rieng cho buoc nay),
  lng (number, kinh do gan dung, cung logic nhu lat)

Neu nguon duoc giao khong co to chuc nao dat tieu chuan tren (khong tim ra URL that), tra ve
mang rong []. Khong bao gio bia URL."""


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class GeminiHTTPError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")


def call_gemini_once(api_key, model, user_text):
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
        "tools": [{"google_search": {}}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise GeminiHTTPError(e.code, err_body)

    candidates = body.get("candidates") or []
    if not candidates:
        raise GeminiHTTPError(0, json.dumps(body, ensure_ascii=False))

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts if "text" in p)
    grounding = candidates[0].get("groundingMetadata", {}) or {}
    grounded_urls = []
    for chunk in grounding.get("groundingChunks", []) or []:
        web = chunk.get("web") or {}
        if web.get("uri"):
            grounded_urls.append(web["uri"])
    usage = body.get("usageMetadata", {})
    return text, grounded_urls, usage


def plain_call_works(api_key, model):
    """A quick non-grounded probe on the same model/key, used only for
    diagnostics when every grounded attempt is exhausted - it tells us
    whether the KEY is dead (plain call also fails) or just the grounding
    quota specifically (plain call succeeds). Confirmed empirically on
    2026-09-06: a key can have a perfectly healthy plain-call quota while
    every grounded (tools:[{"google_search":{}}]) call gets an immediate
    429 RESOURCE_EXHAUSTED - Google's 2026 free-tier cuts appear to zero
    out grounding specifically unless billing is enabled on the project."""
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"role": "user", "parts": [{"text": "ping"}]}]}
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status == 200
    except Exception:
        return False


def call_gemini(api_key, models, user_text):
    last_err = None
    for i, model in enumerate(models):
        try:
            text, grounded_urls, usage = call_gemini_once(api_key, model, user_text)
            if i > 0:
                print(f"(Da chuyen sang model {model})", file=sys.stderr)
            return model, text, grounded_urls, usage
        except GeminiHTTPError as e:
            last_err = e
            if e.status in RETRYABLE_STATUS and i < len(models) - 1:
                print(f"Model {model} loi {e.status}, thu model ke tiep...", file=sys.stderr)
                continue
            break
    if last_err.status in RETRYABLE_STATUS:
        if plain_call_works(api_key, models[-1]):
            print(
                f"Ca {len(models)} model deu tra 429 KHI BAT GOOGLE SEARCH GROUNDING, "
                f"nhung goi thuong (khong grounding) tren cung key/model van chay duoc. "
                f"Day la han muc grounding rieng bi chan/het, khong phai key het hop le. "
                f"Xem https://ai.dev/rate-limit (can dang nhap dung tai khoan) hoac can nhac "
                f"bat billing tren Google Cloud project cua key nay (Tier 1 co 1.500 luot "
                f"grounding mien phi/ngay, nhung bat billing se xoa toan bo han muc mien phi "
                f"khac cua project).",
                file=sys.stderr,
            )
        else:
            print(f"Ca {len(models)} model deu het han muc/qua tai (loi cuoi: {last_err.status}) - "
                  f"ke ca goi khong grounding cung loi, co the ca key da het han muc chung.",
                  file=sys.stderr)
        sys.exit(2)
    print(f"Loi HTTP {last_err.status} tu Gemini: {last_err.body}", file=sys.stderr)
    sys.exit(1)


def log_usage(model, usage, label):
    is_new = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["thoi_gian", "model", "input_tokens", "output_tokens", "viec"])
        w.writerow([
            datetime.datetime.now().isoformat(timespec="seconds"),
            model,
            usage.get("promptTokenCount", ""),
            usage.get("candidatesTokenCount", ""),
            label,
        ])


def extract_json_array(text):
    """Gemini is told not to wrap in a fence, but strip one if present anyway."""
    stripped = text.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", stripped, re.S)
    if fence:
        stripped = fence.group(1).strip()
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        return json.loads(stripped[start:end + 1])
    except json.JSONDecodeError:
        return None


def load_existing_roster(roster_html_path):
    """Extract the ROSTER JS array from src/atlas.html by bracket-matching -
    it's plain JSON-compatible data (see build.py for the same technique)."""
    html = read_text(roster_html_path)
    marker = "var ROSTER = /*__ROSTER_DATA__*/["
    start = html.find(marker)
    if start == -1:
        return []
    arr_start = html.index("[", start)
    depth = 0
    i = arr_start
    while True:
        c = html[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        if depth == 0:
            break
        i += 1
    return json.loads(html[arr_start:i + 1])


def domain_of(url):
    m = re.search(r"https?://(?:www\.)?([^/]+)", url or "", re.I)
    return m.group(1).lower() if m else ""


def normalize_name(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def url_is_alive(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (roster-grow-worker)"}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description="Grow ROSTER via Gemini + Google Search grounding")
    ap.add_argument("--queue-item", required=True, help="Description of the ONE source to search this run")
    ap.add_argument("--roster-html", required=True, help="Path to src/atlas.html, to read existing ROSTER for dedup")
    ap.add_argument("--output", required=True, help="Where to write the validated candidates JSON")
    ap.add_argument("--max-new", type=int, default=15)
    ap.add_argument("--model", help="Force a single model instead of the fallback chain")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY chua duoc set trong bien moi truong.", file=sys.stderr)
        sys.exit(1)

    existing = load_existing_roster(args.roster_html)
    existing_names = {normalize_name(r[0]) for r in existing}
    existing_domains = {domain_of(r[3]) for r in existing if len(r) > 3 and r[3]}

    user_text = (
        f"Nguon can tra: {args.queue_item}\n\n"
        "Liet ke cac to chuc CGCN/DMST dai hoc tim duoc tu nguon nay, theo dung dinh dang JSON "
        "da mo ta trong system instruction."
    )
    models = [args.model] if args.model else MODEL_FALLBACK_CHAIN
    model, text, grounded_urls, usage = call_gemini(api_key, models, user_text)
    log_usage(model, usage, args.queue_item)

    parsed = extract_json_array(text)
    if parsed is None:
        print("Khong parse duoc JSON tu Gemini. Raw output:", file=sys.stderr)
        print(text, file=sys.stderr)
        sys.exit(1)

    grounded_domains = {domain_of(u) for u in grounded_urls}
    results = []
    for item in parsed:
        if len(results) >= args.max_new:
            break
        name = (item.get("name") or "").strip()
        url = (item.get("url") or "").strip()
        country = (item.get("country") or "").strip()
        if not name or not url:
            continue
        norm = normalize_name(name)
        dom = domain_of(url)
        if norm in existing_names or (dom and dom in existing_domains):
            continue  # already in ROSTER
        if not url_is_alive(url):
            print(f"Bo qua (URL khong song): {name} - {url}", file=sys.stderr)
            continue
        results.append({
            "name": name,
            "host": (item.get("host") or "").strip(),
            "country": country,
            "url": url,
            "lat": item.get("lat"),
            "lng": item.get("lng"),
            "grounded": dom in grounded_domains,  # informational only, not a filter
            "source_queue_item": args.queue_item,
        })
        existing_names.add(norm)  # avoid duplicate candidates within this same run
        if dom:
            existing_domains.add(dom)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Model dung: {model}. Gemini de xuat {len(parsed)} muc, giu lai {len(results)} sau khi loc trung + kiem tra song.", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
