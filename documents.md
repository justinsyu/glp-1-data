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
</section>

<section class="summary-grid summary-grid-no-top summary-grid-toolbar-aligned" aria-label="Document source summary">
  <div><strong>Total</strong><span>{{ actual_document_count }}</span></div>
  <div><strong>Posters and Presentations</strong><span>{{ presentation_documents | size }}</span></div>
  <div><strong>Publications</strong><span>{{ manuscript_documents | size }}</span></div>
</section>

{% include document_list.html documents=actual_documents sort_by="year" sort_dir="desc" %}
