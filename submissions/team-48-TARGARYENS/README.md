# DevSprint Search Term Triage Engine

A local Streamlit MVP for explainable Google Ads search-term triage. It processes 25,000+ rows in memory, assigns `PROMOTE`, `BLOCK`, `IGNORE`, or `REVIEW`, shows confidence and a plain-language reason, groups normalized duplicate queries, supports session-only reviewer corrections, and exports CSV worklists.

## Run

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Upload a UTF-8 or standard Google Ads CSV with search term, clicks, impressions, cost, and conversions. Title-case headers and snake_case headers such as `search_term`, `match_type`, and `conversion_value` are supported. Campaign and ad group are retained for targeting. Numeric values with commas or currency symbols are parsed. The app starts empty and does not include generated sample rows.

## Decision policy

- **PROMOTE:** at least 20 clicks and 2 conversions. Confidence rises with more volume. A single conversion can never auto-promote.
- **BLOCK:** at least 25 clicks, spend, and zero conversions.
- **REVIEW:** fewer than 8 clicks, including any conversion on thin data; or conversions that do not meet promotion volume.
- **IGNORE:** the remaining low-signal terms, retained for monitoring.

Rules are conservative starting points, not universal account benchmarks. Reasons expose the evidence. Reviewer changes apply to the current session and are included in the full export. Duplicate grouping normalizes case, punctuation, and whitespace; it does not use semantic or fuzzy matching.

## Export

Download a complete audit CSV or separate worklists. The promote list suggests exact-match keywords; the negative list formats exact negatives and assigns ad-group scope when available, otherwise campaign scope. Review targeting, match types, and policy before importing into Google Ads.
