#!/usr/bin/env python3
"""Generate the static GLP-1 Jekyll data and pages.

The source list is intentionally small and explicit so treatment inclusion can
be audited. It is derived from the user-provided GLP-1 research attachment, with
recent volatile milestones checked against sponsor/regulator/publication pages.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


COMPANIES = [
    {
        "slug": "eli-lilly",
        "code": "LLY",
        "folder": "eli_lilly",
        "name": "Eli Lilly and Company",
        "short_name": "Lilly",
        "description": "Commercial and investigational incretin portfolio spanning dulaglutide, tirzepatide, orforglipron, and retatrutide.",
        "primary": "#d52b1e",
        "secondary": "#7a1d18",
        "accent": "#f5b5a8",
        "highlight": "#5b2c83",
        "brand_site": "https://www.lilly.com/",
    },
    {
        "slug": "novo-nordisk",
        "code": "NVO",
        "folder": "novo_nordisk",
        "name": "Novo Nordisk",
        "short_name": "Novo",
        "description": "Late-stage GLP-1 and amylin portfolio focused on CagriSema, amycretin/zenagamtide, and insulin combination products.",
        "primary": "#001965",
        "secondary": "#0072ce",
        "accent": "#7ad0ff",
        "highlight": "#65a6d9",
        "brand_site": "https://www.novonordisk.com/",
    },
    {
        "slug": "sanofi",
        "code": "SNY",
        "folder": "sanofi",
        "name": "Sanofi",
        "short_name": "Sanofi",
        "description": "Active fixed-dose insulin glargine and lixisenatide combination franchise.",
        "primary": "#7a00e6",
        "secondary": "#23004d",
        "accent": "#00a3e0",
        "highlight": "#ff5f7e",
        "brand_site": "https://www.sanofi.com/",
    },
    {
        "slug": "amgen",
        "code": "AMGN",
        "folder": "amgen",
        "name": "Amgen",
        "short_name": "Amgen",
        "description": "MariTide / maridebart cafraglutide Phase 3 obesity and cardiometabolic development program.",
        "primary": "#005daa",
        "secondary": "#0072ce",
        "accent": "#00b5e2",
        "highlight": "#103858",
        "brand_site": "https://www.amgen.com/",
    },
    {
        "slug": "innovent",
        "code": "INNV",
        "folder": "innovent",
        "name": "Innovent Biologics",
        "short_name": "Innovent",
        "description": "China-approved mazdutide GCG/GLP-1 dual receptor agonist, licensed from Lilly for Greater China.",
        "primary": "#006b54",
        "secondary": "#00a887",
        "accent": "#f0c64a",
        "highlight": "#173f5f",
        "brand_site": "https://www.innoventbio.com/",
    },
    {
        "slug": "sciwind-pfizer",
        "code": "SCI",
        "folder": "sciwind_pfizer",
        "name": "Sciwind Biosciences / Pfizer China",
        "short_name": "Sciwind / Pfizer",
        "description": "Ecnoglutide China approvals and additional Sciwind-origin GLP-1 pipeline assets.",
        "primary": "#0099a8",
        "secondary": "#005eb8",
        "accent": "#69d2e7",
        "highlight": "#002f6c",
        "brand_site": "https://www.sciwind.com/",
    },
    {
        "slug": "shanghai-benemae",
        "code": "BENE",
        "folder": "shanghai_benemae",
        "name": "Shanghai Benemae Pharmaceutical",
        "short_name": "Benemae",
        "description": "China-branded native GLP-1 receptor agonist beinaglutide for T2D and weight management.",
        "primary": "#0f766e",
        "secondary": "#134e4a",
        "accent": "#a7f3d0",
        "highlight": "#0891b2",
        "brand_site": "https://www.benemae.com/",
    },
    {
        "slug": "huadong-jiuyuan",
        "code": "HDJG",
        "folder": "huadong_jiuyuan",
        "name": "Huadong Medicine / Jiuyuan Gene",
        "short_name": "Huadong / Jiuyuan",
        "description": "China-approved PEG-loxenatide weekly GLP-1 receptor agonist franchise.",
        "primary": "#005bac",
        "secondary": "#123c69",
        "accent": "#37b34a",
        "highlight": "#6aaee8",
        "brand_site": "https://www.eastchinapharm.com/",
    },
    {
        "slug": "innogen",
        "code": "INNO",
        "folder": "innogen",
        "name": "Innogen Pharmaceutical",
        "short_name": "Innogen",
        "description": "Efsubaglutide alfa / supaglutide Fc-fusion GLP-1 receptor agonist approved in China for T2D.",
        "primary": "#1d4ed8",
        "secondary": "#0f172a",
        "accent": "#38bdf8",
        "highlight": "#22c55e",
        "brand_site": "https://www.innogenpharm.com/",
    },
    {
        "slug": "gan-and-lee",
        "code": "GLP",
        "folder": "gan_and_lee",
        "name": "Gan & Lee Pharmaceuticals",
        "short_name": "Gan & Lee",
        "description": "Bofanglutide / GZR18 long-acting GLP-1 program in obesity and T2D trials.",
        "primary": "#0055a4",
        "secondary": "#00a3ad",
        "accent": "#f6c343",
        "highlight": "#0b3d91",
        "brand_site": "https://www.ganlee.com/",
    },
    {
        "slug": "hengrui",
        "code": "HRS",
        "folder": "hengrui",
        "name": "Hengrui Pharma",
        "short_name": "Hengrui",
        "description": "Noiiglutide / SHR20004 GLP-1 mono-agonist and broader metabolic R&D from Jiangsu Hengrui.",
        "primary": "#004b87",
        "secondary": "#0f2f5f",
        "accent": "#d71920",
        "highlight": "#37b5d6",
        "brand_site": "https://www.hengrui.com/en",
    },
    {
        "slug": "kailera",
        "code": "KAI",
        "folder": "kailera",
        "name": "Kailera Therapeutics",
        "short_name": "Kailera",
        "description": "Ribupatide / HRS9531 / KAI-9531 dual GIP/GLP-1 global development program.",
        "primary": "#007f89",
        "secondary": "#00313c",
        "accent": "#82c0c7",
        "highlight": "#d2fbf2",
        "brand_site": "https://www.kailera.com/",
    },
    {
        "slug": "hanmi",
        "code": "HNM",
        "folder": "hanmi",
        "name": "Hanmi Pharmaceutical",
        "short_name": "Hanmi",
        "description": "Efpeglenatide, efocipegtrutide, and licensed efinopegdutide incretin assets.",
        "primary": "#c8102e",
        "secondary": "#4d4d4f",
        "accent": "#f2a900",
        "highlight": "#0067b1",
        "brand_site": "https://www.hanmipharm.com/",
    },
    {
        "slug": "structure-therapeutics",
        "code": "GPCR",
        "folder": "structure_therapeutics",
        "name": "Structure Therapeutics",
        "short_name": "Structure",
        "description": "Oral small-molecule GLP-1 receptor agonist aleniglipron / GSBR-1290.",
        "primary": "#172554",
        "secondary": "#2563eb",
        "accent": "#f97316",
        "highlight": "#14b8a6",
        "brand_site": "https://www.structuretx.com/",
    },
    {
        "slug": "eccogene-astrazeneca",
        "code": "AZD",
        "folder": "eccogene_astrazeneca",
        "name": "Eccogene / AstraZeneca",
        "short_name": "Eccogene / AstraZeneca",
        "description": "Oral small-molecule GLP-1 receptor agonist elecoglipron / ECC5004 / AZD5004.",
        "primary": "#830051",
        "secondary": "#003865",
        "accent": "#00a3e0",
        "highlight": "#f0ab00",
        "brand_site": "https://www.astrazeneca.com/",
    },
    {
        "slug": "roche-carmot",
        "code": "RHHBY",
        "folder": "roche_carmot",
        "name": "Roche / Carmot Therapeutics",
        "short_name": "Roche / Carmot",
        "description": "Oral small-molecule GLP-1 receptor agonist CT-996 inherited through Carmot.",
        "primary": "#003da5",
        "secondary": "#0b1f4d",
        "accent": "#00aeef",
        "highlight": "#f4c542",
        "brand_site": "https://www.roche.com/",
    },
    {
        "slug": "viking-therapeutics",
        "code": "VKTX",
        "folder": "viking_therapeutics",
        "name": "Viking Therapeutics",
        "short_name": "Viking",
        "description": "VK2735 injectable and oral dual GIP/GLP-1 obesity development program.",
        "primary": "#0b3d91",
        "secondary": "#1d4ed8",
        "accent": "#f59e0b",
        "highlight": "#22d3ee",
        "brand_site": "https://www.vikingtherapeutics.com/",
    },
    {
        "slug": "boehringer-zealand",
        "code": "BI-ZL",
        "folder": "boehringer_zealand",
        "name": "Boehringer Ingelheim / Zealand Pharma",
        "short_name": "Boehringer / Zealand",
        "description": "Survodutide GLP-1/glucagon receptor dual agonist in obesity and MASH development.",
        "primary": "#005f61",
        "secondary": "#003b49",
        "accent": "#00a0af",
        "highlight": "#ef476f",
        "brand_site": "https://www.boehringer-ingelheim.com/",
    },
    {
        "slug": "altimmune",
        "code": "ALT",
        "folder": "altimmune",
        "name": "Altimmune",
        "short_name": "Altimmune",
        "description": "Pemvidutide GLP-1/glucagon dual agonist in MASH and obesity.",
        "primary": "#005eb8",
        "secondary": "#003b5c",
        "accent": "#8dc63f",
        "highlight": "#00a9e0",
        "brand_site": "https://www.altimmune.com/",
    },
    {
        "slug": "merck-hanmi",
        "code": "MRK",
        "folder": "merck_hanmi",
        "name": "Merck / Hanmi",
        "short_name": "Merck / Hanmi",
        "description": "Efinopegdutide / MK-6024 GLP-1/glucagon dual agonist for MASH.",
        "primary": "#00857c",
        "secondary": "#243746",
        "accent": "#78be20",
        "highlight": "#00b2a9",
        "brand_site": "https://www.merck.com/",
    },
    {
        "slug": "united-labs-novo",
        "code": "UBT",
        "folder": "united_labs_novo",
        "name": "United Laboratories / Novo Nordisk",
        "short_name": "United Labs / Novo",
        "description": "UBT251 triple agonist, with Novo Nordisk ex-Greater China rights.",
        "primary": "#0f766e",
        "secondary": "#001965",
        "accent": "#60a5fa",
        "highlight": "#f59e0b",
        "brand_site": "https://www.tul.com.cn/",
    },
]


TREATMENTS = [
    ("dulaglutide", "Dulaglutide", "Trulicity", "eli-lilly", "Pure GLP-1 receptor agonist", "Approved branded", "SC weekly", "US, EU, others", "T2D; CV risk reduction in T2D", "Included because Trulicity remains an active branded product and no approved dulaglutide generic is listed in the seed scope."),
    ("beinaglutide", "Beinaglutide", "Yishengtai; Feisumei", "shanghai-benemae", "Pure GLP-1 receptor agonist", "Approved branded", "SC multiple daily", "China", "T2D; obesity/overweight", "Included as an active China-approved branded GLP-1 product."),
    ("peg-loxenatide", "PEG-loxenatide / PEX168", "Fulaimei / Jinglixin", "huadong-jiuyuan", "Pure GLP-1 receptor agonist", "Approved branded", "SC weekly", "China", "T2D", "Included as an active China-approved branded long-acting GLP-1 product."),
    ("efsubaglutide-alfa", "Efsubaglutide alfa / supaglutide", "Yinuoqing / Diabegone", "innogen", "Pure GLP-1 receptor agonist", "Approved branded", "SC weekly", "China; Macau", "T2D", "Included as an active China-approved branded Fc-fusion GLP-1 product."),
    ("ecnoglutide", "Ecnoglutide / XW003", "Xianyida; Xianweiying", "sciwind-pfizer", "Pure GLP-1 receptor agonist", "Approved branded", "SC weekly", "China", "T2D; obesity/overweight", "Included as an active branded China-approved cAMP-biased GLP-1 product."),
    ("bofanglutide", "Bofanglutide / GZR18", "", "gan-and-lee", "Pure GLP-1 receptor agonist", "Investigational", "SC weekly or q2w", "China and US trials", "Obesity/overweight; T2D", "Included as an active investigational GLP-1 program."),
    ("noiiglutide", "Noiiglutide / SHR20004", "", "hengrui", "Pure GLP-1 receptor agonist", "Investigational", "SC daily", "China trials", "Obesity", "Included as an active investigational Hengrui GLP-1 mono-agonist."),
    ("efpeglenatide", "Efpeglenatide", "", "hanmi", "Pure GLP-1 receptor agonist", "Investigational", "SC weekly", "Korea / Asia-centered", "Obesity; T2D", "Included as a non-discontinued investigational/late-stage GLP-1 program."),
    ("utreglutide", "Utreglutide / GL0034", "", "sciwind-pfizer", "Pure GLP-1 receptor agonist", "Investigational", "SC", "Early clinical", "Metabolic disease / obesity", "Included as an investigational Sciwind-origin GLP-1 asset with unclear but not discontinued status in the seed."),
    ("orforglipron", "Orforglipron", "Foundayo", "eli-lilly", "Oral small-molecule GLP-1 receptor agonist", "Approved branded", "Oral daily", "US", "Obesity/overweight with comorbidity", "Included as an active FDA-approved branded oral GLP-1 product."),
    ("aleniglipron", "Aleniglipron / GSBR-1290", "", "structure-therapeutics", "Oral small-molecule GLP-1 receptor agonist", "Investigational", "Oral daily", "Global trials", "Obesity; T2D", "Included as an active investigational oral GLP-1 program."),
    ("elecoglipron", "Elecoglipron / ECC5004 / AZD5004", "", "eccogene-astrazeneca", "Oral small-molecule GLP-1 receptor agonist", "Investigational", "Oral daily", "Global / China trials", "Obesity; T2D", "Included as an active investigational oral GLP-1 program."),
    ("ct-996", "CT-996", "", "roche-carmot", "Oral small-molecule GLP-1 receptor agonist", "Investigational", "Oral daily", "Global trials", "Obesity; T2D", "Included as an active investigational oral GLP-1 program."),
    ("tirzepatide", "Tirzepatide", "Mounjaro; Zepbound", "eli-lilly", "Dual GIP/GLP-1 receptor agonist", "Approved branded", "SC weekly", "US, EU, China, Japan, others", "T2D; obesity/overweight; OSA with obesity", "Included as an active branded dual incretin product with no generic version."),
    ("maritide", "Maridebart cafraglutide / MariTide / AMG 133", "", "amgen", "Dual GIP/GLP-1 receptor agonist", "Investigational", "SC monthly or less frequent", "Global trials", "Obesity and obesity-related conditions", "Included as an active Phase 3 investigational incretin program."),
    ("ribupatide", "Ribupatide / HRS9531 / KAI-9531", "", "kailera", "Dual GIP/GLP-1 receptor agonist", "Investigational", "SC weekly; oral form in development", "China and global trials", "Obesity/overweight", "Included as an active Kailera global investigational program originated from Hengrui science."),
    ("vk2735", "VK2735", "", "viking-therapeutics", "Dual GIP/GLP-1 receptor agonist", "Investigational", "SC weekly; oral form in trials", "Global trials", "Obesity/overweight; T2D", "Included as an active investigational dual incretin program."),
    ("mazdutide", "Mazdutide / IBI362 / LY3305677", "", "innovent", "Dual GLP-1/glucagon receptor agonist", "Approved branded", "SC weekly", "China", "Obesity/overweight; T2D", "Included as an active China-approved GLP-1/glucagon dual receptor agonist."),
    ("survodutide", "Survodutide / BI 456906", "", "boehringer-zealand", "Dual GLP-1/glucagon receptor agonist", "Investigational", "SC weekly", "Global trials", "Obesity; T2D; MASH", "Included as an active investigational GLP-1/glucagon program."),
    ("pemvidutide", "Pemvidutide", "", "altimmune", "Dual GLP-1/glucagon receptor agonist", "Investigational", "SC weekly", "US / global trials", "MASH; obesity", "Included as an active investigational GLP-1/glucagon program."),
    ("efinopegdutide", "Efinopegdutide / MK-6024 / HM12525A", "", "merck-hanmi", "Dual GLP-1/glucagon receptor agonist", "Investigational", "SC weekly", "Global trials", "MASH / metabolic disease", "Included as an active investigational GLP-1/glucagon program."),
    ("retatrutide", "Retatrutide / LY3437943", "", "eli-lilly", "Triple GIP/GLP-1/glucagon receptor agonist", "Investigational", "SC weekly", "Global Phase 3", "Obesity/overweight; T2D; obesity-related comorbidities", "Included as an active Phase 3 triple agonist program."),
    ("ubt251", "UBT251", "", "united-labs-novo", "Triple GIP/GLP-1/glucagon receptor agonist", "Investigational", "SC", "China and global trials", "Obesity; T2D", "Included as an active investigational triple agonist program."),
    ("efocipegtrutide", "Efocipegtrutide / HM15211", "", "hanmi", "Triple GIP/GLP-1/glucagon receptor agonist", "Investigational", "SC weekly", "Global / Korea trials", "MASH", "Included as an active investigational triple agonist program."),
    ("cagrisema", "CagriSema", "", "novo-nordisk", "GLP-1/amylin combination", "Investigational filed/late-stage", "SC weekly", "US / EU / global", "Obesity/overweight; T2D", "Included as an active branded investigational fixed-combination program."),
    ("amycretin", "Amycretin / zenagamtide", "", "novo-nordisk", "GLP-1/amylin combination", "Investigational", "Oral and SC programs", "Global trials", "Obesity/overweight", "Included as an active investigational GLP-1/amylin program."),
    ("xultophy", "Insulin degludec / liraglutide", "Xultophy", "novo-nordisk", "Insulin + GLP-1 fixed-dose combination", "Approved branded FDC", "SC daily", "US, EU, others", "T2D", "Included because the fixed-dose combination remains an active branded product, even though liraglutide monotherapy has generic exposure."),
    ("soliqua-suliqua", "Insulin glargine / lixisenatide", "Soliqua; Suliqua", "sanofi", "Insulin + GLP-1 fixed-dose combination", "Approved branded FDC", "SC daily", "US, EU, others", "T2D", "Included because the fixed-dose combination remains active even though standalone lixisenatide is withdrawn in key markets."),
    ("kyinsu", "Insulin icodec / semaglutide", "Kyinsu", "novo-nordisk", "Insulin + GLP-1 fixed-dose combination", "Approved branded FDC", "SC weekly", "EU; Korea reported", "T2D", "Included because Kyinsu is an active branded fixed-dose combination, even though semaglutide monotherapy has generic exposure in some markets."),
]


LOGO_ASSETS = {
    "eli-lilly": {"logo": "/assets/img/company-logos/eli-lilly.svg"},
    "novo-nordisk": {"logo": "/assets/img/company-logos/novo-nordisk-wordmark.png", "logo_class": "company-card-logos logo-wide logo-novo"},
    "sanofi": {"logo": "/assets/img/company-logos/sanofi-wordmark.svg", "logo_class": "company-card-logos logo-wide"},
    "amgen": {"logo": "/assets/img/company-logos/amgen.svg"},
    "innovent": {"logo": "/assets/img/company-logos/innovent.png"},
    "sciwind-pfizer": {"logo": "/assets/img/company-logos/sciwind.png", "secondary_logo": "/assets/img/company-logos/pfizer.svg"},
    "shanghai-benemae": {"logo": "/assets/img/company-logos/benemae.png", "logo_class": "company-card-logos logo-on-dark logo-wide"},
    "huadong-jiuyuan": {"logo": "/assets/img/company-logos/huadong.png"},
    "innogen": {"logo": "/assets/img/company-logos/innogen.png"},
    "gan-and-lee": {"logo": "/assets/img/company-logos/gan-and-lee.png", "logo_class": "company-card-logos logo-on-dark logo-wide"},
    "hengrui": {"logo": "/assets/img/company-logos/hengrui.png", "logo_class": "company-card-logos logo-tall"},
    "kailera": {"logo": "/assets/img/company-logos/kailera.svg", "logo_class": "company-card-logos logo-on-dark logo-wide"},
    "hanmi": {"logo": "/assets/img/company-logos/hanmi.svg"},
    "structure-therapeutics": {"logo": "/assets/img/company-logos/structure-therapeutics.png", "logo_class": "company-card-logos logo-on-dark logo-wide"},
    "eccogene-astrazeneca": {"logo": "/assets/img/company-logos/eccogene.png", "secondary_logo": "/assets/img/company-logos/astrazeneca.png"},
    "roche-carmot": {"logo": "/assets/img/company-logos/roche-wordmark.svg", "logo_class": "company-card-logos logo-wide"},
    "viking-therapeutics": {"logo": "/assets/img/company-logos/viking.png"},
    "boehringer-zealand": {"logo": "/assets/img/company-logos/boehringer-ingelheim.svg", "secondary_logo": "/assets/img/company-logos/zealand.svg"},
    "altimmune": {"logo": "/assets/img/company-logos/altimmune.png"},
    "merck-hanmi": {"logo": "/assets/img/company-logos/merck.svg", "secondary_logo": "/assets/img/company-logos/hanmi.svg"},
    "united-labs-novo": {"logo": "/assets/img/company-logos/united-labs.png", "secondary_logo": "/assets/img/company-logos/novo-nordisk-wordmark.png"},
}


SOURCES = [
    {
        "id": "fda-foundayo",
        "title": "FDA approves Foundayo (orforglipron)",
        "date": "2026-04-01",
        "company_slug": "eli-lilly",
        "program": "Foundayo / orforglipron",
        "category": "Regulatory decision",
        "indication": "Obesity",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-approves-first-new-molecular-entity-under-national-priority-voucher-program",
        "summary": "FDA approval of Lilly's oral GLP-1 orforglipron for adults with obesity or overweight with weight-related medical problems.",
    },
    {
        "id": "lilly-retatrutide-triumph1",
        "title": "Retatrutide TRIUMPH-1 Phase 3 obesity topline results",
        "date": "2026-05-21",
        "company_slug": "eli-lilly",
        "program": "Retatrutide",
        "category": "Clinical data",
        "indication": "Obesity",
        "url": "https://investor.lilly.com/news-releases/news-release-details/lillys-triple-agonist-retatrutide-delivered-powerful-weight-loss",
        "summary": "Lilly reported Phase 3 TRIUMPH-1 body-weight reductions for retatrutide in obesity or overweight without diabetes.",
    },
    {
        "id": "fda-zepbound-osa",
        "title": "FDA approves Zepbound as first medication for obstructive sleep apnea",
        "date": "2024-12-20",
        "company_slug": "eli-lilly",
        "program": "Zepbound / tirzepatide",
        "category": "Regulatory decision",
        "indication": "OSA with obesity",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-approves-first-medication-obstructive-sleep-apnea",
        "summary": "FDA approval of Zepbound for moderate-to-severe obstructive sleep apnea in adults with obesity.",
    },
    {
        "id": "novo-cagrisema-nda",
        "title": "Novo Nordisk submits CagriSema NDA for obesity",
        "date": "2025-12-18",
        "company_slug": "novo-nordisk",
        "program": "CagriSema",
        "category": "Regulatory filing",
        "indication": "Obesity",
        "url": "https://www.novonordisk.com/news-and-media/news-and-ir-materials/news-details.html?id=916470",
        "summary": "Novo Nordisk announced U.S. NDA submission for once-weekly CagriSema based on REDEFINE 1 and REDEFINE 2.",
    },
    {
        "id": "amgen-maritide-phase3",
        "title": "Amgen reports MariTide Phase 3 program progress",
        "date": "2026-02-03",
        "company_slug": "amgen",
        "program": "MariTide",
        "category": "Company update",
        "indication": "Obesity and cardiometabolic disease",
        "url": "https://www.amgen.com/newsroom/press-releases/2026/02/amgen-reports-fourth-quarter-and-full-year-2025-financial-results",
        "summary": "Amgen listed ongoing MARITIME Phase 3 chronic weight management, cardiovascular, heart failure, and OSA studies for MariTide.",
    },
    {
        "id": "innovent-mazdutide-approval",
        "title": "Innovent announces mazdutide NMPA approval for chronic weight management",
        "date": "2025-06-27",
        "company_slug": "innovent",
        "program": "Mazdutide",
        "category": "Regulatory decision",
        "indication": "Obesity/overweight",
        "url": "https://www.nasdaq.com/press-release/innovent-announces-mazdutide-first-dual-gcg-glp-1-receptor-agonist-received-approval",
        "summary": "Innovent announced China NMPA approval of mazdutide for chronic weight management.",
    },
    {
        "id": "innovent-mazdutide-t2d",
        "title": "Innovent notes mazdutide approvals for weight management and glycemic control",
        "date": "2025-11-19",
        "company_slug": "innovent",
        "program": "Mazdutide",
        "category": "Company update",
        "indication": "Obesity; T2D",
        "url": "https://en.innoventbio.com/InvestorsAndMedia/PressReleaseDetail?key=573",
        "summary": "Innovent described mazdutide as approved by China's NMPA for weight management and glycemic control in 2025.",
    },
    {
        "id": "sciwind-ecnoglutide-obesity",
        "title": "Sciwind announces ecnoglutide NMPA approval for chronic weight management",
        "date": "2026-03-06",
        "company_slug": "sciwind-pfizer",
        "program": "Ecnoglutide",
        "category": "Regulatory decision",
        "indication": "Obesity/overweight",
        "url": "https://www.prnewswire.com/apac/news-releases/sciwind-biosciences-announces-ecnoglutide-injection-approved-by-chinas-national-medical-products-administration-nmpa-for-chronic-weight-management-302706448.html",
        "summary": "Sciwind announced China NMPA approval of ecnoglutide injection for chronic weight management.",
    },
    {
        "id": "nmpa-efsubaglutide",
        "title": "NMPA reports efsubaglutide alfa approval",
        "date": "2025-06-11",
        "company_slug": "innogen",
        "program": "Efsubaglutide alfa",
        "category": "Regulatory decision",
        "indication": "T2D",
        "url": "https://english.nmpa.gov.cn/2025-06/11/c_1101509.htm",
        "summary": "China NMPA English-language update covering approval details for efsubaglutide alfa.",
    },
    {
        "id": "ema-kyinsu",
        "title": "EMA Kyinsu EPAR",
        "date": "2025-11-24",
        "company_slug": "novo-nordisk",
        "program": "Kyinsu / IcoSema",
        "category": "Regulatory decision",
        "indication": "T2D",
        "url": "https://www.ema.europa.eu/en/medicines/human/EPAR/kyinsu",
        "summary": "EMA public assessment entry for Kyinsu, the insulin icodec and semaglutide fixed-dose combination.",
    },
    {
        "id": "health-canada-generic-semaglutide",
        "title": "Health Canada announces generic semaglutide approval",
        "date": "2026-04-28",
        "company_slug": "novo-nordisk",
        "program": "Semaglutide monotherapy exclusion",
        "category": "Generic approval",
        "indication": "T2D / obesity",
        "url": "https://www.canada.ca/en/health-canada/news/2026/04/canada-becomes-the-first-g7-country-to-approve-a-generic-version-of-semaglutide.html",
        "summary": "Source used to exclude semaglutide monotherapy brands from the in-scope branded/non-generic treatment set.",
    },
    {
        "id": "fda-generic-liraglutide",
        "title": "FDA approves first generic once-daily GLP-1 injection",
        "date": "2024-12-23",
        "company_slug": "novo-nordisk",
        "program": "Liraglutide monotherapy exclusion",
        "category": "Generic approval",
        "indication": "T2D",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-approves-first-generic-once-daily-glp-1-injection-lower-blood-sugar-patients-type-2-diabetes",
        "summary": "Source used to exclude liraglutide monotherapy brands while retaining active branded fixed-dose combinations.",
    },
]


EXCLUSIONS = [
    ("Semaglutide monotherapies", "Ozempic, Rybelsus, Wegovy, oral Wegovy", "Excluded because generic semaglutide versions are approved/launched in Canada and India, even though U.S. brands remain active."),
    ("Exenatide", "Byetta, Bydureon BCise", "Excluded because generic exenatide exists and Byetta was discontinued in the U.S."),
    ("Liraglutide monotherapies", "Victoza, Saxenda", "Excluded because generic liraglutide versions exist; active branded fixed-dose IDegLira is separately retained."),
    ("Lixisenatide standalone", "Adlyxin, Lyxumia", "Excluded because standalone product is withdrawn/discontinued in key markets; active branded FDC iGlarLixi is retained."),
    ("Albiglutide", "Tanzeum, Eperzan", "Excluded because the product was discontinued/withdrawn."),
    ("Danuglipron", "", "Excluded because Pfizer discontinued the program."),
    ("Lotiglipron", "", "Excluded because Pfizer discontinued the program."),
    ("Cotadutide", "", "Excluded because AstraZeneca terminated/dropped the program."),
]


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def dump_json(path: str, data: object) -> None:
    write(path, json.dumps(data, indent=2) + "\n")


def dump_yaml(path: str, data: object) -> None:
    write(path, yaml.safe_dump(data, sort_keys=False, allow_unicode=False))


def company_map() -> dict[str, dict]:
    return {company["slug"]: company for company in COMPANIES}


def build_treatments() -> list[dict]:
    companies = company_map()
    rows = []
    for index, row in enumerate(TREATMENTS, start=1):
        slug, name, brand, company_slug, mechanism, status, route, jurisdiction, indications, rationale = row
        company = companies[company_slug]
        treatment = {
            "id": slug,
            "slug": slug,
            "row_id": f"treatment-{index:03d}",
            "name": name,
            "title": name,
            "brand": brand,
            "company": company["name"],
            "company_slug": company_slug,
            "program": brand or name,
            "program_slug": slugify(brand or name),
            "mechanism": mechanism,
            "status": status,
            "route": route,
            "jurisdiction": jurisdiction,
            "indication": indications,
            "indications": [part.strip() for part in indications.split(";")],
            "inclusion_rationale": rationale,
            "url": f"/programs/{slug}/",
            "year": "2026" if "2026" in status else "",
            "primary_color": company["primary"],
            "secondary_color": company["secondary"],
            "accent_color": company["accent"],
            "background_image": f"/assets/img/company-backgrounds/{company_slug}.svg",
        }
        rows.append(treatment)
    return rows


def build_profiles(treatments: list[dict]) -> list[dict]:
    counts = Counter(t["company_slug"] for t in treatments)
    programs = defaultdict(list)
    for treatment in treatments:
        programs[treatment["company_slug"]].append(treatment["brand"] or treatment["name"])
    out = []
    for company in COMPANIES:
        logo_meta = LOGO_ASSETS.get(company["slug"], {
            "logo": f"/assets/img/company-logos/fallback-{company['slug']}.svg",
        })
        row = {
            **company,
            "palette_note": "Palette approximated from public corporate branding and official web presence for sponsor-specific styling.",
            "background_source": "Locally generated abstract metabolic-science SVG using the company palette; no clinical claims embedded.",
            "background_image": f"/assets/img/company-backgrounds/{company['slug']}.svg",
            "treatment_count": counts[company["slug"]],
            "document_count": len([s for s in SOURCES if s["company_slug"] == company["slug"]]),
            "programs": sorted(programs[company["slug"]]),
            "page_url": f"/companies/{company['slug']}/",
            "css_class": f"company-{company['slug']}",
            **logo_meta,
        }
        out.append(row)
    return out


def build_programs(treatments: list[dict]) -> list[dict]:
    return [
        {
            "slug": treatment["slug"],
            "company": treatment["company"],
            "company_slug": treatment["company_slug"],
            "program": treatment["brand"] or treatment["name"],
            "program_slug": treatment["program_slug"],
            "url": treatment["url"],
            "description": f"{treatment['name']} is tracked as {treatment['status'].lower()} in the {treatment['mechanism'].lower()} class.",
            "document_count": len([s for s in SOURCES if s["company_slug"] == treatment["company_slug"] and treatment["name"].split(" / ")[0].lower() in s["program"].lower()]),
            "status": treatment["status"],
            "mechanism": treatment["mechanism"],
            "route": treatment["route"],
            "indication": treatment["indication"],
            "primary_color": treatment["primary_color"],
            "secondary_color": treatment["secondary_color"],
            "accent_color": treatment["accent_color"],
            "background_image": treatment["background_image"],
        }
        for treatment in treatments
    ]


def build_documents() -> list[dict]:
    profiles = company_map()
    docs = []
    for source in SOURCES:
        if source["category"] not in {"Presentation/Poster", "Published Manuscript"}:
            continue
        profile = profiles[source["company_slug"]]
        docs.append({
            "id": source["id"],
            "row_id": source["id"],
            "title": source["title"],
            "url": source["url"],
            "company": profile["name"],
            "company_slug": source["company_slug"],
            "company_folder": profile["folder"],
            "program": source["program"],
            "program_slug": slugify(source["program"]),
            "indication": source["indication"],
            "document_type": source["category"],
            "category": source["category"],
            "year": source["date"][:4],
            "conference": "",
            "source_url": source["url"],
            "source_page": source["url"],
            "status": "external_source",
            "summary": source["summary"],
            "primary_color": profile["primary"],
            "secondary_color": profile["secondary"],
            "accent_color": profile["accent"],
        })
    return docs


def write_svg_assets(profiles: list[dict]) -> None:
    write("assets/img/site-icon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#06254a"/><path d="M17 42c12-25 18-25 30 0" fill="none" stroke="#22b3cd" stroke-width="6" stroke-linecap="round"/><circle cx="24" cy="26" r="4" fill="#ea18a8"/><circle cx="40" cy="26" r="4" fill="#76a6eb"/></svg>
""")
    for profile in profiles:
        if f"/fallback-{profile['slug']}.svg" in profile.get("logo", ""):
            initials = profile["code"][:5]
            logo = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 96" role="img" aria-label="{profile['name']} logo approximation"><rect width="320" height="96" fill="white"/><rect x="0" y="0" width="10" height="96" fill="{profile['primary']}"/><text x="28" y="43" font-family="Inter, Arial, sans-serif" font-size="26" font-weight="700" fill="{profile['primary']}">{initials}</text><text x="28" y="69" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="500" fill="{profile['secondary']}">{profile['short_name']}</text><circle cx="280" cy="48" r="20" fill="{profile['accent']}" opacity="0.82"/><circle cx="294" cy="48" r="13" fill="{profile['secondary']}" opacity="0.62"/></svg>
