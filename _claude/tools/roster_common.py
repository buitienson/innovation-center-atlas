"""Shared helpers for the ROSTER-growth tooling (roster_grow_worker.py,
roster_fill_websites.py). Keeping this in one place matters here more than
usual: the URL-verification logic below is safety-critical (it's the only
thing standing between a Gemini guess and a wrong link going live on a
public page), and it was hardened twice this session after two real
false-positives slipped through - duplicating it into two scripts would let
one copy drift out of sync with lessons learned in the other.
"""
import csv
import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse

MODEL_FALLBACK_CHAIN = ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-pro-latest"]
RETRYABLE_STATUS = (429, 503)
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usage.log")
ROSTER_MARKER = "var ROSTER = /*__ROSTER_DATA__*/["


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class GeminiHTTPError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")


def call_gemini_once(api_key, model, system_instruction, user_text, tools=None):
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
    }
    if tools:
        payload["tools"] = tools
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
    return candidates[0], text, usage


def plain_call_works(api_key, model):
    """Tool-free probe used only for diagnostics when every tooled attempt is
    exhausted - distinguishes "this key is dead" from "just this tool's quota
    is blocked" (confirmed both happen independently on 2026-09-06/07)."""
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


def call_gemini(api_key, models, system_instruction, user_text, tools=None, tool_label="tool"):
    """Runs the fallback chain; on total exhaustion, diagnoses and exits(2),
    or exits(1) on a genuine non-quota error. Returns (model, candidate, text, usage)."""
    last_err = None
    for i, model in enumerate(models):
        try:
            candidate, text, usage = call_gemini_once(api_key, model, system_instruction, user_text, tools)
            if i > 0:
                print(f"(Da chuyen sang model {model})", file=sys.stderr)
            return model, candidate, text, usage
        except GeminiHTTPError as e:
            last_err = e
            if e.status in RETRYABLE_STATUS and i < len(models) - 1:
                print(f"Model {model} loi {e.status}, thu model ke tiep...", file=sys.stderr)
                continue
            break
    if last_err.status in RETRYABLE_STATUS:
        if plain_call_works(api_key, models[-1]):
            print(
                f"Ca {len(models)} model deu tra 429 KHI DUNG {tool_label}, nhung goi thuong "
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


def load_roster_from_html(html):
    arr_start, arr_end = find_roster_span(html)
    return json.loads(html[arr_start:arr_end])


def load_roster(roster_html_path):
    return load_roster_from_html(read_text(roster_html_path))


def save_roster(html, roster):
    arr_start, arr_end = find_roster_span(html)
    new_arr_text = json.dumps(roster, ensure_ascii=False, separators=(",", ":"))
    return html[:arr_start] + new_arr_text + html[arr_end:]


def domain_of(url):
    m = re.search(r"https?://(?:www\.)?([^/]+)", url or "", re.I)
    return m.group(1).lower() if m else ""


def normalize_name(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


# --- URL trust verification -------------------------------------------
#
# Confirmed twice this session that "HTTP 200" is not proof a URL is what it
# claims to be:
#   1. Gemini guessed "fistiitp.com" for a real IIT Patna organization; it
#      resolved as a live GoDaddy domain-resale listing (200 OK, full of
#      "buy this domain" text).
#   2. Gemini guessed "ramot.com" for the real Ramot (Tel Aviv University's
#      tech-transfer company); the whole response was a ~130-byte stub whose
#      only content was `window.location.href="/lander"` - a client-side JS
#      redirect to a parking page that a plain-text scan never sees, because
#      urllib doesn't execute JS.
# A first fix that flagged any "thin" response also misfired on real sites
# (Oxford, Birmingham, Trinity College Dublin) whose actual content was
# simply pushed past a small read size by a long <head> section. The fix
# needs BOTH signals - thinness AND an explicit redirect-out - together.
PARKING_PAGE_SIGNS = [
    "domain for sale", "domain may be for sale", "buy this domain",
    "this domain is for sale", "backorder this domain", "premium domain",
    "domain broker", "godaddy", "afternic", "hugedomains", "sedo.com",
    "dan.com", "namecheap", "expireddomains", "domain name is for sale",
    "inquire about this domain", "make an offer",
]
REDIRECT_OUT_PATTERNS = [
    r"window\.location(?:\.href)?\s*=\s*[\"']([^\"']+)[\"']",
    r"document\.location(?:\.href)?\s*=\s*[\"']([^\"']+)[\"']",
    r"top\.location(?:\.href)?\s*=\s*[\"']([^\"']+)[\"']",
    r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]*content=["\'][^;]*;\s*url=([^"\']+)["\']',
]
MIN_VISIBLE_TEXT_CHARS = 200
READ_BYTES = 65536


def visible_text_len(html):
    no_script = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    no_tags = re.sub(r"<[^>]+>", " ", no_script)
    return len(re.sub(r"\s+", " ", no_tags).strip())


def _find_redirect_target(body):
    for pattern in REDIRECT_OUT_PATTERNS:
        m = re.search(pattern, body, re.I)
        if m:
            return m.group(1)
    return None


def _fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (roster-tools)"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.geturl(), resp.read(READ_BYTES).decode("utf-8", errors="ignore")


def check_url(url, timeout=10, _hop=0):
    """Returns (ok, reason). ok=False means: don't trust this URL.

    A thin page with a client-side redirect isn't damning by itself - lots of
    real sites (confirmed: ums.edu.my) use `window.location.href="/v6"` as an
    ordinary same-site version/locale router, structurally identical to how
    a parking service hands a domain to its sale page (confirmed: ramot.com
    -> "/lander"). The only way to actually tell them apart is to follow the
    redirect one hop and judge what's really there - real content (UMS) vs.
    another dead end or parking page (Ramot's "/lander" 403s)."""
    try:
        status, _final_url, raw = _fetch(url, timeout)
        if not (200 <= status < 400):
            return False, f"HTTP {status}"
        body = raw.lower()
    except Exception as e:
        return False, f"{type(e).__name__}"
    thin = visible_text_len(raw) < MIN_VISIBLE_TEXT_CHARS
    target = _find_redirect_target(body)
    if thin and target:
        if _hop >= 1:
            return False, "redirect chain still thin after following one hop"
        resolved = urllib.parse.urljoin(url, target)
        ok, reason = check_url(resolved, timeout=timeout, _hop=_hop + 1)
        if ok:
            return True, "ok (via same-site redirect target)"
        return False, f"thin page whose redirect target also failed ({reason})"
    for sign in PARKING_PAGE_SIGNS:
        if sign in body:
            return False, f"parking-page phrase '{sign}'"
    return True, "ok"


def url_is_alive(url, timeout=10):
    ok, _ = check_url(url, timeout=timeout)
    return ok
