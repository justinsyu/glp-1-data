---
layout: default
title: Infographics
permalink: /infographics/
description: Visual summaries generated from parsed GLP-1 congress, poster, manuscript, and presentation source documents.
---

<section class="hero">
  <h1>Infographics</h1>
</section>

{% include document_list.html documents=site.data.company_documents sort_by="year" sort_dir="desc" infographic_mode=true match_summary_spacing=true %}