"""
            write(f"assets/img/company-logos/fallback-{profile['slug']}.svg", logo)
        bg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" preserveAspectRatio="none"><rect width="1200" height="520" fill="#ffffff"/><path d="M0 390 C190 260 310 470 520 300 C730 130 830 270 1200 120 L1200 520 L0 520 Z" fill="{profile['primary']}" opacity="0.10"/><path d="M80 430 C260 320 420 420 590 260 C760 100 900 210 1120 80" fill="none" stroke="{profile['secondary']}" stroke-width="4" opacity="0.35"/><g opacity="0.55" fill="{profile['accent']}"><circle cx="180" cy="170" r="16"/><circle cx="360" cy="245" r="9"/><circle cx="720" cy="130" r="13"/><circle cx="980" cy="250" r="10"/></g></svg>
"""
        write(f"assets/img/company-backgrounds/{profile['slug']}.svg", bg)


def front_matter(**kwargs: str) -> str:
    return "---\n" + yaml.safe_dump(kwargs, sort_keys=False, allow_unicode=False) + "---\n\n"


def write_company_pages(profiles: list[dict]) -> None:
    valid_slugs = {profile["slug"] for profile in profiles}
    company_dir = ROOT / "companies"
    if company_dir.exists():
        for stale_page in company_dir.glob("*.md"):
            if stale_page.stem not in valid_slugs and "layout: company" in stale_page.read_text(encoding="utf-8"):
                stale_page.unlink()
    for profile in profiles:
        write(
            f"companies/{profile['slug']}.md",
            front_matter(
                layout="company",
                title=profile["name"],
                permalink=f"/companies/{profile['slug']}/",
                company_slug=profile["slug"],
                description=profile["description"],
            ),
        )


