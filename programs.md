---
layout: default
title: Programs
permalink: /programs/
description: Product and pipeline entry points for GLP-1 treatment records.
---

<section class="hero">
  <h1>Programs</h1>
  <p class="lead">Product and pipeline cards are colored by their sponsoring company's palette and link to treatment-level pages.</p>
</section>

{% assign program_cards = site.data.company_programs | sort: "program" %}
<section>
  <h2>Program / Product Landing Pages</h2>
  <ul class="document-list">
    {% for program in program_cards %}
      <li data-company-color="true" style="--card-primary: {{ program.primary_color }}; --card-secondary: {{ program.secondary_color }}; --card-accent: {{ program.accent_color }};">
        <a class="topic-card-link" href="{{ program.url | relative_url }}">
          <span class="topic-card-title">{{ program.program }}</span>
          <span class="topic-card-meta">{{ program.company }} / {{ program.status }}</span>
          <span class="topic-card-description">{{ program.description }}</span>
        </a>
      </li>
    {% endfor %}
  </ul>
</section>
