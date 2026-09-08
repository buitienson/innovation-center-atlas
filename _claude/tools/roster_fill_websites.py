#!/usr/bin/env python3
"""Fill in missing website URLs for EXISTING ROSTER entries (src/atlas.html).

Different job from roster_grow_worker.py (which adds brand-new organizations
found on a given source page). This script targets ROSTER rows that already
have a name/host/country but an empty `url` field, and asks Gemini - a PLAIN
call, no tools - to recall each organization's official website from its own
training knowledge. This is intentionally NOT grounded (no url_context, no
google_search): we already know the organization exists (it's already in
ROSTER), so the only question is "what's its URL", and a wrong guess is
caught by the shared verification in roster_common.py - never trust a guess,
verify it resolves AND isn't a parking page.

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
import json
import os
import sys

import roster_common as c

SYSTEM_INSTRUCTION = """Ban duoc giao mot danh sach cac to chuc chuyen giao cong nghe/doi moi
sang tao gan voi truong dai hoc, DA XAC NHAN LA CO THAT (khong can kiem tra su ton tai). Viec
duy nhat can lam: voi moi to chuc, neu ban biet chac (tu kien thuc huan luyen) URL trang web
chinh thuc cua no thi ghi ra; neu KHONG chac chan, ghi null - khong doan dai, thu se tu kiem
tra song rieng nen doan sai khong sao nhung dung bia mot URL hoan toan khong lien quan.

Tra ve DUNG MOT JSON array thuan tuy (khong markdown fence, khong giai thich), cung do dai va
cung thu tu voi danh sach duoc giao, moi phan tu la mot object {"index": <so thu tu goc>, "url":
"<url hoac null>"}."""


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

    html = c.read_text(args.roster_html)
    roster = c.load_roster_from_html(html)
    existing_domains = {c.domain_of(r[3]) for r in roster if len(r) > 3 and r[3]}

    missing = [(i, r) for i, r in enumerate(roster) if len(r) < 4 or not r[3] or not str(r[3]).strip()]
    missing = missing[:args.limit]
    print(f"Tong {len(roster)} muc ROSTER, {sum(1 for r in roster if len(r)<4 or not r[3] or not str(r[3]).strip())} thieu website, xu ly {len(missing)} muc lan nay.", file=sys.stderr)

    models = [args.model] if args.model else c.MODEL_FALLBACK_CHAIN
    filled = []
    for batch_start in range(0, len(missing), args.batch_size):
        batch = missing[batch_start:batch_start + args.batch_size]
        listing = "\n".join(
            f"{j}. {r[0]} | Truong/vien chu quan: {r[1] or '(doc lap)'} | Quoc gia: {r[2]}"
            for j, (_, r) in enumerate(batch)
        )
        user_text = f"Danh sach ({len(batch)} to chuc):\n{listing}"
        model, _candidate, text, usage = c.call_gemini(api_key, models, SYSTEM_INSTRUCTION, user_text)
        c.log_usage(model, usage, f"fill-websites batch {batch_start}")
        parsed = c.extract_json_array(text)
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
            dom = c.domain_of(guess)
            if not dom or dom in existing_domains:
                continue  # would collide with an existing entry - skip, don't merge two orgs
            ok, reason = c.check_url(guess)
            if not ok:
                print(f"Bo qua ({reason}): {row[0]} -> {guess}", file=sys.stderr)
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
        new_html = c.save_roster(html, roster)
        with open(args.roster_html, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Da ghi {len(filled)} URL moi vao {args.roster_html}.", file=sys.stderr)
    elif not args.apply:
        print("(dry run - dung --apply de ghi that vao file)", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