def write_program_pages(treatments: list[dict]) -> None:
    sources_by_company = defaultdict(list)
    for source in SOURCES:
        sources_by_company[source["company_slug"]].append(source)
    for treatment in treatments:
        source_rows = sources_by_company[treatment["company_slug"]][:5]
        source_md = "\n".join(
            f"    <li><a href=\"{s['url']}\" rel=\"noopener\">{s['title']}</a> <span class=\"topic-card-meta\">{s['category']}, {s['date']}</span><br>{s['summary']}</li>"
            for s in source_rows
        ) or "    <li>Source rows pending automation discovery.</li>"
        content = front_matter(
            layout="default",
            title=treatment["brand"] or treatment["name"],
            permalink=f"/programs/{treatment['slug']}/",
            company_slug=treatment["company_slug"],
            description=f"{treatment['name']} GLP-1 treatment profile.",
        )
        content += f"""<section class="company-hero">
  <div class="company-hero-content">
    <div class="brand-chip-row">
      <span class="brand-chip">{treatment['status']}</span>
      <span class="brand-chip-sponsor">{treatment['mechanism']}</span>
    </div>
    <h1>{treatment['brand'] or treatment['name']}</h1>
    <p class="lead">{treatment['name']} is tracked as {treatment['status'].lower()} for {treatment['indication']}.</p>
  </div>
</section>

<section class="summary-grid" aria-label="Treatment summary">
  <div><strong>Company</strong><span>{treatment['company']}</span></div>
  <div><strong>Route</strong><span>{treatment['route']}</span></div>
  <div><strong>Jurisdiction</strong><span>{treatment['jurisdiction']}</span></div>
  <div><strong>Status</strong><span>{treatment['status']}</span></div>
</section>

<section>
  <h2>Inclusion rationale</h2>
  <p class="lead">{treatment['inclusion_rationale']}</p>
</section>

<section>
  <h2>Source trail</h2>
  <ul>
{source_md}
  </ul>
</section>
"""
        write(f"programs/{treatment['slug']}.md", content)


