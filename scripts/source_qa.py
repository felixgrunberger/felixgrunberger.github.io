#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
required = [
    '_quarto.yml','index.qmd','expertise.qmd','work.qmd','publications.qmd','about.qmd','404.qmd',
    'styles.scss','site.js','robots.txt','.nojekyll','includes/head.html','includes/after-body.html',
    'images/favicon.svg','images/social-preview.png','images/project-longread.svg','images/project-multiomics.svg',
    'images/project-quality.svg','images/project-digital.svg','images/project-assay.svg'
]
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'Missing {rel}')
try:
    data=yaml.safe_load((ROOT/'_quarto.yml').read_text())
    if data.get('project',{}).get('type')!='website': errors.append('_quarto.yml is not a website project')
except Exception as e: errors.append(f'Invalid YAML: {e}')

for qmd in ROOT.glob('*.qmd'):
    text=qmd.read_text()
    for path in re.findall(r'(?:src|href)="([^"]+)"', text):
        if path.startswith(('http:','https:','mailto:','#')): continue
        target=(ROOT/path.split('#')[0])
        if path.endswith('.qmd'):
            target=ROOT/path.split('#')[0]
        if not target.exists(): errors.append(f'{qmd.name}: unresolved resource {path}')

scss=(ROOT/'styles.scss').read_text()
rules=scss.split('/*-- scss:rules --*/',1)[-1]
if rules.count('{') != rules.count('}'):
    errors.append('styles.scss has unbalanced braces')
if 'open to new opportunities' in (ROOT/'index.qmd').read_text().lower():
    errors.append('Explicit job-search language found')
if (ROOT/'publications.qmd').read_text().count('https://doi.org/') < 17:
    errors.append('Fewer than 17 DOI links')

if errors:
    raise SystemExit('Source QA failed:\n- '+'\n- '.join(errors))
print('Source QA passed.')
