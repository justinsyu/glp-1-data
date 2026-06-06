---
layout: default
title: GLP-1 Data Archive
description: Open index of branded and investigational GLP-1-containing treatments.
---

{% assign treatment_count = site.data.treatments | size %}
{% assign company_count = site.data.company_profiles | size %}
{% assign news_count = site.data.company_press_releases | size %}

<section class="hero">
  <h1>Branded and investigational GLP-1 treatment landscape</h1>
  <p class="lead">A GitHub Pages archive of in-scope GLP-1-containing treatments from the supplied research file, excluding discontinued products and monotherapy families with generic versions. The site keeps sponsor-specific styling, source trails, and automation-ready press/publication monitoring in the same structural pattern as the reference archive.</p>
</section>

<section class="summary-grid" aria-label="Archive summary">
  <div><strong>Treatments</strong><span>{{ treatment_count }}</span></div>
  <div><strong>Approved branded</strong><span>11</span></div>
  <div><strong>Investigational</strong><span>18</span></div>
  <div><strong>Mechanisms</strong><span>7</span></div>
  <div><strong>Companies</strong><span>{{ company_count }}</span></div>
  <div><strong>News rows</strong><span>{{ news_count }}</span></div>
</section>

<section>
  <h2>Browse</h2>
  <ul class="document-list">
    <li><a class="topic-card-link" href="{{ '/treatments/' | relative_url }}"><span class="topic-card-title">Treatments</span><span class="topic-card-description">Complete in-scope treatment list with status, route, jurisdiction, mechanism, and inclusion rationale.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/companies/' | relative_url }}"><span class="topic-card-title">Companies</span><span class="topic-card-description">Sponsor landing pages styled with company-specific palettes and program lists.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/programs/' | relative_url }}"><span class="topic-card-title">Programs</span><span class="topic-card-description">Product and pipeline entry points for each branded or investigational treatment.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/news/' | relative_url }}"><span class="topic-card-title">News</span><span class="topic-card-description">Regulatory decisions, filings, clinical data, company updates, and generic approvals separated from the document library.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/documents/' | relative_url }}"><span class="topic-card-title">Documents</span><span class="topic-card-description">Parsed publications, posters, and presentations with source pages and infographics.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/topics/' | relative_url }}"><span class="topic-card-title">Topics</span><span class="topic-card-description">Mechanism map, exclusions, and evidence notes.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/automation-audit/' | relative_url }}"><span class="topic-card-title">Automation Audit</span><span class="topic-card-description">Expected source rosters and run-level coverage for press and publication sweeps.</span></a></li>
  </ul>
</section>

<section>
  <h2>Featured mechanisms</h2>
  {% assign featured_programs = site.data.company_programs | sort: "mechanism" %}
  <ul class="document-list">
    {% for program in featured_programs limit:12 %}
      <li data-company-color="true" style="--card-primary: {{ program.primary_color }}; --card-secondary: {{ program.secondary_color }}; --card-accent: {{ program.accent_color }};">
        <a class="topic-card-link" href="{{ program.url | relative_url }}">
          <span class="topic-card-title">{{ program.program }}</span>
          <span class="topic-card-meta">{{ program.company }} / {{ program.status }}</span>
          <span class="topic-card-description">{{ program.mechanism }}</span>
        </a>
      </li>
    {% endfor %}
  </ul>
</section>