def write_indication_pages(treatments: list[dict]) -> None:
    indications = {
        "obesity": ("Obesity and Weight Management", "Obesity|overweight|weight"),
        "t2d": ("Type 2 Diabetes", "T2D|diabetes|glycemic"),
        "mash": ("MASH", "MASH"),
        "osa": ("Obstructive Sleep Apnea", "OSA|sleep apnea"),
        "cv-kidney": ("Cardiovascular and Kidney Risk", "CV|cardiovascular|CKD|kidney"),
    }
    for slug, (title, pattern) in indications.items():
        regex = re.compile(pattern, re.I)
        matches = [t for t in treatments if regex.search(t["indication"])]
        rows = "\n".join(f"- [{t['brand'] or t['name']}]({t['url']}) - {t['company']}; {t['status']}; {t['mechanism']}" for t in matches)
        write(
            f"indications/{slug}.md",
            front_matter(layout="default", title=title, permalink=f"/indications/{slug}/", description=f"GLP-1 treatments tracked for {title}.")
            + f"""<section class="hero">
  <h1>{title}</h1>
  <p class="lead">In-scope branded and investigational GLP-1-containing treatments with source-backed status tracking.</p>
</section>

<section>
  <h2>Treatments</h2>
  <ul>
{rows or '- No matching treatment rows yet.'}
  </ul>
</section>
""",
        )


