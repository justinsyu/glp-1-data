---
layout: document_infographic
title: "Poster: Pemvidutide, a glucagon-like peptide 1/glucagon dual receptor agonist, improves metabolic dysfunction-associated steatohepatitis activity and fibrosis in a clinical quantitative systems pharmacology model"
permalink: /infographics/altimmune-pemvidutide-158d0d4d-73c3-4223-8e85-a3dee7ca2104/
company: "Altimmune"
company_slug: "altimmune"
source_url: "/company-documents/altimmune-pemvidutide-158d0d4d-73c3-4223-8e85-a3dee7ca2104/"
source_title: "Poster: Pemvidutide, a glucagon-like peptide 1/glucagon dual receptor agonist, improves metabolic dysfunction-associated steatohepatitis activity and fibrosis in a clinical quantitative systems pharmacology model"
program: "Pemvidutide"
indication: "MASH; obesity"
year: "2024"
conference: "EASL Congress"
document_type: "Presentation/Poster"
pdf_url: ""
description: "Infographic version of Poster: Pemvidutide, a glucagon-like peptide 1/glucagon dual receptor agonist, improves metabolic dysfunction-associated steatohepatitis activity and fibrosis in a clinical quantitative systems pharmacology model, generated from the parsed source markdown."
---

<section>
  <h2>Model headline</h2>
  <div class="stat-grid" aria-label="QSP model headline numbers">
    <div class="stat">
      <span class="stat-value">24<span class="stat-unit">weeks</span></span>
      <span class="stat-label">Pemvidutide 1.2 mg and 1.8 mg once weekly dosing period used to calibrate quantitative effects</span>
    </div>
    <div class="stat">
      <span class="stat-value">0.0</span>
      <span class="stat-label">Predicted NAS score at Week 24 with pemvidutide 1.8 mg QW</span>
    </div>
    <div class="stat">
      <span class="stat-value">1<span class="stat-unit">point</span></span>
      <span class="stat-label">Median MASH fibrosis improvement predicted at Week 24 for pemvidutide 1.8 mg</span>
    </div>
    <div class="stat">
      <span class="stat-value">100</span>
      <span class="stat-label">Participants in the simulated MASH cohort</span>
    </div>
  </div>
</section>

