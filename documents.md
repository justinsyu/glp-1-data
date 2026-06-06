---
layout: default
title: Documents
permalink: /documents/
description: External source document index for the GLP-1 archive.
---

{% assign presentation_documents = site.data.company_documents | where: "document_type", "Presentation/Poster" %}
{% assign manuscript_documents = site.data.company_documents | where: "document_type", "Published Manuscript" %}
{% assign actual_documents = presentation_documents | concat: manuscript_documents %}
{% assign actual_document_count = actual_documents | size %}

<section class="hero">
  <h1>Documents</h1>
  <p class="lead">Publications, posters, and presentations with parsed source pages in the archive. Regulatory decisions, sponsor news, topline updates, and generic approval evidence now live on News.</p>
</section>

<section class="summary-grid" aria-label="Document source summary">
  <div><strong>Documents</strong><span>{{ actual_document_count }}</span></div>
  <div><strong>Poster and presentation rows</strong><span>{{ presentation_documents | size }}</span></div>
  <div><strong>Publication rows</strong><span>{{ manuscript_documents | size }}</span></div>
  <div><strong>Other source rows</strong><span><a href="{{ '/news/' | relative_url }}">News</a></span></div>
</section>

{% include document_list.html documents=actual_documents sort_by="year" sort_dir="desc" %}