def write_topic_pages(treatments: list[dict]) -> None:
    mechanisms = defaultdict(list)
    for treatment in treatments:
        mechanisms[treatment["mechanism"]].append(treatment)
    content = front_matter(layout="default", title="Mechanism Map", permalink="/topics/mechanism-map/", description="Mechanism-level map of GLP-1-containing treatments.")
    content += """<section class="hero">
  <h1>Mechanism Map</h1>
  <p class="lead">The GLP-1 landscape now spans mono-agonists, oral small molecules, dual incretins, GLP-1/glucagon duals, triple agonists, amylin combinations, and insulin fixed-dose combinations.</p>
</section>
"""
    for mechanism, rows in sorted(mechanisms.items()):
        items = "\n".join(f"    <li><a href=\"{t['url']}\">{t['brand'] or t['name']}</a> <span class=\"topic-card-meta\">{t['company']} / {t['status']}</span></li>" for t in sorted(rows, key=lambda x: x["name"]))
        content += f"""<section>
  <h2>{mechanism}</h2>
  <ul class="document-list">
{items}
  </ul>
</section>
"""
    write("topics/mechanism-map.md", content)


def write_index_pages(treatments: list[dict], profiles: list[dict], programs: list[dict]) -> None:
    approved = len([t for t in treatments if "Approved" in t["status"]])
    investigational = len(treatments) - approved
    mechanisms = len({t["mechanism"] for t in treatments})
    write(
        "index.md",
        front_matter(layout="default", title="GLP-1 Data Archive", description="Open index of branded and investigational GLP-1-containing treatments.")
        + f"""{{% assign treatment_count = site.data.treatments | size %}}
{{% assign company_count = site.data.company_profiles | size %}}
{{% assign news_count = site.data.company_press_releases | size %}}

<section class="hero">
  <h1>Branded and investigational GLP-1 treatment landscape</h1>
  <p class="lead">A GitHub Pages archive of in-scope GLP-1-containing treatments from the supplied research file, excluding discontinued products and monotherapy families with generic versions. The site keeps sponsor-specific styling, source trails, and automation-ready press/publication monitoring in the same structural pattern as the reference archive.</p>
</section>

<section class="summary-grid" aria-label="Archive summary">
  <div><strong>Treatments</strong><span>{{{{ treatment_count }}}}</span></div>
  <div><strong>Approved branded</strong><span>{approved}</span></div>
  <div><strong>Investigational</strong><span>{investigational}</span></div>
  <div><strong>Mechanisms</strong><span>{mechanisms}</span></div>
  <div><strong>Companies</strong><span>{{{{ company_count }}}}</span></div>
  <div><strong>News rows</strong><span>{{{{ news_count }}}}</span></div>
</section>

<section>
  <h2>Browse</h2>
  <ul class="document-list">
    <li><a class="topic-card-link" href="{{{{ '/treatments/' | relative_url }}}}"><span class="topic-card-title">Treatments</span><span class="topic-card-description">Complete in-scope treatment list with status, route, jurisdiction, mechanism, and inclusion rationale.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/companies/' | relative_url }}}}"><span class="topic-card-title">Companies</span><span class="topic-card-description">Sponsor landing pages styled with company-specific palettes and program lists.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/programs/' | relative_url }}}}"><span class="topic-card-title">Programs</span><span class="topic-card-description">Product and pipeline entry points for each branded or investigational treatment.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/news/' | relative_url }}}}"><span class="topic-card-title">News</span><span class="topic-card-description">Regulatory decisions, filings, clinical data, company updates, and generic approvals separated from the document library.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/documents/' | relative_url }}}}"><span class="topic-card-title">Documents</span><span class="topic-card-description">Parsed publications, posters, and presentations with source pages and infographics.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/infographics/' | relative_url }}}}"><span class="topic-card-title">Infographics</span><span class="topic-card-description">Chart-first summaries generated from parsed congress, poster, presentation, and manuscript source documents.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/topics/' | relative_url }}}}"><span class="topic-card-title">Topics</span><span class="topic-card-description">Mechanism map, exclusions, and evidence notes.</span></a></li>
    <li><a class="topic-card-link" href="{{{{ '/automation-audit/' | relative_url }}}}"><span class="topic-card-title">Automation Audit</span><span class="topic-card-description">Expected source rosters and run-level coverage for press and publication sweeps.</span></a></li>
  </ul>
</section>

<section>
  <h2>Featured mechanisms</h2>
  {{% assign featured_programs = site.data.company_programs | sort: "mechanism" %}}
  <ul class="document-list">
    {{% for program in featured_programs limit:12 %}}
      <li data-company-color="true" style="--card-primary: {{{{ program.primary_color }}}}; --card-secondary: {{{{ program.secondary_color }}}}; --card-accent: {{{{ program.accent_color }}}};">
        <a class="topic-card-link" href="{{{{ program.url | relative_url }}}}">
          <span class="topic-card-title">{{{{ program.program }}}}</span>
          <span class="topic-card-meta">{{{{ program.company }}}} / {{{{ program.status }}}}</span>
          <span class="topic-card-description">{{{{ program.mechanism }}}}</span>
        </a>
      </li>
    {{% endfor %}}
  </ul>
</section>
""",
    )
    write("treatments.md", front_matter(layout="default", title="Treatments", permalink="/treatments/", description="Complete GLP-1 treatment index.") + """<section class="hero">
  <h1>Treatments</h1>
  <p class="lead">Complete in-scope list of branded approved and investigational GLP-1-containing treatments from the supplied research file. Discontinued products and monotherapy families with generic versions are excluded.</p>
</section>

{% include treatment_list.html treatments=site.data.treatments sort_by="name" sort_dir="asc" %}
""")
    write("documents.md", front_matter(layout="default", title="Documents", permalink="/documents/", description="External source document index for the GLP-1 archive.") + """{% assign presentation_documents = site.data.company_documents | where: "document_type", "Presentation/Poster" %}
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
""")
    write("news.md", front_matter(layout="default", title="News", permalink="/news/", description="Non-document GLP-1 source rows, including regulatory decisions, filings, clinical data, company updates, and generic approvals.") + """{% assign regulatory_decisions = site.data.company_press_releases | where: "category", "Regulatory decision" %}
{% assign regulatory_filings = site.data.company_press_releases | where: "category", "Regulatory filing" %}
{% assign clinical_data = site.data.company_press_releases | where: "category", "Clinical data" %}
{% assign company_updates = site.data.company_press_releases | where: "category", "Company update" %}
{% assign generic_approvals = site.data.company_press_releases | where: "category", "Generic approval" %}
{% assign news_count = site.data.company_press_releases | size %}

<section class="hero">
  <h1>News</h1>
  <p class="lead">Non-document source rows used by the archive, separated from publications, posters, and presentations. Sort by type to distinguish regulatory decisions, filings, clinical data, company updates, and generic approvals.</p>
</section>

<section class="summary-grid" aria-label="News source summary">
  <div><strong>News rows</strong><span>{{ news_count }}</span></div>
  <div><strong>Regulatory decisions</strong><span>{{ regulatory_decisions | size }}</span></div>
  <div><strong>Regulatory filings</strong><span>{{ regulatory_filings | size }}</span></div>
  <div><strong>Clinical data</strong><span>{{ clinical_data | size }}</span></div>
  <div><strong>Company updates</strong><span>{{ company_updates | size }}</span></div>
  <div><strong>Generic approvals</strong><span>{{ generic_approvals | size }}</span></div>
</section>

{% include press_release_list.html releases=site.data.company_press_releases sort_by="date" sort_dir="desc" %}
""")
    write("companies.md", front_matter(layout="default", title="Companies", permalink="/companies/", description="Company-level entry points for the GLP-1 archive.") + """<section class="hero">
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
""")
    write("programs.md", front_matter(layout="default", title="Programs", permalink="/programs/", description="Product and pipeline entry points for GLP-1 treatment records.") + """<section class="hero">
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
""")
    write("indications.md", front_matter(layout="default", title="Indications", permalink="/indications/", description="Indication entry points for GLP-1 treatments.") + """<section class="hero">
  <h1>Indications</h1>
  <p class="lead">Disease and use-case entry points across in-scope GLP-1-containing therapies.</p>
</section>

<section>
  <h2>Browse by indication</h2>
  <ul class="document-list">
    <li><a class="topic-card-link" href="{{ '/indications/obesity/' | relative_url }}"><span class="topic-card-title">Obesity and Weight Management</span><span class="topic-card-description">Approved and investigational therapies for obesity, overweight, and chronic weight management.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/indications/t2d/' | relative_url }}"><span class="topic-card-title">Type 2 Diabetes</span><span class="topic-card-description">GLP-1-containing products and combinations for glycemic control.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/indications/mash/' | relative_url }}"><span class="topic-card-title">MASH</span><span class="topic-card-description">Metabolic dysfunction-associated steatohepatitis programs.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/indications/osa/' | relative_url }}"><span class="topic-card-title">Obstructive Sleep Apnea</span><span class="topic-card-description">Obesity-associated OSA label expansions and trials.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/indications/cv-kidney/' | relative_url }}"><span class="topic-card-title">Cardiovascular and Kidney Risk</span><span class="topic-card-description">Cardiometabolic outcomes and organ-protection programs.</span></a></li>
  </ul>
</section>
""")
    write("topics.md", front_matter(layout="default", title="Topic Pages", permalink="/topics/", description="Topic syntheses for the GLP-1 archive.") + """<section class="hero">
  <h1>Topic Pages</h1>
  <p class="lead">Cross-treatment views for mechanism classes, excluded products, and monitoring scope.</p>
</section>

<section>
  <h2>Topics</h2>
  <ul class="document-list">
    <li><a class="topic-card-link" href="{{ '/topics/mechanism-map/' | relative_url }}"><span class="topic-card-title">Mechanism Map</span><span class="topic-card-description">Treatment classes from mono-agonists through triple agonists and fixed-dose combinations.</span></a></li>
    <li><a class="topic-card-link" href="{{ '/topics/exclusions/' | relative_url }}"><span class="topic-card-title">Exclusions</span><span class="topic-card-description">Discontinued and generic-exposed products excluded from the focused archive.</span></a></li>
  </ul>
</section>
""")


