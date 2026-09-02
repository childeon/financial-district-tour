#!/usr/bin/env python3
"""Research Wall Street tour stops with Tavily and save paste-ready notes.

Usage:
  TAVILY_API_KEY="tvly-your-key" python3 research_stops_tavily.py

The script does not edit the HTML directly. It writes tavily_research_notes.md
so you can review the source snippets before folding anything into STOPS.
"""

from __future__ import annotations

import json
import os
import textwrap
import urllib.error
import urllib.request


API_URL = "https://api.tavily.com/search"
OUTPUT_FILE = "tavily_research_notes.md"

STOPS = [
    "Fulton Center NYC transit hub Sky Reflector Net Corbin Building history",
    "Trinity Church Wall Street history Alexander Hamilton burial",
    "One Wall Street Irving Trust Red Room Art Deco conversion condos",
    "Federal Hall National Memorial Washington inauguration history",
    "New York Stock Exchange Buttonwood Agreement 1903 building history",
    "Fearless Girl statue Wall Street State Street history",
    "23 Wall Street House of Morgan 1920 bombing history",
    "Federal Reserve Bank of New York gold vault history tours",
    "Fraunces Tavern Washington farewell history 1975 bombing",
    "55 Water Street NYC history Vietnam Veterans Plaza Elevated Acre",
    "South Street Seaport Pier 17 Schermerhorn Row Wavertree history",
    "Bowling Green NYC oldest park King George III statue fence history",
    "Charging Bull Arturo Di Modica 1989 installation history",
    "Battery Park Castle Clinton immigrant depot history",
    "Goldman Sachs 200 West Street headquarters history architecture",
    "9/11 Memorial Museum Reflecting Absence design history",
    "Oculus World Trade Center Transportation Hub Calatrava history",
    "One World Trade Center 1776 feet David Childs history observatory",
    "120 Broadway Equitable Building finance insurance zoning history",
    "14 Wall Street Bankers Trust Company Building pyramid roof history",
    "40 Wall Street Bank of Manhattan Company skyscraper race history",
    "28 Liberty Street One Chase Manhattan Plaza history David Rockefeller",
    "60 Wall Street J.P. Morgan Deutsche Bank headquarters history renovation",
    "20 Exchange Place City Bank Farmers Trust Building finance history",
    "70 Pine Street Cities Service AIG finance insurance history",
    "200 Vesey Street American Express headquarters Brookfield Place future 2 WTC",
]


def tavily_search(api_key: str, query: str) -> dict:
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 6,
        "include_answer": True,
        "include_raw_content": False,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def render_notes(results: list[tuple[str, dict]]) -> str:
    sections = [
        "# Tavily Research Notes",
        "",
        "Use these notes to refresh the `STOPS` copy in `wall-street-tour.html`.",
        "The live page should stay link-free, but this file keeps URLs for review.",
        "",
    ]

    for index, (query, data) in enumerate(results, start=1):
        sections.append(f"## Stop {index}: {query}")
        answer = data.get("answer") or "No synthesized answer returned."
        sections.append("")
        sections.append(textwrap.fill(answer, width=100))
        sections.append("")
        sections.append("Source candidates:")
        for item in data.get("results", []):
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = (item.get("content") or "").replace("\n", " ")
            sections.append(f"- {title}: {url}")
            if content:
                sections.append(f"  {textwrap.shorten(content, width=260, placeholder='...')}")
        sections.append("")
        sections.append("Paste-back prompt:")
        sections.append(
            "- Rewrite this stop into 3 concise History paragraphs, 2 Today paragraphs, "
            "1 Visitor info paragraph, and 3 Fun facts. Keep it factual, no links in the app."
        )
        sections.append("")

    return "\n".join(sections)


def main() -> None:
    api_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Missing TAVILY_API_KEY. Run: "
            'TAVILY_API_KEY="tvly-your-key" python3 research_stops_tavily.py'
        )

    results: list[tuple[str, dict]] = []
    for query in STOPS:
        print(f"Researching: {query}")
        try:
            results.append((query, tavily_search(api_key, query)))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            results.append((query, {"answer": f"HTTP {exc.code}: {body}", "results": []}))
        except Exception as exc:
            results.append((query, {"answer": f"Error: {exc}", "results": []}))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(render_notes(results))

    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
