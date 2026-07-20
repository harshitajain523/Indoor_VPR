# Auditing Indoor VPR — project page

Static project page (Bulma / Academic Project Page Template style), served by GitHub Pages.

## Structure
```
index.html                 the page (edit text + the REPLACE_… placeholders)
static/css/custom.css       styling tweaks
static/images/              figures (regenerate with make_figures.py)
make_figures.py             builds fig_fragility.png + fig_mask_examples.png from the code repo's data
```

## Fill in before publishing
Search `index.html` for `REPLACE_WITH_…` and the author placeholders (`Author Two`, `Advisor Name`,
`Institution / Lab`) and set:
- `REPLACE_WITH_CODE_REPO_URL` — the SegVLAD/MegaLoc code repo
- `REPLACE_WITH_REPORT_PDF_URL`, `REPLACE_WITH_DATA_URL`, `REPLACE_WITH_PAGE_URL`

## Preview locally
```bash
python -m http.server 8000   # then open http://localhost:8000
```

## Publish on GitHub Pages
```bash
git init && git add -A && git commit -m "Project page"
git branch -M main
git remote add origin git@github.com:<user>/<repo>.git
git push -u origin main
```
Then: repo **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/ (root)`**.
Page appears at `https://<user>.github.io/<repo>/`.

## Regenerate figures
```bash
/home/harshita/projects/wpr/.venv/bin/python make_figures.py
```
(reads maze images + `data/maze/out/maze_mask_stats.csv` from the code repo)

Numbers on the page are measured; nothing is hand-entered beyond what the code produces.