def write_exclusions_page() -> None:
    rows = "\n".join(f"| {name} | {brands} | {why} |" for name, brands, why in EXCLUSIONS)
    write("topics/exclusions.md", front_matter(layout="default", title="Exclusions", permalink="/topics/exclusions/", description="GLP-1 treatments excluded from the focused archive.") + f"""<section class="hero">
  <h1>Exclusions</h1>
  <p class="lead">Products excluded from this focused archive because they are discontinued, withdrawn, or have generic versions at the molecule/product-family level.</p>
</section>

| Treatment | Brand(s) / code(s) | Rationale |
|---|---|---|
{rows}
""")


def write_methodology_and_ops() -> None:
    write("methodology.md", front_matter(layout="default", title="Methodology", permalink="/methodology/", description="Scope and source methodology for the GLP-1 archive.") + """<section class="hero">
  <h1>Methodology</h1>
  <p class="lead">The archive starts from the supplied GLP-1 research attachment and keeps only active branded or investigational GLP-1-containing treatments.</p>
</section>

## Inclusion rules

- Include branded approved products if the product family is not discontinued and does not have a generic monotherapy version in the seed/source scope.
- Include investigational treatments unless the program is explicitly discontinued.
- Retain active branded fixed-dose combinations even when one component has generic exposure, and flag that edge case in the rationale.
- Exclude discontinued, withdrawn, or generic-exposed monotherapy products.

## Source priority

Primary source preference is regulator pages, sponsor press releases, trial registries, peer-reviewed publications, and sponsor science portals. Automation scripts record candidates in a worklist before adding rows to the rendered archive.
""")
    write("automation-audit.md", front_matter(layout="default", title="Automation audit dashboard", permalink="/automation-audit/", description="Run-level audit dashboard for GLP-1 publication and press release automation.") + """{% assign audit = site.data.automation_audit %}
{% assign summary = audit.summary %}
{% assign latest_run = audit.runs | first %}

<section class="hero">
  <p class="eyebrow">Operations audit</p>
  <h1>Automation Audit</h1>
  <p class="lead">This dashboard tracks expected source rosters, source-level terminal status, press release rows, publication/congress candidates, deferred review items, and run outcomes. Generated {{ audit.generated_at_utc }}.</p>
</section>

<section class="summary-grid audit-summary-grid" aria-label="Automation audit summary">
  <div><strong>Companies</strong><span>{{ summary.in_scope_companies }}</span></div>
  <div><strong>Expected Sources</strong><span>{{ summary.expected_sources }}</span></div>
  <div><strong>Publication Sources</strong><span>{{ summary.publication_expected_sources }}</span></div>
  <div><strong>Press Sources</strong><span>{{ summary.press_release_expected_sources }}</span></div>
  <div><strong>Latest Coverage</strong><span>{{ summary.latest_checked_sources }} / {{ summary.latest_expected_sources }}</span></div>
  <div><strong>Latest Status</strong><span>{{ summary.latest_run_status_label | default: summary.latest_run_status }}</span></div>
  <div><strong>Open Findings</strong><span>{{ summary.open_findings }}</span></div>
</section>

<section>
  <h2>Expected Source Roster</h2>
  <p class="lead">Every active row for the relevant automation type should appear in each run's terminal source-status ledger.</p>
  <table class="audit-table audit-wide-table">
    <thead><tr><th>Type</th><th>Company</th><th>Tier</th><th>Fetcher</th><th>Source</th><th>Mode</th></tr></thead>
    <tbody>
      {% for source in audit.expected_sources %}
        <tr>
          <td>{{ source.source_family_label | default: source.source_family }}</td>
          <td>{{ source.company_name }}</td>
          <td>{{ source.tier }}</td>
          <td>{{ source.fetcher_label | default: source.fetcher }}</td>
          <td>{% if source.source_url %}<a href="{{ source.source_url }}" rel="noopener">{{ source.source_url }}</a>{% elsif source.pubmed_terms %}<code>{{ source.pubmed_terms | join: " OR " }}</code>{% else %}<span>{{ source.skip_reason | default: "(not configured)" }}</span>{% endif %}</td>
          <td>{% if source.discovery_only %}<span class="status-pill status-warning">Manual Review</span>{% else %}<span class="status-pill status-ok">Automated</span>{% endif %}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</section>

<section>
  <h2>Automation Runs</h2>
  {% if audit.runs.size == 0 %}
    <p class="lead">No automation run records found.</p>
  {% else %}
    <table class="audit-table audit-wide-table">
      <thead><tr><th>Run</th><th>Type</th><th>Status</th><th>Started</th><th>Coverage</th><th>Worklist</th><th>Errors</th></tr></thead>
      <tbody>
        {% for run in audit.runs limit:25 %}
          <tr><td><code>{{ run.run_id }}</code></td><td>{{ run.run_type_label | default: run.run_type }}</td><td><span class="status-pill status-{{ run.status }}">{{ run.status_label | default: run.status }}</span></td><td><code>{{ run.started_at }}</code></td><td>{{ run.checked_sources_count }} / {{ run.expected_sources_count }}</td><td>{{ run.worklist_items_count }}</td><td>{{ run.error_sources_count }}</td></tr>
        {% endfor %}
      </tbody>
    </table>
  {% endif %}
</section>
""")
    write("README.md", "# GLP-1 Data Archive\n\nGitHub Pages archive of branded and investigational GLP-1-containing treatments, generated from the supplied research file and source-backed public updates.\n\nRun `python scripts/generate_glp1_site.py` after changing the treatment seed data.\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://justinsyu.github.io/glp-1-data/sitemap.xml\n")
    write("sitemap.xml", """---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{% for page in site.pages %}
  {% unless page.sitemap == false %}
  <url><loc>{{ site.url }}{{ site.baseurl }}{{ page.url }}</loc></url>
  {% endunless %}
{% endfor %}
</urlset>
""")


