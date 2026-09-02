# Tavily research workflow

Paste your key into the command, not into the HTML:

```bash
TAVILY_API_KEY="tvly-your-key-here" python3 research_stops_tavily.py
```

The script writes `tavily_research_notes.md` with:

- a Tavily synthesized answer for each stop
- source candidate URLs for review
- a paste-back prompt for rewriting each stop into the page format

The live tour page intentionally contains no source links in the stop text.
