# TriageAI: Enterprise Search Term Optimization Engine

## The Problem
PPC Analysts face thousands of search terms weekly, falling into a critical statistical trap: treating small-sample noise as actionable data. A search query with two clicks and one conversion mathematically proves nothing, yet manual processes often promote it, wasting budget.

## Key Innovations (The Data Science Architecture)
Our system bypasses simple heuristic rules and implements a mathematically sound MLOps pipeline:

1. **Empirical Bayes (Beta-Binomial Shrinkage):** We calculate the global account conversion rate and use it as a Bayesian prior. Individual query metrics are shrunk toward this mean, preventing low-volume "lucky" queries from being falsely promoted.
2. **Wilson Score Interval:** We calculate the conservative lower bound of the conversion rate at a 95% confidence level. A term is only marked for "Promote" if its worst-case statistical scenario is still profitable.
3. **Semantic NLP Clustering:** Using `sentence-transformers/all-MiniLM-L6-v2`, we generate vector embeddings for all queries, reduce dimensionality with UMAP, and cluster them via HDBSCAN. Sparse data is pooled across these semantic clusters to identify systemic intent waste.
4. **Search Term Isolation & N-Gram Waste:** The engine automatically prevents keyword cannibalization by generating "Negative Exact" cross-campaign rules, and actively scans for 1-gram tokens bleeding money across the entire account.
5. **Google Ads Editor Integration:** The dual-CSV output is immediately actionable, formatted precisely to Google's proprietary bulk-upload schema.

## Execution Guide
1. Run `pip install -r requirements.txt`.
2. Place the dataset in the root directory named `search_terms_report.csv`.
3. Execute `python main.py`.
4.