def write_config() -> None:
    write("_config.yml", """title: GLP-1 Data Archive
description: Public archive of branded and investigational GLP-1-containing treatments, sponsor updates, and publication/congress source monitoring.
url: "https://justinsyu.github.io"
baseurl: "/glp-1-data"
lang: en-US
timezone: America/New_York
maintainer: Justin Yu
repository_url: "https://github.com/justinsyu/glp-1-data"

markdown: kramdown
theme: null

plugins:
  - jekyll-seo-tag

defaults:
  - scope:
      path: ""
    values:
      last_modified_at: 2026-06-05

exclude:
  - scripts/
  - vendor/
  - vendor/bundle/
  - Gemfile
  - Gemfile.lock
  - .DS_Store
  - README.md
  - instructions-for-setup.md
  - tmp/
  - .playwright-mcp/
""")


def write_automation_sources(profiles: list[dict]) -> None:
    important = {
        "eli-lilly": ["orforglipron", "Foundayo", "tirzepatide", "Zepbound", "Mounjaro", "retatrutide", "GLP-1"],
        "novo-nordisk": ["CagriSema", "amycretin", "zenagamtide", "Xultophy", "Kyinsu", "IcoSema", "GLP-1"],
        "amgen": ["MariTide", "maridebart", "AMG 133", "GLP-1"],
        "innovent": ["mazdutide", "IBI362", "GLP-1", "glucagon"],
        "sciwind-pfizer": ["ecnoglutide", "XW003", "GLP-1"],
        "hengrui": ["noiiglutide", "SHR20004", "GLP-1"],
        "kailera": ["ribupatide", "HRS9531", "KAI-9531", "GLP-1"],
        "boehringer-zealand": ["survodutide", "BI 456906", "GLP-1", "MASH"],
        "viking-therapeutics": ["VK2735", "GLP-1", "GIP"],
        "altimmune": ["pemvidutide", "GLP-1", "MASH"],
    }
    press_urls = {
        "eli-lilly": "https://investor.lilly.com/",
        "novo-nordisk": "https://www.novonordisk.com/news-and-media/news-and-ir-materials.html",
        "sanofi": "https://www.sanofi.com/en/media-room/press-releases",
        "amgen": "https://www.amgen.com/newsroom/press-releases",
        "innovent": "https://en.innoventbio.com/InvestorsAndMedia/PressRelease",
        "sciwind-pfizer": "https://www.sciwindbio.com/news.html",
        "gan-and-lee": "https://www.ganlee.com/news.html",
        "hengrui": "https://www.hengrui.com/en/media.html",
        "kailera": "https://www.kailera.com/",
        "hanmi": "https://www.hanmipharm.com/ehanmi/handler/Rnd-Pipeline",
        "viking-therapeutics": "https://ir.vikingtherapeutics.com/news-releases",
        "altimmune": "https://ir.altimmune.com/news-releases",
        "merck-hanmi": "https://www.merck.com/news/",
        "roche-carmot": "https://www.roche.com/media/releases",
    }
    press_companies = []
    publication_companies = []
    for profile in profiles:
        terms = important.get(profile["slug"], ["GLP-1", profile["short_name"]])
        regex = "(?i)" + "|".join(re.escape(term) for term in terms)
        press_companies.append({
            "id": profile["folder"],
            "company_slug": profile["slug"],
            "name": profile["name"],
            "tier": 1 if profile["slug"] in important else 2,
            "sources": [{
                "source_id": f"{profile['slug']}-primary-news",
                "url": press_urls.get(profile["slug"], profile["brand_site"]),
                "fetcher": "requests",
                "title_filter": regex,
            }],
        })
        publication_companies.append({
            "id": profile["folder"],
            "company_slug": profile["slug"],
            "name": profile["name"],
            "tier": 1 if profile["slug"] in important else 2,
            "sources": [
                {
                    "kind": "pubmed",
                    "terms": terms[:4],
                    "fetcher": "pubmed",
                    "discovery_only": True,
                    "title_filter": regex,
                },
                {
                    "kind": "html",
                    "url": profile["brand_site"],
                    "fetcher": "requests",
                    "discovery_only": True,
                    "title_filter": regex,
                },
            ],
        })
    dump_yaml("scripts/press_release_sources.yml", {"companies": press_companies})
    dump_yaml("scripts/publication_sources.yml", {"companies": publication_companies})


