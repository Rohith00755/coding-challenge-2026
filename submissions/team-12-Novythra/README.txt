AdProof AI — Dataset Website
=================================

This website is built around the uploaded Srishti-2K26 dataset:
- 60 fictional search ads in ads.csv
- 60 paired HTML landing-page snapshots
- Industries: financial services, SaaS, and consumer e-commerce

Features:
- Overview dashboard with dataset counts and risk distribution
- Search/filter all 60 pairs by advertiser, claim, industry, pair ID, risk
- Claim-by-claim audit detail with closest exact text block from the paired snapshot
- Page snapshot text blocks shown for manual verification
- Batch screening and priority queue
- CSV exports: full claim-level report, filtered results, pair report, dataset manifest, executive summary
- Guided dataset-aware AdProof Assistant (local rules; no external AI/API)

Run:
1. Extract the ZIP.
2. Keep index.html, styles.css, app.js and dataset.json together.
3. Because the app loads dataset.json with fetch(), run it through a local server:
   - If Python is installed, open a terminal in this folder and run: python -m http.server 8000
   - Open http://localhost:8000
   - Alternatively use VS Code Live Server.
4. Navigate to Dataset audits and click Inspect on a pair (e.g. P01).

Methodology limitation:
This is a transparent heuristic prototype, not a connected LLM and not a legal/compliance decision system. Scores/risk labels are estimates based on text overlap and critical terms. Evidence quote is the closest matching extracted block, not a ground-truth annotation. Manually inspect exact claim, evidence, page position and qualifiers before acting. No live URLs are fetched; use the provided snapshots.


More features note:
The added modules are client-side demo tools. Review notes and drafts stay in this browser only. The rewrite checker and comparisons are heuristic aids; no connected LLM, backend database, live URL fetch, legal verdict, or cloud sync is included.

NEW: Check my ad
Open the “Check my ad” page from the sidebar. Enter an ad headline, optional description, and the landing-page text, then click “Check message match”. The checker reports approximate keyword overlap and flags numeric details or strong promises not found in the pasted page text. This is a heuristic helper, not a truth, legal, or compliance verdict.
