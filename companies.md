---
layout: default
title: Companies
permalink: /companies/
description: Company-level entry points for the GLP-1 archive.
---

<section class="hero">
  <h1>Companies</h1>
  <p class="lead">Sponsor entry points for the GLP-1 archive. Each card uses the company's palette and links to treatment and source rows.</p>
</section>

{% assign companies = site.data.company_profiles | sort: "name" %}
<section>
  <h2>Company landing pages</h2>
  <ul class="document-list company-card-grid">
    {% for company in companies %}
      <li data-company-color="true" style="--card-primary: {{ company.primary }}; --card-secondary: {{ company.secondary }}; --card-accent: {{ company.accent }};">
        <a class="topic-card-link company-card-link" href="{{ company.page_url | relative_url }}">
          <span class="brand-chip">{{ company.code }}</span>
          {% if company.logo %}
            {% assign logo_class = company.logo_class | default: "company-card-logos" %}
            <span class="{{ logo_class }}" aria-hidden="true">
              <img class="company-card-logo" src="{{ company.logo | relative_url }}" alt="" loading="lazy">
              {% if company.secondary_logo %}
                <img class="company-card-logo company-card-logo-secondary" src="{{ company.secondary_logo | relative_url }}" alt="" loading="lazy">
              {% endif %}
            </span>
          {% endif %}
          <span class="topic-card-title">{{ company.name }}</span>
          <span class="topic-card-meta">{{ company.treatment_count }} treatments / {{ company.document_count }} source rows</span>
          <span class="topic-card-description">{{ company.description }}</span>
        </a>
      </li>
    {% endfor %}
  </ul>
</section>