<section>
  <h2>Study at a glance</h2>
  <div class="flow-diagram" aria-label="QSP modeling workflow">
    <div>NAFLDsym QSP model</div>
    <div>1-compartment pemvidutide pharmacokinetic profiles</div>
    <div>Clinical trial calibration in MASLD and/or overweight/obesity</div>
    <div>Simulated MASH cohort predictions over 24 weeks</div>
  </div>
  <div class="callout">
    <strong>Source model interpretation</strong>
    <p>Model simulations predict that the dual GLP-1/glucagon receptor agonism of pemvidutide will produce greater reductions in MASH NAS, liver fat, and fibrosis than GLP-1R mono-agonists.</p>
  </div>

  <table>
    <thead><tr><th>Measure</th><th>MASH SimCohort</th><th>MASLD Phase 1 1.2 mg</th><th>MASLD Phase 1 1.8 mg</th><th>Obesity Phase 2 1.2 mg</th><th>Obesity Phase 2 1.8 mg</th></tr></thead>
    <tbody>
      <tr><td>n</td><td>100</td><td>23</td><td>23</td><td>40</td><td>40</td></tr>
      <tr><td>Body Weight, kg (SD)</td><td>105.7 (22.1)</td><td>102.4 (14.6)</td><td>98.9 (19.7)</td><td>100.0 (20.4)</td><td>102.1 (17.7)</td></tr>
      <tr><td>LFC, % (SD)</td><td>25.0 (8.1)</td><td>21.6 (7.3)</td><td>21.8 (8.0)</td><td>NA</td><td>NA</td></tr>
      <tr><td>ALT, U/L (SD)</td><td>48.5 (9.2)</td><td>32.4 (13.8)</td><td>36.4 (15.6)</td><td>24.8 (13.1)</td><td>23.7 (13.3)</td></tr>
      <tr><td>NAS, (SD)</td><td>4.7 (1.3)</td><td>NA</td><td>NA</td><td>NA</td><td>NA</td></tr>
      <tr><td>Fibrosis Stage, (SD)</td><td>2.2 (0.9)</td><td>NA</td><td>NA</td><td>NA</td><td>NA</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h2>NAS score over 24 weeks</h2>
  <h3>Pemvidutide effects</h3>
  <svg class="svg-chart" data-interactive="line" viewBox="0 0 720 320" role="img" aria-labelledby="nas-pem-title">
    <title id="nas-pem-title">Simulated NAS score over 24 weeks with pemvidutide</title>
    <line class="axis" x1="60" y1="270" x2="690" y2="270"/>
    <line class="axis" x1="60" y1="20" x2="60" y2="270"/>
    <line class="grid-line" x1="60" y1="91" x2="690" y2="91"/>
    <line class="grid-line" x1="60" y1="163" x2="690" y2="163"/>
    <line class="grid-line" x1="60" y1="234" x2="690" y2="234"/>
    <line class="hover-guide" x1="0" y1="20" x2="0" y2="270"/>
    <polyline class="line" points="100,20 190,74 280,109 370,145 460,163 550,181 640,199"/>
    <polyline class="line alt" points="100,20 190,91 280,145 370,181 460,216 550,252 640,270"/>
    <circle class="point" cx="100" cy="20" r="4" data-x="Week 0" data-y="7.0 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="190" cy="74" r="4" data-x="Week 4" data-y="5.5 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="280" cy="109" r="4" data-x="Week 8" data-y="4.5 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="370" cy="145" r="4" data-x="Week 12" data-y="3.5 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="460" cy="163" r="4" data-x="Week 16" data-y="3.0 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="550" cy="181" r="4" data-x="Week 20" data-y="2.5 NAS score" data-series="1.2 mg QW"/>
    <circle class="point" cx="640" cy="199" r="4" data-x="Week 24" data-y="2.0 NAS score" data-series="1.2 mg QW"/>
    <circle class="point alt" cx="100" cy="20" r="4" data-x="Week 0" data-y="7.0 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="190" cy="91" r="4" data-x="Week 4" data-y="5.0 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="280" cy="145" r="4" data-x="Week 8" data-y="3.5 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="370" cy="181" r="4" data-x="Week 12" data-y="2.5 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="460" cy="216" r="4" data-x="Week 16" data-y="1.5 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="550" cy="252" r="4" data-x="Week 20" data-y="0.5 NAS score" data-series="1.8 mg QW"/>
    <circle class="point alt" cx="640" cy="270" r="4" data-x="Week 24" data-y="0.0 NAS score" data-series="1.8 mg QW"/>
    <text class="tick-label" x="100" y="292" text-anchor="middle">0</text><text class="tick-label" x="190" y="292" text-anchor="middle">4</text><text class="tick-label" x="280" y="292" text-anchor="middle">8</text><text class="tick-label" x="370" y="292" text-anchor="middle">12</text><text class="tick-label" x="460" y="292" text-anchor="middle">16</text><text class="tick-label" x="550" y="292" text-anchor="middle">20</text><text class="tick-label" x="640" y="292" text-anchor="middle">24</text>
    <text class="axis-label" x="24" y="145" transform="rotate(-90 24 145)" text-anchor="middle">NAS score</text>
  </svg>
  <div class="chart-legend"><span><i></i> 1.2 mg QW</span><span><i class="alt"></i> 1.8 mg QW</span></div>
  <details class="data-table-toggle">
    <summary>Show data table</summary>
    <table>
      <thead><tr><th>Time (weeks)</th><th>1.2 mg QW</th><th>1.8 mg QW</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>7.0</td><td>7.0</td></tr><tr><td>4</td><td>5.5</td><td>5.0</td></tr><tr><td>8</td><td>4.5</td><td>3.5</td></tr><tr><td>12</td><td>3.5</td><td>2.5</td></tr><tr><td>16</td><td>3.0</td><td>1.5</td></tr><tr><td>20</td><td>2.5</td><td>0.5</td></tr><tr><td>24</td><td>2.0</td><td>0.0</td></tr>
      </tbody>
    </table>
  </details>

  <h3>Receptor contribution to NAS</h3>
  <div class="evidence-grid evidence-grid-2">
    <article class="evidence-card">
      <h3>GLP-1 RA only</h3>
      <p>GLP-1 receptor agonism alone was predicted to reduce NAS score from 7.0 at Week 0 to 5.0 at Week 24 for both 1.2 mg QW and 1.8 mg QW.</p>
    </article>
    <article class="evidence-card">
      <h3>Glucagon RA only</h3>
      <p>Glucagon RA only effects were predicted to reduce NAS score from 7.0 at Week 0 to 3.0 at Week 24 for 1.2 mg QW and to 2.0 at Week 24 for 1.8 mg QW.</p>
    </article>
  </div>
  <details class="data-table-toggle">
    <summary>Show receptor contribution tables</summary>
    <table>
      <thead><tr><th>Time (weeks)</th><th>GLP-1 1.2 mg QW</th><th>GLP-1 1.8 mg QW</th><th>Glucagon 1.2 mg QW</th><th>Glucagon 1.8 mg QW</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>7.0</td><td>7.0</td><td>7.0</td><td>7.0</td></tr><tr><td>4</td><td>6.5</td><td>6.5</td><td>6.0</td><td>5.5</td></tr><tr><td>8</td><td>6.0</td><td>6.0</td><td>5.0</td><td>4.5</td></tr><tr><td>12</td><td>5.5</td><td>5.5</td><td>4.5</td><td>3.5</td></tr><tr><td>16</td><td>5.5</td><td>5.5</td><td>4.0</td><td>3.0</td></tr><tr><td>20</td><td>5.0</td><td>5.0</td><td>3.5</td><td>2.5</td></tr><tr><td>24</td><td>5.0</td><td>5.0</td><td>3.0</td><td>2.0</td></tr>
      </tbody>
    </table>
  </details>
