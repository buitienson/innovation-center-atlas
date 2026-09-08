#!/usr/bin/env python3
"""Fill in missing website URLs for EXISTING ROSTER entries (src/atlas.html).

Different job from roster_grow_worker.py (which adds brand-new organizations
found on a given source page). This script targets the ~318/786 ROSTER rows
that already have a name/host/country but an empty `url` field, and asks
Gemini - a PLAIN call, no tools - to recall each organization's official
website from its own training knowledge. This is intentionally NOT grounded
(no url_context, no google_search): we already know the organization exists
(it's already in ROSTER), so the only question is "what's its URL", and a
wrong guess is caught by the same mandatory HTTP liveness check used
everywhere else in this pipeline - never trust a guess, verify it resolves.

Usage:
  export GEMINI_API_KEY="your-key"
  python3 roster_fill_websites.py --roster-html ../../src/atlas.html \
    --limit 300 --batch-size 25 --apply

  Without --apply, just reports what it WOULD fill (dry run).

Exit codes:
  0 = ran fine
  1 = real error
  2 = every model hit a quota/overload error
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
ROSTER_MARKER = "var ROSTER = /*__ROSTER_DATA__*/["

SYSTEM_INSTRUCTION = """Ban duoc giao mot danh sach cac to chuc chuyen giao cong nghe/doi moi
sang tao gan voi truong dai hoc, DA XAC NHAN LA CO THAT (khong can kiem tra su ton tai). Viec
duy nhat can lam: voi moi to chuc, neu ban biet chac (tu kien thuc huan luyen) URL trang web
chinh thuc cua no thi ghi ra; neu KHONG chac chan, ghi null - khong doan dai, thu se tu kiem
tra song rieng nen doan sai khong sao nhung dung bia mot URL hoan toan khong lien quan.

Tra ve DUNG MOT JSON array thuan tuy (khong markdown fence, khong giai thich), cung do dai va
cung thu tu voi danh sach duoc giao, moi phan tu la mot object {"index": <so thu tu goc>, "url":
"<url hoac null>"}."""


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
    usage = body.get("usageMetadata", {})
    return text, usage


def call_gemini(api_key, models, user_text):
    last_err = None
    for i, model in enumerate(models):
        try:
            text, usage = call_gemini_once(api_key, model, user_text)
            return model, text, usage
        except GeminiHTTPError as e:
            last_err = e
            if e.status in RETRYABLE_STATUS and i < len(models) - 1:
                print(f"Model {model} loi {e.status}, thu model ke tiep...", file=sys.stderr)
                continue
            break
    if last_err.status in RETRYABLE_STATUS:
        print(f"Ca {len(models)} model deu het han muc/qua tai (loi cuoi: {last_err.status}).", file=sys.stderr)
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
            model, usage.get("promptTokenCount", ""), usage.get("candidatesTokenCount", ""), label,
        ])


def extract_json_array(text):
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


def find_roster_span(html):
    start = html.find(ROSTER_MARKER)
    if start == -1:
        raise ValueError("ROSTER marker not found")
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
    return arr_start, i + 1


def load_roster(html):
    arr_start, arr_end = find_roster_span(html)
    return json.loads(html[arr_start:arr_end])


def save_roster(html, roster):
    arr_start, arr_end = find_roster_span(html)
    new_arr_text = json.dumps(roster, ensure_ascii=False, separators=(",", ":"))
    return html[:arr_start] + new_arr_text + html[arr_end:]


def domain_of(url):
    m = re.search(r"https?://(?:www\.)?([^/]+)", url or "", re.I)
    return m.group(1).lower() if m else ""


# A plain 200 OK is not enough proof - expired/never-registered .edu-adjacent
# domains routinely get scooped up by domain resellers and serve a normal
# 200 "buy this domain" parking page (confirmed the hard way: Gemini guessed
# "fistiitp.com" for a real IIT Patna organization, and it resolved fine as
# an active for-sale listing on a completely unrelated reseller site). These
# phrases are the standard signatures of that family of parking pages.
PARKING_PAGE_SIGNS = [
    "domain for sale", "domain may be for sale", "buy this domain",
    "this domain is for sale", "backorder this domain", "premium domain",
    "domain broker", "godaddy", "afternic", "hugedomains", "sedo.com",
    "dan.com", "namecheap", "expireddomains", "domain name is for sale",
    "inquire about this domain", "make an offer",
]


# Confirmed the hard way (twice): a parking service can hand a domain over
# via a CLIENT-SIDE JS redirect (`window.location.href=...`) instead of an
# HTTP redirect - urllib never executes that JS, so it only ever sees a tiny
# stub page with none of the tell-tale "for sale" wording (ramot.com's whole
# response was `<script>window.onload=function(){window.location.href=
# "/lander"}</script>`, ~130 bytes). A real organization's homepage almost
# never renders down to near-nothing, so treat a suspiciously thin page as
# untrustworthy even when no parking phrase matched.
MIN_VISIBLE_TEXT_CHARS = 200


def visible_text_len(html):
    no_script = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    no_tags = re.sub(r"<[^>]+>", " ", no_script)
    return len(re.sub(r"\s+", " ", no_tags).strip())


# A real page's actual body text can easily be pushed past a small read
# size by a long <head> (meta tags, structured data, inline critical CSS) -
# confirmed the hard way too: Oxford/Birmingham/Trinity College Dublin all
# got misflagged as "thin" at an 8KB read because that budget was entirely
# consumed by <head> before any visible body text appeared. Read enough that
# a normal page's real content shows up.
READ_BYTES = 65536
# Being thin is only damning together with an explicit client-side redirect
# OUT of the page (this is what ramot.com/fistiitp.com actually did) - a
# thin page with no redirect could just be a heavy anti-bot challenge page
# on an otherwise real, legitimate site, which must not be rejected on that
# basis alone.
REDIRECT_OUT_PATTERNS = [
    r"window\.location", r"document\.location", r"top\.location",
    r'<meta[^>]+http-equiv=["\']?refresh',
]


def check_url(url, timeout=10):
    """Returns (ok, reason). ok=False means: don't trust this URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (roster-fill-websites)"}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if not (200 <= resp.status < 400):
                return False, f"HTTP {resp.status}"
            raw = resp.read(READ_BYTES).decode("utf-8", errors="ignore")
            body = raw.lower()
    except Exception as e:
        return False, f"{type(e).__name__}"
    thin = visible_text_len(raw) < MIN_VISIBLE_TEXT_CHARS
    redirects_out = any(re.search(p, body) for p in REDIRECT_OUT_PATTERNS)
    if thin and redirects_out:
        return False, "thin page with a client-side redirect out (parking-stub pattern)"
    for sign in PARKING_PAGE_SIGNS:
        if sign in body:
            return False, f"parking-page phrase '{sign}'"
    return True, "ok"


