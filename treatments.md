---
layout: default
title: Treatments
permalink: /treatments/
description: Complete GLP-1 treatment index.
---

<section class="hero">
  <h1>Treatments</h1>
  <p class="lead">Complete in-scope list of branded approved and investigational GLP-1-containing treatments from the supplied research file. Discontinued products and monotherapy families with generic versions are excluded.</p>
</section>

{% include treatment_list.html treatments=site.data.treatments sort_by="name" sort_dir="asc" %}
