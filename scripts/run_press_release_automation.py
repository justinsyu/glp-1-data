#!/usr/bin/env python3
"""Run a GLP-1 press-release source sweep and write audit artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml

from build_automation_audit import expected_from, rel


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "_data" / "company_press_releases.yml"
RUNS_DIR = ROOT / "artifacts" / "automation_runs"
USER_AGENT = "Mozilla/5.0 GLP1DataPressReleaseSweep/1.0"


@dataclass
class Candidate:
    title: str
    url: str
    date: str = ""


class PressLinkParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.links: list[dict[str, str]] = []
        self._stack: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "a" and attr_map.get("href"):
            self._stack.append({"href": urljoin(self.base_url, attr_map["href"]), "text": []})

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or not self._stack:
            return
        current = self._stack.pop()
        text = normalize_space(" ".join(current["text"]))
        if text:
            self.links.append({"href": current["href"], "text": text})

    def handle_data(self, data: str) -> None:
        for item in self._stack:
            item["text"].append(data)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def run_id() -> str:
    return "press-release-sweep-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def extract_date(text: str, href: str) -> str:
    haystack = f"{text} {href}"
    match = re.search(r"\b(20\d{2})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])\b", haystack)
    if match:
        return f"{int(match.group(1)):04d}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
    months = "January|February|March|April|May|June|July|August|September|October|November|December|Jan\\.?|Feb\\.?|Mar\\.?|Apr\\.?|Jun\\.?|Jul\\.?|Aug\\.?|Sep\\.?|Sept\\.?|Oct\\.?|Nov\\.?|Dec\\.?"
    match = re.search(rf"\b({months})\s+([0-9]{{1,2}}),\s+(20\d{{2}})\b", haystack, re.I)
    if not match:
        return ""
    lookup = {m.lower(): i for i, names in enumerate([["jan", "january"], ["feb", "february"], ["mar", "march"], ["apr", "april"], ["may"], ["jun", "june"], ["jul", "july"], ["aug", "august"], ["sep", "sept", "september"], ["oct", "october"], ["nov", "november"], ["dec", "december"]], start=1) for m in names}
    return f"{int(match.group(3)):04d}-{lookup[match.group(1).lower().rstrip('.')]:02d}-{int(match.group(2)):02d}"


def existing_keys() -> set[str]:
    rows = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8")) if DATA_PATH.exists() else []
    keys = set()
    for row in rows or []:
        if row.get("source_url"):
            keys.add(str(row["source_url"]).lower())
    return keys


def fetch(url: str, timeout: int) -> str:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    response.raise_for_status()
    return response.text


def candidates(source: dict, html: str) -> list[Candidate]:
    parser = PressLinkParser(source["source_url"])
    parser.feed(html)
    regex = re.compile(source.get("title_filter") or ".", re.I)
    source_host = host(source["source_url"])
    rows = []
    seen = set()
    for link in parser.links:
        href = link["href"].split("#", 1)[0]
        if href in seen or host(href) != source_host:
            continue
        text = normalize_space(link["text"])
        if len(text) < 4 or not regex.search(f"{text} {href}"):
            continue
        seen.add(href)
        rows.append(Candidate(text[:220], href, extract_date(text, href)))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger", default="manual")
    parser.add_argument("--run-id", default=run_id())
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--source-id", action="append", default=[])
    args = parser.parse_args(argv)

    expected = expected_from("scripts/press_release_sources.yml", "press_release")
    if args.source_id:
        selected = set(args.source_id)
        expected = [s for s in expected if s.get("source_key") in selected or s.get("source_id") in selected]
    run_dir = RUNS_DIR / args.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "expected_sources.json").write_text(json.dumps(expected, indent=2), encoding="utf-8")

    existing = existing_keys()
    worklist = []
    statuses = []
    errors = 0
    for source in expected:
        try:
            html = fetch(source["source_url"], args.timeout)
            found = candidates(source, html)
            new_items = [c for c in found if c.url.lower() not in existing]
            for item in new_items:
                worklist.append({"company": source["company_name"], "company_id": source["company_id"], "title": item.title, "date": item.date, "url": item.url, "reason": "candidate press release requires review before adding"})
            status = "checked_with_new_items" if new_items else "checked_ok" if found else "checked_no_candidates"
            statuses.append({**source, "status": status, "checked_at": now(), "candidate_count": len(found), "new_candidate_count": len(new_items), "downloaded_count": 0, "worklist_count": len(new_items)})
        except Exception as exc:
            errors += 1
            statuses.append({**source, "status": "fetch_error", "checked_at": now(), "candidate_count": 0, "new_candidate_count": 0, "downloaded_count": 0, "worklist_count": 0, "error": f"{type(exc).__name__}: {exc}"[:300]})

    with (run_dir / "source_status.jsonl").open("w", encoding="utf-8") as handle:
        for row in statuses:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    run = {"run_id": args.run_id, "run_type": "press_release", "trigger": args.trigger, "status": "partial" if errors else "success", "dry_run": False, "started_at": now(), "ended_at": now(), "expected_sources_count": len(expected), "checked_sources_count": len(expected) - errors, "error_sources_count": errors, "new_press_releases": [], "worklist_items": worklist, "downloaded_documents": [], "validations": []}
    (run_dir / "run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    import build_automation_audit
    build_automation_audit.main()
    print(json.dumps({"run_id": args.run_id, "status": run["status"], "expected_sources": len(expected), "worklist_items": len(worklist), "run_dir": rel(run_dir)}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
