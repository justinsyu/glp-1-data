---
layout: default
title: Treatments
permalink: /treatments/
description: Complete GLP-1 treatment index.
---

<section class="hero">
  <h1>Treatments</h1>
</section>

{% include treatment_list.html treatments=site.data.treatments sort_by="name" sort_dir="asc" match_summary_spacing=true %}
