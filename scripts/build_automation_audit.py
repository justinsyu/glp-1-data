#!/usr/bin/env python3
"""Build GLP-1 automation audit data from configured sources and run ledgers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "artifacts" / "automation_runs"
OUTPUT = ROOT / "_data" / "automation_audit.json"

LABELS = {
    "publication": "Publication",
    "press_release": "Press Release",
    "checked_ok": "Checked OK",
    "checked_no_candidates": "Checked No Candidates",
    "checked_with_new_items": "Checked With New Items",
    "fetch_error": "Fetch Error",
    "parse_error": "Parse Error",
    "success": "Success",
    "partial": "Partial",
    "failed": "Failed",
    "not_run": "Not Run",
}


def label(value: Any) -> str:
    text = str(value or "")
    return LABELS.get(text, " ".join(part.capitalize() for part in text.replace("_", " ").split()))


def rel(path: Path | str | None) -> str:
    if not path:
        return ""
    p = Path(path)
    if p.is_absolute():
        try:
            return p.relative_to(ROOT).as_posix()
        except ValueError:
            return p.as_posix()
    return p.as_posix().replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def read_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return yaml.safe_load(path.read_text(encoding="utf-8")) or default


def expected_from(path: str, family: str) -> list[dict[str, Any]]:
    raw = read_yaml(ROOT / path, {"companies": []})
    rows = []
    for company in raw.get("companies", []):
        for index, source in enumerate(company.get("sources") or [], start=1):
            rows.append({
                "source_key": f"{family}:{company.get('id')}:{index}",
                "source_family": family,
                "source_family_label": label(family),
                "run_type": family,
                "company_id": company.get("id", ""),
                "company_slug": company.get("company_slug", ""),
                "company_name": company.get("name", ""),
                "tier": company.get("tier", ""),
                "source_index": index,
                "source_kind": source.get("kind", "press_release_index" if family == "press_release" else "html"),
                "source_url": source.get("url", ""),
                "pubmed_terms": source.get("terms", []),
                "fetcher": source.get("fetcher", "requests"),
                "fetcher_label": label(source.get("fetcher", "requests")),
                "title_filter": source.get("title_filter", ""),
                "discovery_only": bool(source.get("discovery_only", False)),
                "status": "pending",
            })
    return rows


def expected_publication_sources() -> list[dict[str, Any]]:
    raw = read_yaml(ROOT / "scripts" / "sweep" / "sources.yaml", {"companies": []})
    profiles = read_json(ROOT / "_data" / "company_profiles.json", [])
    slug_by_folder = {profile.get("folder", ""): profile.get("slug", "") for profile in profiles}
    rows = []
    for company in raw.get("companies", []):
        company_folder = str(company.get("folder", "")).replace("\\", "/").split("/")[-1]
        company_slug = company.get("company_slug", "") or slug_by_folder.get(company_folder, "")
        for index, source in enumerate(company.get("sources") or [], start=1):
            kind = source.get("kind", "html")
            if kind == "skip":
                status = "skipped_by_config"
            else:
                status = "pending"
            rows.append({
                "source_key": f"publication:{company.get('id')}:{index}",
                "source_family": "publication",
                "source_family_label": label("publication"),
                "run_type": "publication",
                "company_id": company.get("id", ""),
                "company_slug": company_slug,
                "company_name": company.get("name", ""),
                "tier": company.get("tier", ""),
                "source_index": index,
                "source_kind": kind,
                "source_url": source.get("url", ""),
                "pubmed_terms": source.get("terms", []),
                "fetcher": source.get("fetcher", "pubmed" if kind == "pubmed" else "requests"),
                "fetcher_label": label(source.get("fetcher", "pubmed" if kind == "pubmed" else "requests")),
                "title_filter": source.get("title_filter", ""),
                "discovery_only": bool(source.get("discovery_only", False)),
                "expected_dest": source.get("dest", ""),
                "dest_worklist": source.get("dest_worklist", ""),
                "status": status,
            })
    return rows


def expected_sources() -> list[dict[str, Any]]:
    return (
        expected_publication_sources()
        + expected_from("scripts/press_release_sources.yml", "press_release")
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"status": "parse_error", "error": "invalid JSONL row"})
    return rows


def summarize_run(run_dir: Path) -> dict[str, Any]:
    run = read_json(run_dir / "run.json", {})
    expected = read_json(run_dir / "expected_sources.json", [])
    statuses = read_jsonl(run_dir / "source_status.jsonl")
    latest = {s.get("source_key") or s.get("source_id"): s for s in statuses}
    source_rows = []
    for source in expected:
        status = latest.get(source.get("source_key")) or latest.get(source.get("source_id")) or {}
        terminal_status = status.get("status", "missing")
        source_rows.append({
            **source,
            "terminal_status": terminal_status,
            "terminal_status_label": label(terminal_status),
            "checked_at": status.get("checked_at", ""),
            "candidate_count": status.get("candidate_count", 0),
            "new_candidate_count": status.get("new_candidate_count", 0),
            "downloaded_count": status.get("downloaded_count", 0),
            "worklist_count": status.get("worklist_count", 0),
            "error": status.get("error", ""),
        })
    error_rows = [s for s in source_rows if s["terminal_status"] in {"fetch_error", "parse_error", "missing"}]
    status_value = run.get("status") or ("partial" if error_rows else "success")
    return {
        "run_id": run.get("run_id", run_dir.name),
        "run_type": run.get("run_type", ""),
        "run_type_label": label(run.get("run_type", "")),
        "trigger": run.get("trigger", ""),
        "status": status_value,
        "status_label": label(status_value),
        "dry_run": bool(run.get("dry_run", False)),
        "started_at": run.get("started_at", ""),
        "ended_at": run.get("ended_at", ""),
        "run_dir": rel(run_dir),
        "expected_sources_count": len(expected),
        "checked_sources_count": len([s for s in source_rows if s["terminal_status"] != "missing"]),
        "missing_sources_count": len([s for s in source_rows if s["terminal_status"] == "missing"]),
        "error_sources_count": len(error_rows),
        "downloaded_documents_count": len(run.get("downloaded_documents", []) or []),
        "worklist_items_count": len(run.get("worklist_items", []) or []),
        "new_press_releases_count": len(run.get("new_press_releases", []) or []),
        "source_statuses": source_rows,
        "missing_sources": [s for s in source_rows if s["terminal_status"] == "missing"],
        "error_sources": error_rows,
        "downloaded_documents": run.get("downloaded_documents", []) or [],
        "worklist_items": run.get("worklist_items", []) or [],
        "new_press_releases": run.get("new_press_releases", []) or [],
        "validations": run.get("validations", []) or [],
    }


def automation_runs() -> list[dict[str, Any]]:
    if not RUNS_DIR.exists():
        return []
    runs = [summarize_run(path) for path in RUNS_DIR.iterdir() if path.is_dir() and (path / "run.json").exists()]
    runs.sort(key=lambda row: (row.get("started_at", ""), row.get("run_id", "")), reverse=True)
    return runs


def build() -> dict[str, Any]:
    expected = expected_sources()
    runs = automation_runs()
    latest = runs[0] if runs else {}
    findings = []
    if latest:
        for row in latest.get("missing_sources", []):
            findings.append({"severity": "high", "severity_label": "High", "kind": "missing_source", "kind_label": "Missing Source", "company": row.get("company_name", ""), "source": row.get("source_url") or ", ".join(row.get("pubmed_terms", [])), "detail": "Expected source has no terminal audit status."})
        for row in latest.get("error_sources", []):
            if row.get("terminal_status") != "missing":
                findings.append({"severity": "medium", "severity_label": "Medium", "kind": "source_error", "kind_label": "Source Error", "company": row.get("company_name", ""), "source": row.get("source_url") or ", ".join(row.get("pubmed_terms", [])), "detail": row.get("error", "")})
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "in_scope_companies": len({r["company_id"] for r in expected}),
            "publication_expected_sources": len([r for r in expected if r["source_family"] == "publication"]),
            "press_release_expected_sources": len([r for r in expected if r["source_family"] == "press_release"]),
            "expected_sources": len(expected),
            "configured_skips": 0,
            "automation_runs": len(runs),
            "latest_run_id": latest.get("run_id", ""),
            "latest_run_status": latest.get("status", "not_run"),
            "latest_run_status_label": label(latest.get("status", "not_run")),
            "latest_run_started_at": latest.get("started_at", ""),
            "latest_checked_sources": latest.get("checked_sources_count", 0),
            "latest_expected_sources": latest.get("expected_sources_count", len(expected)),
            "latest_downloaded_documents": latest.get("downloaded_documents_count", 0),
            "latest_worklist_items": latest.get("worklist_items_count", 0),
            "latest_error_sources": latest.get("error_sources_count", 0),
            "open_findings": len(findings),
        },
        "expected_sources": expected,
        "runs": runs,
        "recent_sweep_runs": [],
        "findings": findings,
    }


def main() -> int:
    OUTPUT.write_text(json.dumps(build(), indent=2), encoding="utf-8")
    print(f"Wrote {rel(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
