#!/usr/bin/env python3
"""Download official/public company logo assets used by the GLP-1 archive."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "company-logos"

LOGOS = {
    "eli-lilly.svg": "https://delivery-p137454-e1438138.adobeaemcloud.com/adobe/assets/urn:aaid:aem:2843cade-80ee-42b6-b285-a1450fef6b77/renditions/original/as/LillyLogo_RGB_Red_v3.svg?assetname=LillyLogo_RGB_Red_v3.svg",
    "amgen.svg": "https://www.amgen.com/-/media/Themes/Global/Global/Global/images/migration/Common/amgen-blue.svg?la=en&hash=2F9332F2F46EA1E1EF9CCF9D40B8C7B8",
    "altimmune.png": "https://altimmune.com/wp-content/uploads/2019/11/altimmune_logo.png",
    "benemae.png": "https://www.benemae.com/bocweb/web/img/logo2.png?v=v85",
    "eccogene.png": "https://www.eccogene.com/wp-content/uploads/logo-EccoGene-dark-colored-min.png",
    "gan-and-lee.png": "https://www.ganlee.com/statics/home_en/images/logo-1.png",
    "hanmi.svg": "https://www.hanmi.co.kr/images/common/logo_gnb.svg",
    "huadong.png": "https://www.eastchinapharm.com/static/home/images/logo20210903.png",
    "innogen.png": "https://img.website.xin/sitefiles18031/18031663/%E9%93%B6%E8%AF%BALOGO-ai.png",
    "innovent.png": "https://www.innoventbio.com/static/img/logo_b1.2ba2a53.png",
    "kailera.svg": "https://www.kailera.com/wp-content/uploads/2024/09/Kailera-Logo.svg",
    "merck.svg": "https://www.merck.com/wp-content/uploads/sites/124/2025/08/site-logo.svg",
    "novo-nordisk.ico": "https://www.novonordisk.com/etc.clientlibs/nncorp/components/structure/page/clientlib/resources/favicon.ico",
    "pfizer.svg": "https://www.pfizer.com/profiles/pfecpfizercomus_profile/themes/pfecpfizercomus/public/assets/images/logo-blue.svg",
    "roche.png": "https://www.roche.com/src/resources/images/android-chrome-512x512.png?v=7f5356ff0eaba89671bed4a1828ef379",
    "sanofi.svg": "https://www.sanofi.com/icons/favicon.svg",
    "sciwind.png": "https://www.sciwindbio.com/themes/front/public/images/logo.png",
    "structure-therapeutics.png": "https://structuretx.com/wp-content/uploads/2024/11/logo.png",
    "united-labs.png": "https://www.tul.com.hk/uploads/image/img/logo.png",
    "viking.png": "https://vikingtherapeutics.com/wp-content/uploads/2025/12/viking-logo-color-v4.png",
}

BROWSER_CAPTURED_LOGOS = {
    "astrazeneca.png": "https://www.astrazeneca.com/etc/designs/az/img/logo-az.png",
    "boehringer-ingelheim.svg": "https://upload.wikimedia.org/wikipedia/commons/7/74/Boehringer_Ingelheim_Logo.svg",
    "hengrui.png": "https://www.hengrui.com/en/images/logo.png",
    "novo-nordisk-wordmark.png": "https://www.novonordisk.com/",
    "roche-wordmark.svg": "https://www.roche.com/",
    "sanofi-wordmark.svg": "https://www.sanofi.com/en",
    "zealand.svg": "https://www.zealandpharma.com/assets/favicon/favicon.svg",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 GLP1DataLogoDownloader/1.0",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}


def download(filename: str, url: str) -> None:
    target = OUT / filename
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    content = response.content
    if len(content) < 100:
        raise RuntimeError(f"{url} returned suspiciously small logo payload")
    target.write_bytes(content)
    print(f"{filename}\t{len(content)} bytes\t{urlparse(url).netloc}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failures = []
    for filename, url in LOGOS.items():
        try:
            download(filename, url)
        except Exception as exc:  # noqa: BLE001
            failures.append((filename, url, exc))
            print(f"FAILED\t{filename}\t{url}\t{exc}")
    for filename, url in BROWSER_CAPTURED_LOGOS.items():
        target = OUT / filename
        status = "present" if target.exists() and target.stat().st_size > 100 else "missing"
        print(f"BROWSER\t{filename}\t{status}\t{urlparse(url).netloc}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
