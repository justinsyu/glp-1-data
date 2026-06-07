---
layout: default
title: News
permalink: /news/
description: Non-document GLP-1 source rows, including regulatory decisions, filings, clinical data, company updates, and generic approvals.
---

{% assign regulatory_decisions = site.data.company_press_releases | where: "category", "Regulatory decision" %}
{% assign regulatory_filings = site.data.company_press_releases | where: "category", "Regulatory filing" %}
{% assign clinical_data = site.data.company_press_releases | where: "category", "Clinical data" %}
{% assign company_updates = site.data.company_press_releases | where: "category", "Company update" %}
{% assign generic_approvals = site.data.company_press_releases | where: "category", "Generic approval" %}
{% assign news_count = site.data.company_press_releases | size %}

<section class="hero">
  <h1>News</h1>
</section>

<section class="summary-grid summary-grid-six summary-grid-no-top summary-grid-toolbar-aligned" aria-label="News source summary">
  <div><strong>Articles</strong><span>{{ news_count }}</span></div>
  <div><strong>Regulatory decisions</strong><span>{{ regulatory_decisions | size }}</span></div>
  <div><strong>Regulatory filings</strong><span>{{ regulatory_filings | size }}</span></div>
  <div><strong>Clinical data</strong><span>{{ clinical_data | size }}</span></div>
  <div><strong>Company updates</strong><span>{{ company_updates | size }}</span></div>
  <div><strong>Generic approvals</strong><span>{{ generic_approvals | size }}</span></div>
</section>

{% include press_release_list.html releases=site.data.company_press_releases sort_by="date" sort_dir="desc" %}
