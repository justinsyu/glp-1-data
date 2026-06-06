#!/usr/bin/env python3
"""Publish parsed GLP-1 PDFs as Jekyll document pages.

The sweep downloads PDFs into:
  companies/<company_folder>/<program_slug>/{presentations_posters,published_manuscripts}/

`llamaparse.py` then writes sibling Markdown files. This script turns those
Markdown files into `/company-documents/<slug>/` pages, creates plain-text
mirrors, and merges the parsed-document rows into `_data/company_documents.json`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
COMPANIES_DIR = ROOT / "companies"
DOC_PAGES_DIR = ROOT / "company-documents"
PLAIN_TEXT_DIR = ROOT / "plain-text"
SOURCE_CATEGORIES = {
    "presentations_posters": "Presentation/Poster",
    "published_manuscripts": "Published Manuscript",
}
ACTUAL_DOCUMENT_TYPES = set(SOURCE_CATEGORIES.values())
IMAGE_LINK_RE = re.compile(r"(!\[[^\]]*]\()([^)\n]+)(\))")


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return "/" + path.relative_to(ROOT).as_posix()


def front_matter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=False) + "---\n\n"


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            title = re.sub(r"\s+", " ", match.group(1)).strip()
            if not re.fullmatch(r"Page\s+\d+", title, flags=re.I):
                return title
    return fallback


def clean_title(stem: str) -> str:
    stem = re.sub(r"^[0-9]+[_-]+", "", stem)
    stem = stem.replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", stem).strip().title()


def useful_source_title(value: str) -> str:
    title = re.sub(r"\s+", " ", value or "").strip()
    if not title or title.lower() in {"download", "save", "view pdf"}:
        return ""
    if title.lower().endswith(".pdf"):
        return clean_title(Path(title).stem)
    return title


def clean_document_title(value: str) -> str:
    title = re.sub(r"\s+", " ", value or "").strip()
    title = title.replace("\u2013", "-").replace("\u2014", "-")
    title = title.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    # LlamaParse sometimes picks up sponsor logos and poster numbers in H1 text.
    previous = ""
    while previous != title:
        previous = title
        title = re.sub(r"\s+\d{3,4}-P(?:\s+(?:Hanmi\s+)?logo)*$", "", title, flags=re.I)
        title = re.sub(r"\s+\d{3,4}(?:\s+(?:Hanmi\s+)?logo)*$", "", title, flags=re.I)
        title = re.sub(r"\s+Hanmi\s+logo$", "", title, flags=re.I)
        title = re.sub(r"\s+logo$", "", title, flags=re.I)
    return title.strip()


def rewrite_markdown_links(markdown: str, md_path: Path) -> str:
    source_dir = md_path.parent

    def repl(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if re.match(r"^[a-z]+://", target) or target.startswith("/") or target.startswith("#"):
            return match.group(0)
        rewritten_path = "/" + (source_dir / target).relative_to(ROOT).as_posix()
        rewritten = "{{ '" + rewritten_path + "' | relative_url }}"
        return f"{match.group(1)}{rewritten}{match.group(3)}"

    return IMAGE_LINK_RE.sub(repl, markdown)


def latest_download_sources() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for report in sorted((ROOT / "scripts" / "sweep" / "runs").glob("sweep-*.json")):
        data = read_json(report, {})
        for company in data.get("companies", []):
            for item in company.get("downloads", []):
                dest = item.get("dest_path")
                if not dest:
                    continue
                try:
                    key = Path(dest).resolve().relative_to(ROOT).as_posix()
                except ValueError:
                    key = Path(dest).as_posix()
                out[key] = {
                    "source_url": item.get("url", ""),
                    "source_title": item.get("title", ""),
                    "sweep_report": rel(report),
                }
    return out


def program_lookup() -> dict[tuple[str, str], dict[str, Any]]:
    treatments = read_json(ROOT / "_data" / "treatments.json", [])
    out = {}
    for row in treatments:
        out[(row.get("company_slug", ""), row.get("slug", ""))] = row
        out[(row.get("company_slug", ""), slugify(row.get("program", "")))] = row
    return out


def scan_parsed_documents() -> list[dict[str, Any]]:
    profiles = read_json(ROOT / "_data" / "company_profiles.json", [])
    profile_by_folder = {p["folder"]: p for p in profiles}
    programs = program_lookup()
    source_by_pdf = latest_download_sources()
    records: list[dict[str, Any]] = []

    for md_path in sorted(COMPANIES_DIR.glob("*/*/*/*.md")):
        parts = md_path.relative_to(COMPANIES_DIR).parts
        if len(parts) < 4:
            continue
        folder, program_slug, category = parts[0], parts[1], parts[2]
        if category not in SOURCE_CATEGORIES:
            continue
        if md_path.name.startswith("_worklist"):
            continue

        profile = profile_by_folder.get(folder)
        if not profile:
            continue
        raw_markdown = md_path.read_text(encoding="utf-8", errors="replace")
        markdown = rewrite_markdown_links(raw_markdown, md_path)
        treatment = programs.get((profile["slug"], program_slug), {})
        pdf_path = md_path.with_suffix(".pdf")
        pdf_rel = pdf_path.relative_to(ROOT).as_posix() if pdf_path.exists() else ""
        source = source_by_pdf.get(pdf_rel, {})
        fallback_title = clean_title(md_path.stem)
        heading_title = first_heading(markdown, "")
        source_title = useful_source_title(source.get("source_title", ""))
        title = clean_document_title(heading_title or source_title or fallback_title)
        page_slug = slugify(f"{profile['slug']} {program_slug} {md_path.stem}")
        page_url = f"/company-documents/{page_slug}/"
        plain_text_url = f"/plain-text/{page_slug}.txt"
        record = {
            "id": page_slug,
            "row_id": page_slug,
            "title": title,
            "url": page_url,
            "company": profile["name"],
            "company_slug": profile["slug"],
            "company_folder": folder,
            "program": treatment.get("brand") or treatment.get("name") or program_slug.replace("-", " ").title(),
            "program_slug": program_slug,
            "indication": treatment.get("indication", ""),
            "document_type": SOURCE_CATEGORIES[category],
            "category": SOURCE_CATEGORIES[category],
            "year": "",
            "conference": "",
            "local_file_url": rel(md_path),
            "markdown_file_url": rel(md_path),
            "plain_text_url": plain_text_url,
            "pdf_url": rel(pdf_path) if pdf_path.exists() else "",
            "source_url": source.get("source_url", rel(pdf_path) if pdf_path.exists() else ""),
            "source_page": source.get("source_url", ""),
            "source_file": pdf_path.name if pdf_path.exists() else md_path.name,
            "sweep_report": source.get("sweep_report", ""),
            "status": "parsed_markdown",
            "summary": f"Parsed {SOURCE_CATEGORIES[category].lower()} source document for {profile['name']}.",
            "primary_color": profile["primary"],
            "secondary_color": profile["secondary"],
            "accent_color": profile["accent"],
            "background_image": profile.get("background_image", ""),
        }
        records.append({"record": record, "markdown": markdown})

    return records


def write_pages(parsed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    DOC_PAGES_DIR.mkdir(exist_ok=True)
    PLAIN_TEXT_DIR.mkdir(exist_ok=True)
    rows: list[dict[str, Any]] = []
    for item in parsed:
        record = item["record"]
        markdown = item["markdown"].strip() + "\n"
        slug = record["id"]
        page_path = DOC_PAGES_DIR / f"{slug}.md"
        plain_path = PLAIN_TEXT_DIR / f"{slug}.txt"
        front = {
            "layout": "document",
            "title": record["title"],
            "permalink": record["url"],
            "company": record["company"],
            "company_slug": record["company_slug"],
            "program": record["program"],
            "program_slug": record["program_slug"],
            "indication": record["indication"],
            "year": record["year"],
            "conference": record["conference"],
            "document_type": record["document_type"],
            "source_file": record["source_file"],
            "pdf_url": record["pdf_url"],
            "plain_text_url": record["plain_text_url"],
            "description": record["summary"],
        }
        page_path.write_text(front_matter(front) + markdown, encoding="utf-8")
        plain_path.write_text(markdown, encoding="utf-8")
        rows.append(record)
    return rows


def main() -> int:
    existing = read_json(ROOT / "_data" / "company_documents.json", [])
    seed_rows = [
        row for row in existing
        if row.get("status") != "parsed_markdown"
        and row.get("document_type") in ACTUAL_DOCUMENT_TYPES
    ]
    parsed_rows = write_pages(scan_parsed_documents())
    by_id = {row["id"]: row for row in seed_rows}
    for row in parsed_rows:
        by_id[row["id"]] = row
    rows = sorted(by_id.values(), key=lambda r: (r.get("company", ""), r.get("program", ""), r.get("title", "")))
    (ROOT / "_data" / "company_documents.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    (ROOT / "_data" / "documents.yml").write_text(yaml.safe_dump(rows, sort_keys=False, allow_unicode=False), encoding="utf-8")
    profiles = read_json(ROOT / "_data" / "company_profiles.json", [])
    for profile in profiles:
        profile["document_count"] = len([row for row in rows if row.get("company_slug") == profile.get("slug")])
    (ROOT / "_data" / "company_profiles.json").write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf-8")
    program_rows = read_json(ROOT / "_data" / "company_programs.json", [])
    for program in program_rows:
        program["document_count"] = len([
            row for row in rows
            if row.get("company_slug") == program.get("company_slug")
            and row.get("program_slug") == program.get("program_slug")
        ])
    (ROOT / "_data" / "company_programs.json").write_text(json.dumps(program_rows, indent=2) + "\n", encoding="utf-8")
    pdf_links = [
        {"title": row["title"], "company": row["company"], "url": row.get("pdf_url") or row.get("source_url", "")}
        for row in rows
        if row.get("pdf_url") or str(row.get("source_url", "")).lower().endswith(".pdf")
    ]
    (ROOT / "_data" / "pdf_links.yml").write_text(yaml.safe_dump(pdf_links, sort_keys=False, allow_unicode=False), encoding="utf-8")
    print(f"Published {len(parsed_rows)} parsed document page(s); total company_documents rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
