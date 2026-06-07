---
layout: default
title: Automation audit dashboard
permalink: /automation-audit/
description: Run-level audit dashboard for GLP-1 publication and press release automation.
---

{% assign audit = site.data.automation_audit %}
{% assign summary = audit.summary %}
{% assign latest_run = audit.runs | first %}

<section class="hero audit-index-hero">
  <h1>Automation Audit</h1>
</section>

<section class="summary-grid audit-summary-grid" aria-label="Automation audit summary">
  <div><strong>Companies</strong><span>{{ summary.in_scope_companies }}</span></div>
  <div><strong>Expected Sources</strong><span>{{ summary.expected_sources }}</span></div>
  <div><strong>Pub Sources</strong><span>{{ summary.publication_expected_sources }}</span></div>
  <div><strong>Press Sources</strong><span>{{ summary.press_release_expected_sources }}</span></div>
  <div><strong>Latest Coverage</strong><span>{{ summary.latest_checked_sources }} / {{ summary.latest_expected_sources }}</span></div>
  <div><strong>Latest Status</strong><span>{{ summary.latest_run_status_label | default: summary.latest_run_status }}</span></div>
  <div><strong>Open Findings</strong><span>{{ summary.open_findings }}</span></div>
</section>

<section class="audit-panel">
  <h2>Latest Run</h2>
  {% if latest_run %}
    <dl class="metadata">
      <div>
        <dt>Run ID</dt>
        <dd><code>{{ latest_run.run_id }}</code></dd>
      </div>
      <div>
        <dt>Started</dt>
        <dd><code>{{ latest_run.started_at | default: "(not recorded)" }}</code></dd>
      </div>
      <div>
        <dt>Type</dt>
        <dd>{{ latest_run.run_type_label | default: latest_run.run_type }}</dd>
      </div>
      <div>
        <dt>Mode</dt>
        <dd>{% if latest_run.dry_run %}<span class="status-pill status-warning">Dry Run</span>{% else %}<span class="status-pill status-ok">Live Run</span>{% endif %}</dd>
      </div>
      <div>
        <dt>Status</dt>
        <dd><span class="status-pill status-{{ latest_run.status }}">{{ latest_run.status_label | default: latest_run.status }}</span></dd>
      </div>
      <div>
        <dt>Coverage</dt>
        <dd>{{ latest_run.checked_sources_count }} / {{ latest_run.expected_sources_count }}</dd>
      </div>
      <div>
        <dt>Worklist</dt>
        <dd>{{ latest_run.worklist_items_count }}</dd>
      </div>
      <div>
        <dt>Errors</dt>
        <dd>{{ latest_run.error_sources_count }}</dd>
      </div>
    </dl>
  {% else %}
    <p class="lead">No automation run records found.</p>
  {% endif %}
</section>

<section>
  <h2>Expected Source Roster</h2>
  <p class="lead">Every active row for the relevant automation type should appear in each run's terminal source-status ledger.</p>
  <table class="audit-table audit-wide-table">
    <thead><tr><th>Type</th><th>Company</th><th>Tier</th><th>Fetcher</th><th>Source</th><th>Mode</th></tr></thead>
    <tbody>
      {% for source in audit.expected_sources %}
        <tr>
          <td>{{ source.source_family_label | default: source.source_family }}</td>
          <td>{{ source.company_name }}</td>
          <td>{{ source.tier }}</td>
          <td>{{ source.fetcher_label | default: source.fetcher }}</td>
          <td>{% if source.source_url %}<a href="{{ source.source_url }}" rel="noopener">{{ source.source_url }}</a>{% elsif source.pubmed_terms %}<code>{{ source.pubmed_terms | join: " OR " }}</code>{% else %}<span>{{ source.skip_reason | default: "(not configured)" }}</span>{% endif %}</td>
          <td>{% if source.discovery_only %}<span class="status-pill status-warning">Manual Review</span>{% else %}<span class="status-pill status-ok">Automated</span>{% endif %}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</section>

<section>
  <h2>Automation Runs</h2>
  {% if audit.runs.size == 0 %}
    <p class="lead">No automation run records found.</p>
  {% else %}
    <table class="audit-table audit-wide-table">
      <thead><tr><th>Run</th><th>Type</th><th>Status</th><th>Started</th><th>Coverage</th><th>Worklist</th><th>Errors</th></tr></thead>
      <tbody>
        {% for run in audit.runs limit:25 %}
          <tr><td><code>{{ run.run_id }}</code></td><td>{{ run.run_type_label | default: run.run_type }}</td><td><span class="status-pill status-{{ run.status }}">{{ run.status_label | default: run.status }}</span></td><td><code>{{ run.started_at }}</code></td><td>{{ run.checked_sources_count }} / {{ run.expected_sources_count }}</td><td>{{ run.worklist_items_count }}</td><td>{{ run.error_sources_count }}</td></tr>
        {% endfor %}
      </tbody>
    </table>
  {% endif %}
</section>
