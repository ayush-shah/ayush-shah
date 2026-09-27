#!/usr/bin/env python3
"""Render profile cards from public GitHub PR search and contribution calendar."""

from __future__ import annotations

import argparse
import calendar
import json
import os
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
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


class CalendarParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: dict[date, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "td":
            return
        values = dict(attrs)
        if "data-date" not in values or "data-level" not in values:
            return
        day = date.fromisoformat(values["data-date"] or "")
        level = int(values["data-level"] or "")
        if not 0 <= level <= 4 or day in self.days:
            raise ValueError(f"Invalid public contribution calendar cell for {day}")
        self.days[day] = level


def public_calendar() -> dict[date, int]:
    request = Request(
        "https://github.com/users/ayush-shah/contributions",
        headers={"Accept": "text/html", "User-Agent": "Mozilla/5.0 (ayush-shah-profile-stats)"},
    )
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = CalendarParser()
    parser.feed(html)
    if len(parser.days) < 180:
        raise ValueError("GitHub's public contribution calendar was incomplete")
    return parser.days


def six_months_before(day: date) -> date:
    absolute_month = day.year * 12 + day.month - 1 - 6
    year, month_zero = divmod(absolute_month, 12)
    month = month_zero + 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


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


def activity_svg(start: date, end: date, levels: dict[date, int], as_of: str) -> str:
    active_days = sum(level > 0 for level in levels.values())
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)
    colors = ("#26334D", "#315E77", "#287D92", "#31BEAF", "#69E7CE")
    cells = []
    month_labels = []
    day = start
    while day <= end:
        week = (day - grid_start).days // 7
        weekday = (day.weekday() + 1) % 7
        x, y = 58 + 16 * week, 151 + 14 * weekday
        cells.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="3" fill="{colors[levels[day]]}"/>')
        if day.day == 1:
            month_labels.append(f'<text x="{x}" y="137" fill="#A8B9D9" font-family="{FONT}" font-size="12">{day.strftime("%b")}</text>')
        day += timedelta(days=1)
    swatches = ''.join(f'<rect x="{76 + i * 15}" y="260" width="11" height="11" rx="3" fill="{color}"/>' for i, color in enumerate(colors))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="285" viewBox="0 0 520 285" role="img" aria-labelledby="title desc">
  <title id="title">GitHub contribution activity</title>
  <desc id="desc">{active_days} days with contributions shown on Ayush Shah's public GitHub calendar from {start.isoformat()} through {end.isoformat()}. Snapshot {escape(as_of)}.</desc>
  <defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#151B39"/><stop offset="1" stop-color="#103942"/></linearGradient></defs>
  <rect width="520" height="285" rx="18" fill="url(#bg)"/>
  <rect x="1" y="1" width="518" height="283" rx="17" fill="none" stroke="#8996D9" stroke-opacity=".5" stroke-width="2"/>
  <text x="28" y="39" fill="#BFCDF1" font-family="{FONT}" font-size="15" font-weight="700" letter-spacing="2">GITHUB ACTIVITY</text>
  <text x="26" y="110" fill="#F6F9FF" font-family="{FONT}" font-size="74" font-weight="800" letter-spacing="-3">{active_days}</text>
  <text x="174" y="78" fill="#EAF0FF" font-family="{FONT}" font-size="18" font-weight="700">days with contributions</text>
  <text x="174" y="102" fill="#AFC7D8" font-family="{FONT}" font-size="15">in the past six months</text>
  {''.join(month_labels)}
  <text x="27" y="178" fill="#A8B9D9" font-family="{FONT}" font-size="11">Mon</text>
  <text x="27" y="206" fill="#A8B9D9" font-family="{FONT}" font-size="11">Wed</text>
  <text x="27" y="234" fill="#A8B9D9" font-family="{FONT}" font-size="11">Fri</text>
  {''.join(cells)}
  <text x="28" y="270" fill="#94AACA" font-family="{FONT}" font-size="12">Less</text>{swatches}<text x="157" y="270" fill="#94AACA" font-family="{FONT}" font-size="12">More</text>
  <text x="248" y="270" fill="#94AACA" font-family="{FONT}" font-size="12">Public GitHub calendar · {escape(as_of)}</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=datetime.now(timezone.utc).date(), help="Snapshot date in UTC (YYYY-MM-DD)")
    args = parser.parse_args()
    today = args.date
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    # Fetch everything before writing, so a failed or incomplete response leaves cards intact.
    total = github_count(QUERY, token)
    calendar_days = public_calendar()
    latest = max(calendar_days)
    if latest < today - timedelta(days=2) or latest > today + timedelta(days=1):
        raise ValueError(f"GitHub's public contribution calendar ended on unexpected date {latest}")
    end = min(today, latest)
    start = six_months_before(end)
    dates = (start + timedelta(days=index) for index in range((end - start).days + 1))
    if any(day not in calendar_days for day in dates):
        raise ValueError("GitHub's public contribution calendar has missing days")
    levels = {day: calendar_days[day] for day in sorted(calendar_days) if start <= day <= end}
    active_dates = {day.isoformat(): level for day, level in levels.items() if level > 0}

    state_path = ASSETS / "profile-stats.json"
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    measured = {"total": total, "active_dates": active_dates}
    if all(previous.get(key) == value for key, value in measured.items()):
        print(f"No activity changes; last snapshot {previous['as_of']}")
        return

    as_of = end.strftime("%d %b %Y")
    state = {**measured, "activity_from": start.isoformat(), "activity_through": end.isoformat(), "active_days": len(active_dates), "as_of": as_of}
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "open-source-impact.svg").write_text(impact_svg(total, as_of))
    (ASSETS / "contribution-activity.svg").write_text(activity_svg(start, end, levels, as_of))
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Updated profile cards: {total} merged public PRs, {len(active_dates)} active days as of {as_of}")


if __name__ == "__main__":
    main()