</section>

<section>
  <h2>Weight loss and liver fat correlations</h2>
  <svg class="svg-chart" data-interactive="line" viewBox="0 0 720 320" role="img" aria-labelledby="weight-title">
    <title id="weight-title">Simulated median weight loss over 24 weeks</title>
    <line class="axis" x1="60" y1="270" x2="690" y2="270"/><line class="axis" x1="60" y1="30" x2="60" y2="270"/>
    <line class="grid-line" x1="60" y1="90" x2="690" y2="90"/><line class="grid-line" x1="60" y1="150" x2="690" y2="150"/><line class="grid-line" x1="60" y1="210" x2="690" y2="210"/>
    <line class="hover-guide" x1="0" y1="20" x2="0" y2="270"/>
    <polyline class="line" points="100,30 190,75 280,120 370,150 460,180 550,195 640,210"/>
    <polyline class="line alt" points="100,30 190,90 280,150 370,195 460,225 550,255 640,270"/>
    <circle class="point" cx="100" cy="30" r="4" data-x="Week 0" data-y="0% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="190" cy="75" r="4" data-x="Week 4" data-y="-3% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="280" cy="120" r="4" data-x="Week 8" data-y="-6% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="370" cy="150" r="4" data-x="Week 12" data-y="-8% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="460" cy="180" r="4" data-x="Week 16" data-y="-10% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="550" cy="195" r="4" data-x="Week 20" data-y="-11% simulated median weight loss" data-series="1.2 mg QW"/><circle class="point" cx="640" cy="210" r="4" data-x="Week 24" data-y="-12% simulated median weight loss" data-series="1.2 mg QW"/>
    <circle class="point alt" cx="100" cy="30" r="4" data-x="Week 0" data-y="0% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="190" cy="90" r="4" data-x="Week 4" data-y="-4% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="280" cy="150" r="4" data-x="Week 8" data-y="-8% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="370" cy="195" r="4" data-x="Week 12" data-y="-11% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="460" cy="225" r="4" data-x="Week 16" data-y="-13% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="550" cy="255" r="4" data-x="Week 20" data-y="-15% simulated median weight loss" data-series="1.8 mg QW"/><circle class="point alt" cx="640" cy="270" r="4" data-x="Week 24" data-y="-16% simulated median weight loss" data-series="1.8 mg QW"/>
    <text class="axis-label" x="24" y="150" transform="rotate(-90 24 150)" text-anchor="middle">Simulated median %</text>
  </svg>
  <div class="chart-legend"><span><i></i> 1.2 mg QW</span><span><i class="alt"></i> 1.8 mg QW</span></div>
  <details class="data-table-toggle">
    <summary>Show data table</summary>
    <table>
      <thead><tr><th>Time (weeks)</th><th>1.2 mg QW (Simulated Median %)</th><th>1.8 mg QW (Simulated Median %)</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>0</td><td>0</td></tr><tr><td>4</td><td>-3</td><td>-4</td></tr><tr><td>8</td><td>-6</td><td>-8</td></tr><tr><td>12</td><td>-8</td><td>-11</td></tr><tr><td>16</td><td>-10</td><td>-13</td></tr><tr><td>20</td><td>-11</td><td>-15</td></tr><tr><td>24</td><td>-12</td><td>-16</td></tr>
      </tbody>
    </table>
  </details>

  <svg class="svg-chart" data-interactive="line" viewBox="0 0 720 320" role="img" aria-labelledby="lfc-corr-title">
    <title id="lfc-corr-title">Simulated median liver fat reduction over 12 weeks</title>
    <line class="axis" x1="60" y1="270" x2="690" y2="270"/><line class="axis" x1="60" y1="30" x2="60" y2="270"/>
    <line class="grid-line" x1="60" y1="96" x2="690" y2="96"/><line class="grid-line" x1="60" y1="163" x2="690" y2="163"/><line class="grid-line" x1="60" y1="230" x2="690" y2="230"/>
    <line class="hover-guide" x1="0" y1="20" x2="0" y2="270"/>
    <polyline class="line" points="100,30 280,150 460,203 640,230"/>
    <polyline class="line alt" points="100,30 280,190 460,257 640,270"/>
    <circle class="point" cx="100" cy="30" r="4" data-x="Week 0" data-y="0% simulated median liver fat change" data-series="1.2 mg QW"/><circle class="point" cx="280" cy="150" r="4" data-x="Week 4" data-y="-45% simulated median liver fat change" data-series="1.2 mg QW"/><circle class="point" cx="460" cy="203" r="4" data-x="Week 8" data-y="-65% simulated median liver fat change" data-series="1.2 mg QW"/><circle class="point" cx="640" cy="230" r="4" data-x="Week 12" data-y="-75% simulated median liver fat change" data-series="1.2 mg QW"/>
    <circle class="point alt" cx="100" cy="30" r="4" data-x="Week 0" data-y="0% simulated median liver fat change" data-series="1.8 mg QW"/><circle class="point alt" cx="280" cy="190" r="4" data-x="Week 4" data-y="-60% simulated median liver fat change" data-series="1.8 mg QW"/><circle class="point alt" cx="460" cy="257" r="4" data-x="Week 8" data-y="-85% simulated median liver fat change" data-series="1.8 mg QW"/><circle class="point alt" cx="640" cy="270" r="4" data-x="Week 12" data-y="-90% simulated median liver fat change" data-series="1.8 mg QW"/>
    <text class="axis-label" x="24" y="150" transform="rotate(-90 24 150)" text-anchor="middle">Simulated median %</text>
  </svg>
  <div class="chart-legend"><span><i></i> 1.2 mg QW</span><span><i class="alt"></i> 1.8 mg QW</span></div>
  <details class="data-table-toggle">
    <summary>Show data table</summary>
    <table>
      <thead><tr><th>Time (weeks)</th><th>1.2 mg QW (Simulated Median %)</th><th>1.8 mg QW (Simulated Median %)</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>0</td><td>0</td></tr><tr><td>4</td><td>-45</td><td>-60</td></tr><tr><td>8</td><td>-65</td><td>-85</td></tr><tr><td>12</td><td>-75</td><td>-90</td></tr>
      </tbody>
    </table>
  </details>
