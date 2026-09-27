#!/usr/bin/env python3
"""Render profile cards from public GitHub merged-PR search results."""

from __future__ import annotations

import argparse
import calendar
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
QUERY = "is:pr author:ayush-shah org:open-metadata is:public is:merged"
FONT = "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"


def github_count(query: str, token: str | None) -> int:
    url = "https://api.github.com/search/issues?" + urlencode({"q": query, "per_page": 1})
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ayush-shah-profile-stats"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        data = json.load(response)
    if data.get("incomplete_results") is not False:
        raise ValueError(f"GitHub returned incomplete results for {query!r}")
    count = data.get("total_count")
    if not isinstance(count, int) or count < 0:
        raise ValueError(f"GitHub returned an invalid count for {query!r}")
    return count


def recent_months(today: date) -> list[dict[str, str | int]]:
    months = []
    for offset in range(5, -1, -1):
        absolute_month = today.year * 12 + today.month - 1 - offset
        year, month_zero = divmod(absolute_month, 12)
        month = month_zero + 1
        first = date(year, month, 1)
        last = min(today, date(year, month, calendar.monthrange(year, month)[1]))
        months.append({"label": first.strftime("%b"), "year": year, "start": first.isoformat(), "end": last.isoformat()})
    return months


def impact_svg(total: int, as_of: str) -> str:
    number = f"{total:,}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="205" viewBox="0 0 520 205" role="img" aria-labelledby="title desc">
  <title id="title">Public OpenMetadata contributions</title>
  <desc id="desc">{escape(number)} authored pull requests merged in public open-metadata repositories, snapshot {escape(as_of)}.</desc>
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#151B39"/><stop offset="1" stop-color="#103942"/></linearGradient>
    <linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="#8D9AFF"/><stop offset="1" stop-color="#4DE2C5"/></linearGradient>
  </defs>
  <rect width="520" height="205" rx="18" fill="url(#bg)"/>
  <rect x="1" y="1" width="518" height="203" rx="17" fill="none" stroke="#8996D9" stroke-opacity=".5" stroke-width="2"/>
  <path d="M 28 31 H 171" stroke="url(#accent)" stroke-width="4" stroke-linecap="round"/>
  <text x="28" y="61" fill="#C0CCEF" font-family="{FONT}" font-size="15" font-weight="700" letter-spacing="2">PUBLIC OPEN SOURCE WORK</text>
  <text x="26" y="144" fill="#F6F9FF" font-family="{FONT}" font-size="88" font-weight="800" letter-spacing="-3">{escape(number)}</text>
  <text x="29" y="173" fill="#C4D8E4" font-family="{FONT}" font-size="17" font-weight="600">merged PRs across open-metadata</text>
  <text x="28" y="192" fill="#94AACA" font-family="{FONT}" font-size="12">Public GitHub search snapshot · {escape(as_of)}</text>
</svg>
'''


def activity_svg(months: list[dict[str, str | int]], as_of: str) -> str:
    maximum = max(1, *(int(month["count"]) for month in months))
    bars = []
    descriptions = []
    for index, month in enumerate(months):
        count = int(month["count"])
        height = max(4, round(85 * count / maximum)) if count else 0
        x = 42 + index * 78
        y = 169 - height
        color = "#4DE2C5" if index == 5 else "#8190F7"
        label = str(month["label"])
        bars.append(f'<rect x="{x}" y="{y}" width="43" height="{height}" rx="6" fill="{color}"/>')
        bars.append(f'<text x="{x + 21}" y="{max(82, y - 9)}" text-anchor="middle" fill="#F5F8FF" font-family="{FONT}" font-size="17" font-weight="700">{count}</text>')
        bars.append(f'<text x="{x + 21}" y="194" text-anchor="middle" fill="#A8B9D9" font-family="{FONT}" font-size="14">{escape(label)}</text>')
        descriptions.append(f'{label} {month["year"]}: {count}')
    subtitle = f'{months[0]["label"]} {months[0]["year"]} – {months[-1]["label"]} {months[-1]["year"]}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="235" viewBox="0 0 520 235" role="img" aria-labelledby="title desc">
  <title id="title">Recent merged pull requests</title>
  <desc id="desc">Authored public PRs merged in open-metadata repositories. {escape('; '.join(descriptions))}. Snapshot {escape(as_of)}.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#151B39"/><stop offset="1" stop-color="#103942"/></linearGradient></defs>
  <rect width="520" height="235" rx="18" fill="url(#bg)"/>
  <rect x="1" y="1" width="518" height="233" rx="17" fill="none" stroke="#8996D9" stroke-opacity=".5" stroke-width="2"/>
  <text x="28" y="42" fill="#EAF0FF" font-family="{FONT}" font-size="18" font-weight="700">Recent merged PRs</text>
  <text x="28" y="64" fill="#A8B9D9" font-family="{FONT}" font-size="13">{escape(subtitle)} · public open-metadata repositories</text>
  <path d="M 28 170 H 494" stroke="#A8B9D9" stroke-opacity=".35" stroke-width="1"/>
  {''.join(bars)}
  <text x="28" y="219" fill="#94AACA" font-family="{FONT}" font-size="12">GitHub merged-PR search snapshot · {escape(as_of)}</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=datetime.now(timezone.utc).date(), help="Snapshot date in UTC (YYYY-MM-DD)")
    args = parser.parse_args()
    today = args.date
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    # Fetch everything before writing, so a failed or incomplete API response leaves cards intact.
    total = github_count(QUERY, token)
    months = recent_months(today)
    for month in months:
        month["count"] = github_count(f'{QUERY} merged:{month["start"]}..{month["end"]}', token)

    state_path = ASSETS / "profile-stats.json"
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    measured = {"total": total, "months": months}
    if all(previous.get(key) == value for key, value in measured.items()):
        print(f"No count changes; last snapshot {previous['as_of']}")
        return

    as_of = today.strftime("%d %b %Y")
    state = {**measured, "as_of": as_of}
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "open-source-impact.svg").write_text(impact_svg(total, as_of))
    (ASSETS / "merged-pr-activity.svg").write_text(activity_svg(months, as_of))
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Updated public PR cards: {total} merged as of {as_of}")


if __name__ == "__main__":
    main()
