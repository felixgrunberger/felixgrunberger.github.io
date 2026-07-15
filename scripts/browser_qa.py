#!/usr/bin/env python3
"""Responsive browser checks for a rendered Quarto site.

The page is self-contained in memory before it is opened. This avoids local-server,
file-URL and corporate-browser restrictions while still testing the rendered HTML,
CSS and JavaScript.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "docs").resolve()
VIEWPORTS = {
    "wide": {"width": 1536, "height": 960},
    "desktop": {"width": 1280, "height": 900},
    "tablet": {"width": 1024, "height": 1366},
    "mobile": {"width": 390, "height": 844},
    "small-mobile": {"width": 360, "height": 800},
}


def local_path(url: str, base: Path) -> Path | None:
    if not url or url.startswith(("data:", "http://", "https://", "//", "mailto:", "#")):
        return None
    clean = unquote(urlsplit(url).path).lstrip("/")
    candidate = (base / clean).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def inline_page(index_file: Path) -> str:
    html = index_file.read_text(encoding="utf-8")
    base = index_file.parent

    def css_replace(match: re.Match[str]) -> str:
        href = match.group(1)
        path = local_path(href, base)
        if path and path.suffix.lower() == ".css":
            return f"<style data-inline-source='{path.name}'>\n{path.read_text(encoding='utf-8', errors='ignore')}\n</style>"
        return match.group(0)

    html = re.sub(
        r'<link\b[^>]*rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
        css_replace,
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]*>',
        css_replace,
        html,
        flags=re.I,
    )

    def script_replace(match: re.Match[str]) -> str:
        src = match.group(1)
        path = local_path(src, base)
        if path and path.suffix.lower() == ".js":
            return f"<script data-inline-source='{path.name}'>\n{path.read_text(encoding='utf-8', errors='ignore')}\n</script>"
        return match.group(0)

    html = re.sub(r'<script\b[^>]*src=["\']([^"\']+)["\'][^>]*>\s*</script>', script_replace, html, flags=re.I)

    def asset_replace(match: re.Match[str]) -> str:
        attr, quote, url = match.group(1), match.group(2), match.group(3)
        path = local_path(url, base)
        if not path or path.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            return match.group(0)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"{attr}={quote}data:{mime};base64,{payload}{quote}"

    html = re.sub(r'\b(src|poster)=(["\'])([^"\']+)\2', asset_replace, html, flags=re.I)
    return html


def main() -> None:
    index_file = ROOT / "index.html"
    if not index_file.exists():
        raise SystemExit(f"Rendered homepage not found: {index_file}")

    html = inline_page(index_file)
    errors: list[str] = []
    report: dict[str, object] = {"site": str(ROOT), "viewports": {}}
    qa_dir = ROOT.parent / "qa"
    qa_dir.mkdir(exist_ok=True)

    browser_candidates = [
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    browser_path = next((str(Path(path)) for path in browser_candidates if path and Path(path).exists()), None)

    with sync_playwright() as p:
        launch_args = {"headless": True, "args": ["--no-sandbox"]}
        if browser_path:
            launch_args["executable_path"] = browser_path
        browser = p.chromium.launch(**launch_args)
        for name, viewport in VIEWPORTS.items():
            page = browser.new_page(viewport=viewport, device_scale_factor=1)
            page.set_content(html, wait_until="load")
            page.wait_for_timeout(350)

            # Make reveal sections visible for deterministic full-page screenshots.
            page.evaluate("""() => {
              document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
              window.scrollTo(0, 0);
            }""")
            page.wait_for_timeout(120)

            # Verify that the interactive workflow responds to user input.
            page.evaluate("document.querySelector('[data-workflow-step=\"3\"]')?.click()")
            page.wait_for_timeout(80)
            interaction = page.evaluate("""() => ({
              active: document.querySelector('[data-workflow-panel]')?.dataset.activeStep || null,
              response: document.querySelector('[data-workflow-response]')?.textContent || ''
            })""")
            if interaction['active'] != '3' or 'Evaluate quality' not in interaction['response']:
                errors.append(f"{name}: workflow interaction did not update correctly")
            page.evaluate("document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0, 0)")
            page.wait_for_timeout(180)

            metrics = page.evaluate(
                """() => ({
                  innerWidth: window.innerWidth,
                  scrollWidth: document.documentElement.scrollWidth,
                  headerHeight: document.querySelector('.navbar')?.getBoundingClientRect().height || 0,
                  heroTop: document.querySelector('.hero-section')?.getBoundingClientRect().top || 0,
                  h1Size: parseFloat(getComputedStyle(document.querySelector('.hero-content h1')).fontSize),
                  workflowWidth: document.querySelector('.workflow-panel')?.getBoundingClientRect().width || 0,
                  workflowActive: document.querySelector('[data-workflow-panel]')?.dataset.activeStep || null
                })"""
            )
            overflow = metrics["scrollWidth"] - metrics["innerWidth"]
            if overflow > 1:
                errors.append(f"{name}: horizontal overflow of {overflow}px")
            if not 54 <= metrics["headerHeight"] <= 94:
                errors.append(f"{name}: unexpected header height {metrics['headerHeight']}px")
            if metrics["heroTop"] < metrics["headerHeight"] - 2:
                errors.append(f"{name}: hero overlaps pinned header")
            if metrics["workflowWidth"] > metrics["innerWidth"] - 16:
                errors.append(f"{name}: workflow panel is wider than the usable viewport")
            top_shot = qa_dir / f"{name}-top.png"
            full_shot = qa_dir / f"{name}-full.png"
            page.screenshot(path=str(top_shot), full_page=False)
            page.screenshot(path=str(full_shot), full_page=True)
            report["viewports"][name] = {
                **viewport,
                **metrics,
                "overflow": overflow,
                "topScreenshot": top_shot.name,
                "fullScreenshot": full_shot.name,
            }
            page.close()
        browser.close()

    (qa_dir / "browser-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if errors:
        raise SystemExit("Browser QA failed:\n- " + "\n- ".join(errors))
    print("Browser QA passed at 1536, 1280, 1024, 390 and 360 px widths.")


if __name__ == "__main__":
    main()
