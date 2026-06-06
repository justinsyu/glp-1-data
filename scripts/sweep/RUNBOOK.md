# GLP-1 Document Sweep Runbook

This sweep is the repeatable workflow for official GLP-1 congress presentations, posters, manuscripts, and sponsor presentation PDFs.

## Source Of Truth

`scripts/sweep/sources.yaml` is the company-by-company playbook. Each company entry records:

- official company, medical-information, investor, or publication pages to revisit
- direct official PDF URLs when a known poster or presentation has already been identified
- search filters for the in-scope GLP-1 products
- destination folders under `companies/<company_folder>/<program_slug>/`
- manual worklist files for gated medical-information pages or non-PDF landing pages

## Storage Contract

Downloaded PDFs belong in one of:

- `companies/<company_folder>/<program_slug>/presentations_posters/`
- `companies/<company_folder>/<program_slug>/published_manuscripts/`

After download, run LlamaParse against the folder. The parser writes sibling Markdown files and extracted images:

```powershell
python llamaparse.py companies/kailera/ribupatide/presentations_posters --fallback local
```

For a full refresh after a sweep, run the parser on every destination folder that contains PDFs:

```powershell
Get-ChildItem companies -Recurse -Directory |
  Where-Object { $_.Name -in @("presentations_posters", "published_manuscripts") -and (Get-ChildItem $_.FullName -Filter *.pdf -File -ErrorAction SilentlyContinue) } |
  ForEach-Object { python llamaparse.py $_.FullName --fallback local }
```

Then publish parsed Markdown to the Jekyll site:

```powershell
python scripts/build_document_pages.py
python scripts/build_infographic_manifest.py --output scripts/infographic_manifest.json
```

Each manifest record can be assigned to a subagent using `scripts/infographic_generation_prompt.md`.

## First-Time Setup

```powershell
python -m pip install -r scripts/sweep/requirements.txt
python -m playwright install chromium
```

Optional document parsing and infographic authoring dependencies:

```powershell
python -m pip install -r scripts/document_pipeline_requirements.txt
```

If using cloud parsing, set one of the LlamaCloud API key names already supported by `llamaparse.py`, such as `LLAMA_CLOUD_API_KEY`, in `.env` or the shell environment.

Current dependency note: `llama-cloud-services` works with the Retina parser script, but pip reports it as deprecated and maintained only until May 1, 2026. For now, keep the copied Retina-compatible script for parity. A future maintenance pass should test `llama-cloud>=1.0` and only switch once output image links and markdown structure remain compatible with `scripts/build_document_pages.py`.

## Validate

```powershell
python -m scripts.sweep.smoke
```

This checks the YAML schema and destination folders without network calls.

## Run Discovery And Download

```powershell
python -m scripts.sweep
```

Useful subsets:

```powershell
python -m scripts.sweep --companies kailera,hanmi,eccogene_astrazeneca
python -m scripts.sweep --tier 1
python -m scripts.sweep --dry-run
```

The audited wrapper mirrors the Retina automation pattern and refreshes `/automation-audit/` data:

```powershell
python scripts/run_publication_automation.py --trigger manual
```

## Manual Retrieval

Some medical-information portals require HCP attestation or render PDFs behind JavaScript workflows. Those sources are marked `discovery_only: true`. New candidates are appended to the configured `_worklist_pending_*.md` file. Retrieve those PDFs in a real browser, save them into the suggested destination folder, then run:

```powershell
python llamaparse.py <destination-folder> --fallback local
python scripts/build_document_pages.py
```

## Infographics

After document pages exist:

```powershell
python scripts/build_infographic_manifest.py --output scripts/infographic_manifest.json
```

For each record in the manifest, launch one subagent with `scripts/infographic_generation_prompt.md`. The generated page must use `layout: document_infographic`, cite the parsed source document, and preserve the source-traceable chart-first style.

The manifest intentionally omits rows that have no parsed Markdown yet. If a sponsor source title disagrees with the parsed PDF heading, prefer the parsed heading: `scripts/build_document_pages.py` uses LlamaParse headings before sweep-link titles for this reason.