</section>

<section>
  <h2>Liver fat content and fibrosis</h2>
  <div class="evidence-grid evidence-grid-2">
    <article class="evidence-card">
      <h3>Liver fat content</h3>
      <p>Pemvidutide effects were predicted to lower LFC from 25 at Week 0 to 4 at Week 24 for 1.2 mg QW and to 1 at Week 24 for 1.8 mg QW.</p>
    </article>
    <article class="evidence-card">
      <h3>Fibrosis</h3>
      <p>Pemvidutide effects were predicted to lower fibrosis stage from 2.2 at Week 0 to 1.7 at Week 24 for 1.2 mg QW and to 1.2 at Week 24 for 1.8 mg QW.</p>
    </article>
  </div>
  <details class="data-table-toggle">
    <summary>Show liver fat content and fibrosis tables</summary>
    <table>
      <thead><tr><th>Time (weeks)</th><th>Pemvidutide LFC 1.2 mg</th><th>Pemvidutide LFC 1.8 mg</th><th>GLP-1 LFC 1.2 mg</th><th>GLP-1 LFC 1.8 mg</th><th>Glucagon LFC 1.2 mg</th><th>Glucagon LFC 1.8 mg</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td></tr><tr><td>4</td><td>15</td><td>10</td><td>22</td><td>22</td><td>18</td><td>15</td></tr><tr><td>8</td><td>10</td><td>5</td><td>20</td><td>20</td><td>14</td><td>10</td></tr><tr><td>12</td><td>8</td><td>3</td><td>19</td><td>19</td><td>12</td><td>8</td></tr><tr><td>16</td><td>6</td><td>2</td><td>18</td><td>18</td><td>10</td><td>6</td></tr><tr><td>20</td><td>5</td><td>1</td><td>18</td><td>18</td><td>9</td><td>5</td></tr><tr><td>24</td><td>4</td><td>1</td><td>18</td><td>18</td><td>8</td><td>4</td></tr>
      </tbody>
    </table>

    <table>
      <thead><tr><th>Time (weeks)</th><th>Pemvidutide fibrosis 1.2 mg</th><th>Pemvidutide fibrosis 1.8 mg</th><th>GLP-1 fibrosis 1.2 mg</th><th>GLP-1 fibrosis 1.8 mg</th><th>Glucagon fibrosis 1.2 mg</th><th>Glucagon fibrosis 1.8 mg</th></tr></thead>
      <tbody>
        <tr><td>0</td><td>2.2</td><td>2.2</td><td>2.2</td><td>2.2</td><td>2.2</td><td>2.2</td></tr><tr><td>4</td><td>2.2</td><td>2.1</td><td>2.2</td><td>2.2</td><td>2.2</td><td>2.1</td></tr><tr><td>8</td><td>2.1</td><td>2.0</td><td>2.2</td><td>2.2</td><td>2.1</td><td>2.0</td></tr><tr><td>12</td><td>2.0</td><td>1.8</td><td>2.2</td><td>2.2</td><td>2.0</td><td>1.9</td></tr><tr><td>16</td><td>1.9</td><td>1.6</td><td>2.2</td><td>2.2</td><td>1.9</td><td>1.8</td></tr><tr><td>20</td><td>1.8</td><td>1.4</td><td>2.2</td><td>2.2</td><td>1.8</td><td>1.7</td></tr><tr><td>24</td><td>1.7</td><td>1.2</td><td>2.2</td><td>2.2</td><td>1.7</td><td>1.6</td></tr>
      </tbody>
    </table>
  </details>
</section>

<section>
  <h2>Source conclusions</h2>
  <div class="callout">
    <strong>QSP model conclusion</strong>
    <p>The QSP model predicted additive effects of GLP-1 and GCGR agonism in pemvidutide on reducing MASH LFC, NAS, and fibrosis, and suggested pemvidutide will have successful outcomes on MASH resolution and fibrosis improvement endpoints in an ongoing 24-week MASH clinical trial.</p>
  </div>
</section>

<p class="infographic-caption">Source: <a href="/company-documents/altimmune-pemvidutide-158d0d4d-73c3-4223-8e85-a3dee7ca2104/">Poster: Pemvidutide, a glucagon-like peptide 1/glucagon dual receptor agonist, improves metabolic dysfunction-associated steatohepatitis activity and fibrosis in a clinical quantitative systems pharmacology model</a>.</p>
