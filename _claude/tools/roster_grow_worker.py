#!/usr/bin/env python3
"""Grow ROSTER (src/atlas.html) with real organizations Gemini extracts from
specific, known web pages, for exactly one queue item per run.

Design history (see _claude/routine-roster-grow.md "Tinh trang hien tai" for
the full story): the first version used Gemini's Google Search grounding
tool, which turned out to have a quota of zero on this key without billing.
This version uses the separate `url_context` tool instead (fetch specific
URLs, no open search, confirmed working with no quota error): each queue
item supplies its own candidate source URLs, and Gemini extracts only what
it actually finds on those pages - `urlContextMetadata` confirms which URLs
were really fetched, so a failed fetch can't be quietly passed off as real.

Shares its Gemini-calling and URL-verification logic with
roster_fill_websites.py via roster_common.py - see that module's docstring
for why the verification step is safety-critical and non-trivial (it caught
two real wrong-URL cases this session that a plain "HTTP 200" check missed).

Usage:
  export GEMINI_API_KEY="your-key"   # shell only, never written to a file
  python3 roster_grow_worker.py \
    --queue-item "Malaysia - TTOs at major public universities" \
    --source-urls "https://en.wikipedia.org/wiki/List_of_universities_in_Malaysia" \
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
import os
import sys

import roster_common as c

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

    roster = c.load_roster(args.roster_html)
    existing_names = {c.normalize_name(r[0]) for r in roster}
    existing_domains = {c.domain_of(r[3]) for r in roster if len(r) > 3 and r[3]}
    source_domains = {c.domain_of(u) for u in args.source_urls if c.domain_of(u)}

    urls_block = "\n".join(args.source_urls)
    user_text = (
        f"Muc tieu: {args.queue_item}\n\n"
        f"Doc cac trang sau qua url_context roi liet ke cac to chuc CGCN/DMST dai hoc tim duoc, "
        f"theo dung dinh dang JSON da mo ta trong system instruction:\n{urls_block}"
    )
    models = [args.model] if args.model else c.MODEL_FALLBACK_CHAIN
    model, candidate, text, usage = c.call_gemini(
        api_key, models, SYSTEM_INSTRUCTION, user_text,
        tools=[{"url_context": {}}], tool_label="url_context",
    )
    c.log_usage(model, usage, args.queue_item)

    url_ctx = candidate.get("urlContextMetadata", {}) or {}
    url_statuses = [
        (m.get("retrievedUrl", ""), m.get("urlRetrievalStatus", ""))
        for m in url_ctx.get("urlMetadata", []) or []
    ]
    succeeded = [u for u, s in url_statuses if s == "URL_RETRIEVAL_STATUS_SUCCESS"]
    print(f"Trang tai duoc: {len(succeeded)}/{len(url_statuses)} ({url_statuses})", file=sys.stderr)
    if not succeeded:
        with open(args.output, "w", encoding="utf-8") as f:
            import json
            json.dump([], f)
        print("Khong trang nao tai duoc - ghi ket qua rong, khong tin noi dung Gemini tra ve.", file=sys.stderr)
        sys.exit(0)

    parsed = c.extract_json_array(text)
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
        norm = c.normalize_name(name)
        dom = c.domain_of(url)
        if norm in existing_names or (dom and dom in existing_domains):
            continue  # already in ROSTER
        if dom and dom in source_domains:
            print(f"Bo qua (URL trung voi trang nguon, khong phai trang rieng cua to chuc): {name} - {url}", file=sys.stderr)
            continue
        ok, reason = c.check_url(url)
        if not ok:
            print(f"Bo qua ({reason}): {name} - {url}", file=sys.stderr)
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
        existing_names.add(norm)
        if dom:
            existing_domains.add(dom)

    import json
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Model dung: {model}. Gemini de xuat {len(parsed)} muc, giu lai {len(results)} sau khi loc trung + kiem tra song.", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