def write_initial_audit(profiles: list[dict]) -> None:
    expected = []
    for family, path in [("press_release", "scripts/press_release_sources.yml"), ("publication", "scripts/publication_sources.yml")]:
        raw = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
        for company in raw["companies"]:
            for index, source in enumerate(company["sources"], start=1):
                expected.append({
                    "source_key": f"{family}:{company['id']}:{index}",
                    "source_family": family,
                    "source_family_label": "Press Release" if family == "press_release" else "Publication",
                    "run_type": family,
                    "company_id": company["id"],
                    "company_slug": company["company_slug"],
                    "company_name": company["name"],
                    "tier": company["tier"],
                    "source_index": index,
                    "source_kind": source.get("kind", "press_release_index"),
                    "source_url": source.get("url", ""),
                    "pubmed_terms": source.get("terms", []),
                    "fetcher": source.get("fetcher", "requests"),
                    "fetcher_label": source.get("fetcher", "requests").replace("_", " ").title(),
                    "discovery_only": bool(source.get("discovery_only", False)),
                    "status": "pending",
                })
    active = expected
    audit = {
        "generated_at_utc": "2026-06-05T00:00:00+00:00",
        "summary": {
            "in_scope_companies": len({r["company_id"] for r in expected}),
            "publication_expected_sources": len([r for r in active if r["source_family"] == "publication"]),
            "press_release_expected_sources": len([r for r in active if r["source_family"] == "press_release"]),
            "expected_sources": len(active),
            "configured_skips": 0,
            "automation_runs": 0,
            "latest_run_id": "",
            "latest_run_status": "not_run",
            "latest_run_status_label": "Not Run",
            "latest_run_started_at": "",
            "latest_checked_sources": 0,
            "latest_expected_sources": len(active),
            "latest_downloaded_documents": 0,
            "latest_worklist_items": 0,
            "latest_error_sources": 0,
            "open_findings": 0,
        },
        "expected_sources": expected,
        "runs": [],
        "recent_sweep_runs": [],
        "findings": [],
    }
    dump_json("_data/automation_audit.json", audit)


def main() -> None:
    treatments = build_treatments()
    profiles = build_profiles(treatments)
    programs = build_programs(treatments)
    documents = build_documents()
    press_rows = [
        {
            "title": source["title"],
            "date": source["date"],
            "company": company_map()[source["company_slug"]]["short_name"],
            "company_slug": source["company_slug"],
            "program": source["program"],
            "indication": source["indication"],
            "category": source["category"],
            "summary": source["summary"],
            "source_url": source["url"],
        }
        for source in SOURCES
    ]
    write_config()
    dump_json("_data/treatments.json", treatments)
    dump_json("_data/company_profiles.json", profiles)
    dump_json("_data/company_programs.json", programs)
    dump_json("_data/company_documents.json", documents)
    dump_yaml("_data/company_press_releases.yml", press_rows)
    dump_yaml("_data/documents.yml", [])
    dump_yaml("_data/pdf_links.yml", [])
    write_svg_assets(profiles)
    write_company_pages(profiles)
    write_program_pages(treatments)
    write_indication_pages(treatments)
    write_topic_pages(treatments)
    write_exclusions_page()
    write_index_pages(treatments, profiles, programs)
    write_methodology_and_ops()
    write_automation_sources(profiles)
    write_initial_audit(profiles)


if __name__ == "__main__":
    main()
