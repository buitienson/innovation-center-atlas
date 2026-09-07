#!/usr/bin/env python3
"""Grow ROSTER (src/atlas.html) with real organizations Gemini extracts from
specific, known web pages, for exactly one queue item per run.

Design history (see _claude/routine-roster-grow.md "Tinh trang hien tai" for
the full story): the first version of this script used Gemini's Google
Search grounding tool (tools:[{"google_search":{}}]) so Gemini could search
the open web itself. Confirmed empirically on 2026-09-06 that this key's
project has a grounding quota of zero (429 RESOURCE_EXHAUSTED on every
grounded call, while plain calls succeed) - likely Google's 2026 free-tier
cuts, possibly requiring billing to unlock. Also confirmed that Gemini's
SEPARATE `url_context` tool (fetch specific URLs, no open search) works fine
on the same key with no quota error. This version uses that instead: each
queue item now supplies its own candidate source URLs (a directory page, a
Wikipedia list, an association member page...) instead of a free-text search
query, and Gemini extracts only what it actually finds on those pages -
`urlContextMetadata` in the response confirms which URLs were really
fetched, so a failed fetch can't be quietly passed off as a real finding.

Unlike the generic `gemini_worker.py` (Brain skill `gemini-delegate`, pure
text-in/text-out with no web access at all), this script can actually read
live pages. Every candidate is still independently liveness-checked over
HTTP before being trusted - even a successfully-fetched source page doesn't
guarantee Gemini transcribed an organization's own URL correctly.

Usage:
  export GEMINI_API_KEY="your-key"   # shell only, never written to a file
  python3 roster_grow_worker.py \
    --queue-item "Malaysia - TTOs at major public universities" \
    --source-urls "https://en.wikipedia.org/wiki/List_of_universities_in_Malaysia" "https://example.com/another-source" \
    --roster-html ../../src/atlas.html \
    --output candidates.json \
    --max-new 15

Exit codes (the calling routine relies on these):
  0 = ran fine (candidates.json written, possibly an empty list - including
      the case where every source URL failed to fetch)
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

SYSTEM_INSTRUCTION = """Ban la mot nha nghien cuu dang doc mot so trang web cu the duoc giao
(qua cong cu url_context) de tim cac to chuc/don vi chuyen giao cong nghe (Technology Transfer
Office - TTO), trung tam doi moi sang tao, vuon uom/tang toc khoi nghiep gan voi truong dai hoc
hoac vien nghien cuu.

QUAN TRONG: chi liet ke to chuc THUC SU xuat hien tren cac trang duoc giao - khong duoc tu suy
doan hay lay tu kien thuc san co neu trang khong the tai duoc hoac khong nhac den to chuc do.
Neu mot trang khong tai duoc, bo qua noi dung tu trang do, dung doan.

Tra ve DUNG MOT JSON array thuan tuy (khong markdown fence, khong loi giai thich truoc/sau),
moi phan tu la mot object voi cac truong:
  name (string, ten to chuc/don vi, ten goc - khong dich),
  host (string, truong dai hoc/vien nghien cuu chu quan - de trong "" neu to chuc do doc lap),
  country (string, ten quoc gia bang tieng Anh, vi du "Malaysia"),
  url (string, trang web chinh thuc cua chinh to chuc do - dung lien ket tren trang nguon neu co;
    neu trang nguon khong cho lien ket rieng, uoc luong URL hop ly nhat dua tren ten
    vien/truong/to chuc chu quan - se duoc kiem tra song rieng sau nen uoc luong hop ly van
    chap nhan duoc, KHONG duoc de trong),
  lat (number, vi do gan dung cua thanh pho dat tru so - uoc luong tu kien thuc dia ly, khong can
    tim kiem rieng cho buoc nay),
  lng (number, kinh do gan dung, cung logic nhu lat)

Neu khong trang nao trong so duoc giao tai duoc, hoac khong trang nao nhac den to chuc phu hop,
tra ve mang rong []."""


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
        "tools": [{"url_context": {}}],
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
    url_ctx = candidates[0].get("urlContextMetadata", {}) or {}
    url_statuses = [
        (m.get("retrievedUrl", ""), m.get("urlRetrievalStatus", ""))
        for m in url_ctx.get("urlMetadata", []) or []
    ]
    usage = body.get("usageMetadata", {})
    return text, url_statuses, usage


def plain_call_works(api_key, model):
    """A quick tool-free probe on the same model/key, used only for
    diagnostics when every url_context attempt is exhausted - it tells us
    whether the KEY is dead (plain call also fails) or just this tool's
    quota specifically (plain call succeeds)."""
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
            text, url_statuses, usage = call_gemini_once(api_key, model, user_text)
            if i > 0:
                print(f"(Da chuyen sang model {model})", file=sys.stderr)
            return model, text, url_statuses, usage
        except GeminiHTTPError as e:
            last_err = e
            if e.status in RETRYABLE_STATUS and i < len(models) - 1:
                print(f"Model {model} loi {e.status}, thu model ke tiep...", file=sys.stderr)
                continue
            break
    if last_err.status in RETRYABLE_STATUS:
        if plain_call_works(api_key, models[-1]):
            print(
                f"Ca {len(models)} model deu tra 429 KHI BAT url_context, nhung goi thuong "
                f"(khong tool) tren cung key/model van chay duoc. Day la han muc rieng cua "
                f"tool nay bi chan/het, khong phai key het hop le. Xem "
                f"https://ai.dev/rate-limit (can dang nhap dung tai khoan).",
                file=sys.stderr,
            )
        else:
            print(f"Ca {len(models)} model deu het han muc/qua tai (loi cuoi: {last_err.status}) - "
                  f"ke ca goi khong tool cung loi, co the ca key da het han muc chung.",
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
    ap = argparse.ArgumentParser(description="Grow ROSTER via Gemini's url_context tool")
    ap.add_argument("--queue-item", required=True, help="Label for this run (for logs/records)")
    ap.add_argument("--source-urls", required=True, nargs="+", help="One or more specific pages for Gemini to read via url_context")
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

    urls_block = "\n".join(args.source_urls)
    user_text = (
        f"Muc tieu: {args.queue_item}\n\n"
        f"Doc cac trang sau qua url_context roi liet ke cac to chuc CGCN/DMST dai hoc tim duoc, "
        f"theo dung dinh dang JSON da mo ta trong system instruction:\n{urls_block}"
    )
    models = [args.model] if args.model else MODEL_FALLBACK_CHAIN
    model, text, url_statuses, usage = call_gemini(api_key, models, user_text)
    log_usage(model, usage, args.queue_item)

    succeeded = [u for u, s in url_statuses if s == "URL_RETRIEVAL_STATUS_SUCCESS"]
    print(f"Trang tai duoc: {len(succeeded)}/{len(url_statuses)} ({url_statuses})", file=sys.stderr)
    if not succeeded:
        # Nothing was actually fetched - whatever Gemini said can't be trusted
        # as coming from the source, so don't merge anything this run.
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump([], f)
        print("Khong trang nao tai duoc - ghi ket qua rong, khong tin noi dung Gemini tra ve.", file=sys.stderr)
        sys.exit(0)

    parsed = extract_json_array(text)
    if parsed is None:
        print("Khong parse duoc JSON tu Gemini. Raw output:", file=sys.stderr)
        print(text, file=sys.stderr)
        sys.exit(1)

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