def url_is_alive(url, timeout=10):
    ok, _ = check_url(url, timeout=timeout)
    return ok


def main():
    ap = argparse.ArgumentParser(description="Fill missing website URLs in ROSTER")
    ap.add_argument("--roster-html", required=True)
    ap.add_argument("--limit", type=int, default=1000, help="Max missing-website entries to attempt this run")
    ap.add_argument("--batch-size", type=int, default=25)
    ap.add_argument("--model", help="Force a single model")
    ap.add_argument("--apply", action="store_true", help="Actually write back to the HTML file; without this, dry-run only")
    ap.add_argument("--report", help="Path to write a JSON report of what was filled")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY chua duoc set.", file=sys.stderr)
        sys.exit(1)

    html = read_text(args.roster_html)
    roster = load_roster(html)
    existing_domains = {domain_of(r[3]) for r in roster if len(r) > 3 and r[3]}

    missing = [(i, r) for i, r in enumerate(roster) if len(r) < 4 or not r[3] or not str(r[3]).strip()]
    missing = missing[:args.limit]
    print(f"Tong {len(roster)} muc ROSTER, {sum(1 for r in roster if len(r)<4 or not r[3] or not str(r[3]).strip())} thieu website, xu ly {len(missing)} muc lan nay.", file=sys.stderr)

    models = [args.model] if args.model else MODEL_FALLBACK_CHAIN
    filled = []
    for batch_start in range(0, len(missing), args.batch_size):
        batch = missing[batch_start:batch_start + args.batch_size]
        listing = "\n".join(
            f"{j}. {r[0]} | Truong/vien chu quan: {r[1] or '(doc lap)'} | Quoc gia: {r[2]}"
            for j, (_, r) in enumerate(batch)
        )
        user_text = f"Danh sach ({len(batch)} to chuc):\n{listing}"
        model, text, usage = call_gemini(api_key, models, user_text)
        log_usage(model, usage, f"fill-websites batch {batch_start}")
        parsed = extract_json_array(text)
        if parsed is None:
            print(f"Batch {batch_start}: khong parse duoc JSON, bo qua batch nay.", file=sys.stderr)
            continue
        for item in parsed:
            try:
                j = int(item.get("index"))
            except (TypeError, ValueError):
                continue
            if j < 0 or j >= len(batch):
                continue
            roster_idx, row = batch[j]
            guess = item.get("url")
            if not guess or not isinstance(guess, str) or not guess.strip():
                continue
            guess = guess.strip()
            dom = domain_of(guess)
            if not dom or dom in existing_domains:
                continue  # would collide with an existing entry - skip, don't merge two orgs
            if not url_is_alive(guess):
                print(f"Bo qua (khong song): {row[0]} -> {guess}", file=sys.stderr)
                continue
            filled.append({"index": roster_idx, "name": row[0], "url": guess})
            existing_domains.add(dom)
            if args.apply:
                roster[roster_idx][3] = guess

    print(f"Dien duoc {len(filled)}/{len(missing)} URL da kiem tra song.", file=sys.stderr)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(filled, f, ensure_ascii=False, indent=2)
    if args.apply and filled:
        new_html = save_roster(html, roster)
        with open(args.roster_html, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Da ghi {len(filled)} URL moi vao {args.roster_html}.", file=sys.stderr)
    elif not args.apply:
        print("(dry run - dung --apply de ghi that vao file)", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
