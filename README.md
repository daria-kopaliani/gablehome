# gablehome.app

Static pSEO site for Gable (home maintenance app). Zero JS, print-friendly.

- `tasks.py` — all content (tasks, seasons, copy)
- `build.py` — generator → `docs/` (55 pages: index, 12 monthly, 4 seasonal, 36 how-often, new-homeowners, sitemap, robots, CNAME)
- Rebuild: `python3 build.py`

## Deploy (blocked on domain registration)
1. Register **gablehome.app** (available as of 2026-08-27; RDAP-checked).
2. GitHub → repo Settings → Pages → deploy from `main` /docs.
3. DNS: ALIAS/A records to GitHub Pages, CNAME file already in docs/.
4. Enforce HTTPS (required for .app TLD).
5. Add the property in GSC, submit /sitemap.xml.
6. At app launch: replace the "Coming soon to iPhone" CTA with the App Store link.
