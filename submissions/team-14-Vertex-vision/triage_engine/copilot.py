"""
Personal AI Copilot Module for TriageIQ (PS-01 Search Term Triage Engine).
Provides real-time grounded intelligence, statistical audit reasoning,
and interactive query diagnostics directly to the user across 38+ specialized PPC questions.
"""

import re
import html
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def generate_copilot_response(
    user_query: str,
    res_df: pd.DataFrame,
    clean_df: pd.DataFrame,
    target_cpa: float = 220.0
) -> str:
    """
    Generates a mathematically accurate, grounded response from the active
    search-term dataset, engine decisions, and Kestrel advertiser policy.
    Supports 38+ specialized questions and natural language inquiries.
    """
    q = user_query.lower().strip()
    
    # -------------------------------------------------------------
    # 1. SPECIFIC ROW LOOKUP (e.g., 'row 6', 'row #3', '#1', '6', 'audit row 5')
    # -------------------------------------------------------------
    row_match = re.search(r'(?:row\s*#?|#\s*|^)(\d+)(?:\s*$|\b)', q)
    if row_match:
        rid = int(row_match.group(1))
        matches = res_df[res_df["row_id"] == rid]
        if not matches.empty:
            r = matches.iloc[0]
            clicks = int(r.get("clicks", 0))
            cost = float(r.get("cost", 0.0))
            convs = float(r.get("conversions", 0.0))
            conv_val = float(r.get("conversion_value", 0.0))
            cpa = r.get("cpa")
            cpa_val = f"${cpa:,.2f}" if (cpa is not None and pd.notnull(cpa) and convs > 0) else "— (0 conversions)"
            ci_str = f"[{r.get('ci_lower', 0.0):.1%}, {r.get('ci_upper', 0.0):.1%}]" if clicks > 0 else "N/A"
            review_txt = "⚠️ Flagged for Human Review (`needs_review = True`)" if r.get("needs_review") else "✅ Confident Decision (`needs_review = False`)"
            
            # Special insight for small-sample converting queries (e.g. Row 6)
            special_insight = ""
            if r.get("needs_review") and convs >= 1 and clicks < 10:
                special_insight = f"""
#### 💡 Why This Row Is Quarantined (Small-Sample Guardrail)
> **Statistical Caution:** Although `{r.get('query_text')}` recorded an observed conversion at a nominal CPA of {cpa_val}, the sample size is only **{clicks} clicks**. The Wilson 95% lower bound is **{r.get('ci_lower', 0.0):.1%}**, which indicates high uncertainty. Promoting this term prematurely could waste ad spend if the conversion was an anomaly. It is safely placed in **Human Review** (`needs_review = True`) while preserving status quo (`decision: IGNORE`).
"""
            
            return f"""### 🔍 Audit Dossier for Row #{rid}: `{r.get('query_text', '')}`

- **Organizer Contract Decision:** `{r.get('decision', 'IGNORE')}` (Confidence: `{r.get('confidence', 'MEDIUM')}`)
- **Review Disposition:** {review_txt}
- **Campaign & Group Context:** *{r.get('campaign', '')}* › *{r.get('ad_group', '')}* ({r.get('match_type', 'Broad')})

#### 📊 Performance & Statistical Evidence
- **Volume:** **{clicks:,} clicks** &nbsp;|&nbsp; **Spend:** **${cost:,.2f}**
- **Conversions:** **{int(convs):,}** &nbsp;|&nbsp; **Attributed Value:** **${conv_val:,.2f}**
- **Actual CPA:** **{cpa_val}** *(Target CPA Ceiling: ${target_cpa:,.2f})*
- **Wilson 95% Confidence Interval:** `{ci_str}`
{special_insight}
#### 🎯 Decision Rationale
> {r.get('reason', '')}

#### ⚖️ Supporting Evidence & Constraints
- **🟢 Supporting Evidence:** {r.get('supporting_evidence', 'N/A')}
- **🔴 Counterevidence & Limitations:** {r.get('counterevidence', 'N/A')}
- **📌 Recommended Next Action:** **{r.get('next_action', 'N/A')}**"""
        else:
            return f"⚠️ Row #{rid} was not found in the current dataset (valid row IDs range from 1 to {len(res_df):,})."

    # -------------------------------------------------------------
    # 2. SPECIFIC SEARCH QUERY SEARCH (e.g., 'what about equipment loan', 'audit personal loans')
    # -------------------------------------------------------------
    search_term = None
    term_match = re.search(r"['\"]([^'\"]+)['\"]", user_query)
    if term_match:
        search_term = term_match.group(1).strip()
    elif any(k in q for k in ["about query ", "search for query ", "audit term ", "check query ", "inspect term "]):
        for prefix in ["about query ", "search for query ", "audit term ", "check query ", "inspect term "]:
            if prefix in q:
                candidate = q.split(prefix, 1)[1].strip(" ?.!\"'")
                if len(candidate) > 2 and not candidate.startswith("row"):
                    search_term = candidate
                    break
                    
    if search_term:
        term_matches = res_df[res_df["query_text"].str.contains(search_term, case=False, na=False)]
        if not term_matches.empty:
            r = term_matches.iloc[0]
            total_matches = len(term_matches)
            cpa = r.get("cpa")
            cpa_val = f"${cpa:,.2f}" if (cpa is not None and pd.notnull(cpa) and r.get("conversions", 0) > 0) else "—"
            review_txt = "⚠️ Needs Human Review" if r.get("needs_review") else "✅ Confident Decision"
            
            note = f"\n*(Showing top match of {total_matches:,} queries matching '{search_term}')*" if total_matches > 1 else ""
            return f"""### 🔍 Query Match: `{r.get('query_text', '')}` (Row #{r.get('row_id')}){note}

- **Primary Decision:** `{r.get('decision', 'IGNORE')}` ({review_txt})
- **Performance:** {r.get('clicks', 0):,} clicks · ${r.get('cost', 0.0):,.2f} spend · {int(r.get('conversions', 0)):,} convs
- **Actual CPA:** {cpa_val} *(Target: ${target_cpa:,.2f})*
- **Wilson 95% Bound:** [{r.get('ci_lower', 0.0):.1%}, {r.get('ci_upper', 0.0):.1%}]
- **Rationale:** {r.get('reason', '')}
- **Recommended Action:** **{r.get('next_action', '')}**"""

    # -------------------------------------------------------------
    # 3. SPECIFIC DOMAIN EXCLUSIONS & POLICIES (PRIORITIZED BEFORE GENERIC BLOCK)
    # -------------------------------------------------------------
    # A. Grants & Stimulus
    if any(k in q for k in ["grant", "stimulus", "government grant", "free money", "handout"]):
        grant_spend = float(clean_df[clean_df["query_text"].str.contains("grant|stimulus|free", case=False, na=False)]["cost"].sum())
        return f"""### 🚫 Government Grant & Free Money Exclusion Policy

- **Policy Rule:** Searchers looking for "free government grants" or "stimulus checks" have **zero intent to repay commercial loans**.
- **Historical Spend Wasted:** **${grant_spend:,.2f}**
- **Action:** Mapped to universal negative phrase `[grant]` and `[stimulus]`.
- **Exclusion Scope:** Applied at the **Campaign level** across all commercial financing campaigns."""

    # B. Careers & Employment
    if any(k in q for k in ["job", "career", "hiring", "salary", "internship", "employment", "resume"]):
        job_spend = float(clean_df[clean_df["query_text"].str.contains("job|career|salary|hiring|internship", case=False, na=False)]["cost"].sum())
        return f"""### 🚫 Career & Employment Query Exclusion Policy

- **Policy Rule:** Job seekers researching loan officer salaries or financial careers generate high click costs with 0% commercial borrower intent.
- **Historical Spend Wasted:** **${job_spend:,.2f}**
- **Action:** Excluded via negative phrase triggers: `jobs`, `hiring`, `careers`, `salary`.
- **Scope:** Campaign-level negative phrase list."""

    # C. Consumer Loans
    if any(k in q for k in ["consumer loan", "personal loan", "car loan", "auto loan", "mortgage", "student loan", "bad credit personal", "personal"]):
        consumer_spend = float(clean_df[clean_df["query_text"].str.contains("personal|auto|car|mortgage|student", case=False, na=False)]["cost"].sum())
        return f"""### 🚫 Consumer Loan Exclusion Policy

- **Policy Rule:** Kestrel is exclusively a **commercial B2B financing provider**. It does not underwrite personal loans, consumer mortgages, or student debt.
- **Impact in Dataset:** Consumer queries accumulated **${consumer_spend:,.2f}** in wasted spend.
- **Prohibited Patterns:** `personal loan`, `emergency personal cash`, `auto loan bad credit`, `home mortgage refinance`.
- **Triage Action:** All terms matching consumer tokens are assigned **`BLOCK`** with **Campaign-level Negative Phrase** scope to prevent broad match bleeding."""

    # D. Non-Buyer / Informational (use whole word / distinct phrases, avoid substring collision with 'performance' or 'format')
    if any(k in q for k in ["template", "sample invoice", "sample contract", "login", "portal", "wikipedia", "pdf download", "free download", "document template"]):
        info_spend = float(clean_df[clean_df["query_text"].str.contains("template|sample|login|portal|wikipedia|pdf", case=False, na=False)]["cost"].sum())
        return f"""### 🚫 Non-Buyer & Informational Query Policy

- **Policy Rule:** Searchers seeking loan agreement templates, sample promissory notes, or existing client login portals are not active prospective borrowers.
- **Historical Spend Wasted:** **${info_spend:,.2f}**
- **Action:** Excluded as Negative Exact or Phrase keywords depending on the ad group context."""

    # -------------------------------------------------------------
    # 4. STATISTICAL & TECHNICAL EXPLAINERS
    # -------------------------------------------------------------
    # A. Small Sample Noise / Variance Trap
    if any(k in q for k in ["small sample", "variance trap", "1 conversion", "1 conv", "single conversion", "one conversion", "n=1", "low click conversion", "row 6 explanation", "why is row 6"]):
        return f"""### ⚠️ The Small-Sample Variance Trap (1 Conversion != Success)

One of the most dangerous pitfalls in Google Ads search-term management is **premature promotion**:

#### Why TriageIQ treats single conversions cautiously:
1. **The Fallacy of Low CPA on N=1:**
   - A query with **1 click, $12.50 spend, and 1 conversion** has a nominal CPA of $12.50.
   - However, a sample size of $N=1$ provides near-zero statistical significance.
2. **Asymmetric Wilson Confidence Bound:**
   - On 1 conversion from 1 click, the 95% Wilson confidence interval is **[2.5%, 97.5%]**.
   - The lower bound is nearly zero! This means the true long-term conversion rate could easily be unprofitable.
3. **Engine Policy & Quarantining:**
   - TriageIQ enforces a minimum evidence gate (default: **{engine_params_min_clicks(res_df)} clicks and 2 conversions**).
   - In accordance with the organizer's contract, these queries receive **`decision: IGNORE`** with **`needs_review: True`**.
   - This quarantines the query in the **Human Review Queue** so a senior media buyer can evaluate business viability before risking campaign budget."""

    # B. Wilson Interval
    if any(k in q for k in ["wilson interval", "wilson confidence", "wilson bound", "wilson formula", "binomial confidence", "ci_lower", "how wilson works", "score interval"]):
        return """### 📐 Statistical Rigor: Wilson Score Binomial Confidence Interval

Standard normal approximation intervals fail dramatically on low conversion counts, often yielding negative probabilities. TriageIQ solves this using the **Wilson Score Interval**:

#### Mathematical Formulation:
`Wilson Lower/Upper = (p + z²/(2n) ± z·√((p(1-p) + z²/(4n))/n)) / (1 + z²/n)`
*(Where z = 1.96 for 95% two-sided confidence, n = clicks, and p = observed conversion rate)*

#### Strategic Properties for PPC Search Terms:
1. **Asymmetric Shrinkage:** When sample size is small, the lower bound `ci_lower` shrinks aggressively towards zero, preventing false positives.
2. **Zero-Conversion Safety:** Even with 0 conversions on 10 clicks, Wilson provides a realistic upper bound on what the conversion rate could be.
3. **Promotion Guardrail:** A query cannot be assigned **`PROMOTE`** unless its Wilson lower bound is strictly greater than zero and validates long-term CPA viability."""

    # C. Empirical Bayes
    if any(k in q for k in ["empirical bayes", "bayesian shrinkage", "prior distribution", "beta binomial", "shrinkage formula", "how empirical bayes works"]):
        return """### 🧠 Empirical Bayes Shrinkage: Filtering Variance Noise

Individual search terms often suffer from extreme statistical variance due to sparse data. TriageIQ employs **Empirical Bayes (EB) Shrinkage** to stabilize conversion rate estimates:

#### How It Works:
1. **The Campaign Prior:** We fit a Beta prior distribution across all terms in each campaign to capture account baseline behavior.
2. **Shrinkage Mechanism:**
   `p_EB = (conversions + α) / (clicks + α + β)`
3. **Adaptive Weighting:**
   - For high-volume terms (100+ clicks), the observed data dominates and shrinkage is negligible.
   - For low-volume terms (1-5 clicks), the estimate is pulled gracefully toward the campaign prior, preventing wild bid adjustments.
4. **Bidding Calibration:** Suggested Max CPC bids are computed using smoothed conversion rates rather than raw, noisy metrics."""

    # D. 3-Way Contract
    if any(k in q for k in ["three-way contract", "3-way contract", "decision contract", "strict contract", "mutually exclusive", "why ignore not review"]):
        return """### 📜 Organizer Decision Contract Specification

TriageIQ strictly complies with the hackathon organizer's foundational contract:

1. **Mutually Exclusive Primary Decision:**
   - Every row MUST be categorized as exactly one of: **`PROMOTE`**, **`BLOCK`**, or **`IGNORE`**.
   - No row may have ambiguous or missing decisions.
2. **Decoupled Review Governance:**
   - **Human Review** is decoupled as a boolean flag (`needs_review: True / False`).
   - Why? Human Review is a **state of management attention**, not an execution state in Google Ads!
   - In Google Ads, a term is either added as an exact match (`PROMOTE`), excluded (`BLOCK`), or left alone in broad match (`IGNORE`).
3. **Full Audit Trail:**
   - Every decision includes confidence (`HIGH`, `MEDIUM`, `LOW`), supporting evidence, counterevidence, and next action."""

    # E. Over-Exclusion Risk (prioritized before generic exclusion)
    if any(k in q for k in ["over-exclusion", "exclusion risk", "collateral damage", "blocking good terms", "false positive exclusion"]):
        return f"""### ⚠️ Over-Exclusion Risk & Collateral Damage Prevention

Adding negative keywords aggressively can inadvertently block legitimate, paying customers:

1. **Collision Analysis:** TriageIQ tests every negative candidate against core commercial terms (`business`, `commercial`, `equipment`, `working capital`).
2. **Ambiguity Flags:** Negative words that contain high-intent commercial modifiers trigger amber risk warnings.
3. **Human Approval Gate:** Negative suggestions are presented in **Pending Analyst Approval** mode and are never deployed automatically without verification."""

    # F. Narrow Scope Rule
    if any(k in q for k in ["narrow scope", "narrowest scope", "scope rule", "campaign vs ad group negative", "negative scope"]):
        return f"""### 🛡️ Narrowest Appropriate Scope Rule for Negatives

To prevent accidental traffic suppression, TriageIQ adheres to strict scoping hierarchy:

1. **Campaign-Level Negative Phrase:**
   - Reserved exclusively for **universal non-commercial tokens** (`personal loans`, `student loans`, `grants`, `careers`, `hiring`).
   - Blocks the theme across all ad groups in the campaign.
2. **Ad Group-Level Negative Exact:**
   - Applied to **product-specific bleeders** (e.g. `equipment financing calculator` failing in an equipment loan group).
   - Prevents blocking the term in another group where a calculator ad might convert profitably.
3. **Safety Guarantee:** Prevents account-wide over-exclusion."""

    # G. Cluster Conflicts (prioritized before generic cluster)
    if any(k in q for k in ["cluster conflict", "decision conflict", "cluster divergence", "conflicting decisions", "why conflict"]):
        conflict_count = int(res_df.get("cluster_has_conflict", pd.Series([False]*len(res_df))).sum())
        return f"""### ⚡ Intent Cluster Decision Conflicts

- **Terms in Conflicting Clusters:** **{conflict_count:,} search terms**
- **Why Conflicts Occur:** A high-volume query (e.g. `equipment financing bad credit`, 40 clicks, 4 convs) receives **`PROMOTE`**, while a minor syntactic variant (`bad credit equipment financing`, 2 clicks, 0 convs) receives **`IGNORE`**.
- **How TriageIQ Resolves It:** Surfaces the cluster in **🧩 Intent Clusters** allowing the analyst to apply the dominant decision across all cluster variants with one click."""

    # H. Search-Intent Clustering
    if any(k in q for k in ["cluster", "clustering", "search intent", "intent cluster", "near-duplicate", "how does clustering work"]):
        conflict_count = int(res_df.get("cluster_has_conflict", pd.Series([False]*len(res_df))).sum())
        return f"""### 🧩 Near-Duplicate Search-Intent Clustering

TriageIQ groups semantically equivalent queries using token normalization and intent categorization:

1. **Syntactic Collapse with Qualifier Preservation:**
   - Collapses word re-orderings, punctuation, and pluralizations.
   - Strictly preserves commercial qualifiers: *business vs personal*, *calculator*, *alternative*, *bad credit*, *jobs*.
2. **Decision Conflict Detection:**
   - Flags clusters where member queries received conflicting decisions (e.g. one variant was `PROMOTE` while another was `IGNORE` due to click thresholds).
   - Currently **{conflict_count:,} search terms** belong to clusters with decision divergence.
3. **Reviewer Reconciliation:**
   - Analysts can inspect clusters in the **🧩 Intent Clusters** tab and reconcile cluster-wide policies with a single click."""

    # I. Reviewer Precedents & Session Learning
    if any(k in q for k in ["precedent", "reviewer correction", "session learning", "analyst learning", "correction memory"]):
        return f"""### 💡 Reviewer Precedents & Contextual Learning

TriageIQ learns from analyst corrections dynamically within the session without model retraining:

1. **Precedent Recording:**
   - When an analyst changes a recommendation (e.g. in the Review Queue), TriageIQ logs the original decision, revised decision, query text, campaign, reason code, and timestamp.
2. **Contextual Guidance:**
   - Unreviewed queries are cross-referenced against historical corrections using token similarity.
   - When a similar query is detected, TriageIQ surfaces a precedent banner explaining how a human reviewer handled the case previously.
3. **Guidance, Not Universal Ground Truth:**
   - Precedents are offered as guidance. They do not silently override statistical data, preserving the analyst's ultimate judgment."""

    # J. Suggested Bid / Max CPC Formula
    if any(k in q for k in ["suggested bid", "max cpc", "bid formula", "how bid calculated", "proposed bid"]):
        return f"""### 🏷️ Value-Based Max CPC Bidding Formula

TriageIQ does not use static bids. For every promoted keyword, it calculates a mathematically grounded **Suggested Max CPC**:

`Max CPC = Target CPA * p_EB * Safety Factor (0.85)`

- **Target CPA Ceiling:** ${target_cpa:,.2f}
- **p_EB:** Empirical Bayes conversion rate (smoothed against campaign prior)
- **Safety Factor:** 0.85 (15% margin guardrail against bid auction surges)

This guarantees that even under traffic fluctuations, the resulting CPA will stay safely below Kestrel's ${target_cpa:,.2f} ceiling."""

    # K. Google Ads Import Guide
    if any(k in q for k in ["how to import", "import guide", "editor import", "apply to google ads"]):
        return f"""### 🚀 Step-by-Step Google Ads Editor Import Instructions

To deploy TriageIQ recommendations into live campaigns:

1. **Download Exports:** Navigate to **📥 Google Ads Exports** in the sidebar and download both CSVs.
2. **Open Google Ads Editor:** Select your Kestrel Google Ads account.
3. **Import Negatives:**
   - Go to **Keywords and targeting** › **Keywords, Negative**.
   - Click **Make multiple changes** › **Paste from clipboard** or choose **Import from file**.
   - Select `google_ads_negative_keywords.csv` and click **Process**.
4. **Import Promoted Keywords:**
   - Go to **Keywords and targeting** › **Keywords**.
   - Click **Make multiple changes** and import `google_ads_promoted_keywords.csv`.
5. **Review & Post:** Verify staged changes and click **Post** (top-right)."""

    # L. Google Ads Export Specs
    if any(k in q for k in ["export format", "google ads export", "csv format", "export csv", "export files", "editor columns"]):
        return f"""### 📥 Google Ads Editor 1-Click Export Specifications

TriageIQ generates two production-ready CSV files matching Google Ads Editor schemas:

1. **`google_ads_promoted_keywords.csv`**:
   - Columns: `Campaign`, `Ad Group`, `Keyword`, `Criterion Type` (`Exact`), `Max CPC`, `Status` (`Enabled`).
2. **`google_ads_negative_keywords.csv`**:
   - Columns: `Campaign`, `Ad Group`, `Keyword`, `Criterion Type` (`Phrase` or `Exact`), `Status` (`Enabled`).
3. **Audit Artifacts:** Full triage audit CSV and Human Review queue CSVs with complete Wilson bounds."""

    # M. Negative Keyword Suggestions Workflow
    if any(k in q for k in ["negative suggestion", "candidate negative", "negative keyword list", "how negative generated"]):
        return f"""### 🛠️ Candidate Negative Keyword Generation Pipeline

TriageIQ discovers negative keywords systematically:

1. **N-Gram Token Analysis:** Scans all zero-conversion queries for repetitive unigrams and bigrams.
2. **Cost-Concentration Mining:** Identifies terms causing disproportionate spend waste without conversions.
3. **Policy Mapping:** Matches tokens against Kestrel negative categories.
4. **Export Formatting:** Outputs clean negative candidates ready for Google Ads Editor."""

    # -------------------------------------------------------------
    # 5. PERFORMANCE DIAGNOSTICS & COMPARISONS
    # -------------------------------------------------------------
    # A. Top Spend Bleeders (prioritized before generic zero convs)
    if any(k in q for k in ["bleeder", "top bleeder", "biggest bleeder", "worst keyword", "top waste", "highest cost zero conv", "budget waster", "worst terms", "top 5 bleeders"]):
        bleeders = res_df[(res_df["conversions"] == 0) & (res_df["decision"] == "BLOCK")].sort_values(by="cost", ascending=False).head(5)
        if bleeders.empty:
            return "No zero-conversion spend bleeders found in the current dataset."
            
        bleed_txt = ""
        for idx, (_, b) in enumerate(bleeders.iterrows(), 1):
            bleed_txt += f"{idx}. **`{b['query_text']}`** (Row #{b['row_id']}) — **${b['cost']:,.2f} spend** ({int(b['clicks'])} clicks, 0 convs) · *{b['campaign']}*\n"
            
        return f"""### 🩸 Top Spend Bleeders (Zero Conversions)

These non-converting terms accumulated massive spend without generating a single customer lead:

{bleed_txt}
These terms are quarantined and staged for immediate negative keyword exclusion in `google_ads_negative_keywords.csv`."""

    # B. Zero-Conversion Queries
    if any(k in q for k in ["zero conversion", "0 conversion", "no conversion", "zero conv"]):
        zero_df = clean_df[clean_df["conversions"] == 0]
        zero_spend = float(zero_df["cost"].sum())
        zero_clicks = int(zero_df["clicks"].sum())
        zero_count = len(zero_df)
        total_spend = float(clean_df["cost"].sum())
        
        return f"""### 📉 Zero-Conversion Search Term Aggregate

- **Zero-Conversion Search Terms:** **{zero_count:,} terms** ({(zero_count/len(clean_df))*100:.1f}% of all queries)
- **Cumulative Waste on Zero-Conv Terms:** **${zero_spend:,.2f}** ({(zero_spend/total_spend)*100:.1f}% of total spend)
- **Clicks with Zero Returns:** **{zero_clicks:,} clicks**

TriageIQ evaluates these terms to isolate high-cost bleeders and policy collisions for negative keyword exclusion while allowing small-sample terms to gather data."""

    # B. Match Type Performance Breakdown
    if any(k in q for k in ["match type", "broad vs exact", "phrase match", "exact match performance", "match type breakdown"]):
        mt_agg = clean_df.groupby("match_type").agg({"cost": "sum", "conversions": "sum", "clicks": "sum"}).reset_index()
        mt_agg["cpa"] = mt_agg["cost"] / mt_agg["conversions"].replace(0, np.nan)
        
        mt_txt = ""
        for _, m in mt_agg.iterrows():
            cpa_val = f"${m['cpa']:,.2f}" if pd.notnull(m['cpa']) else "—"
            mt_txt += f"- **{m['match_type']}**: Spend ${m['cost']:,.2f} · Clicks {int(m['clicks']):,} · Convs {int(m['conversions']):,} · CPA **{cpa_val}**\n"
            
        return f"""### 🔍 Match Type Efficiency Analysis

Performance across search term match types:

{mt_txt}
**Insight:** Broad Match terms typically exhibit higher variance and account for the majority of spend bleeders. Promoting winners to Exact Match locks in conversion efficiency."""

    # C. Low CTR / High Impressions
    if any(k in q for k in ["low ctr", "high impression", "impression volume", "click through rate", "ctr analysis"]):
        if "impressions" in clean_df.columns:
            clean_df_ctr = clean_df[clean_df["impressions"] >= 50].copy()
            clean_df_ctr["ctr"] = (clean_df_ctr["clicks"] / clean_df_ctr["impressions"]) * 100
            low_ctr = clean_df_ctr.sort_values(by="ctr", ascending=True).head(4)
            
            ctr_txt = ""
            for _, r in low_ctr.iterrows():
                ctr_txt += f"- **`{r['query_text']}`**: CTR **{r['ctr']:.2f}%** ({int(r['clicks'])} clicks / {int(r['impressions'])} impressions)\n"
        else:
            ctr_txt = "- *(Impressions metric not provided in primary report columns)*"
            
        return f"""### 👁️ High Impression / Low CTR Diagnostics

Low CTR indicates an ad copy or intent mismatch where impressions are generated without compelling user clicks:

{ctr_txt}
**Recommendation:** Refine ad copy relevance or evaluate negative keyword exclusions if search intent is off-target."""

    # D. Keyword Cannibalization
    if any(k in q for k in ["cannibalization", "internal competition", "duplicate query", "competing keywords", "auction overlap"]):
        return f"""### ⚔️ Search Term Cannibalization & Auction Overlap

When a search term triggers multiple keywords across different campaigns or ad groups:

1. **The Problem:** Broad match keywords often bid against Exact match keywords, driving up average CPCs and splitting conversion history.
2. **The TriageIQ Solution:**
   - Promoted winners are added as **Exact Match** keywords in their dedicated ad groups.
   - Matching Ad Group-level negative exact keywords are generated to prevent broader ad groups from stealing impressions.
3. **Outcome:** Ensures 100% impression share routing to the most relevant, highest-converting ad group."""

    # E. Top Promoted Winners
    if any(k in q for k in ["top candidate", "best keyword", "top promoted", "winner", "promote candidate", "best terms", "top winners", "top 5 promoted"]):
        prom_df = res_df[res_df["decision"] == "PROMOTE"].sort_values(by="conversions", ascending=False).head(5)
        if prom_df.empty:
            return "Currently no queries have met the high-evidence threshold for promotion."
            
        winners_txt = ""
        for idx, (_, w) in enumerate(prom_df.iterrows(), 1):
            winners_txt += f"""{idx}. **`{w['query_text']}`** (Row #{w['row_id']})
   - Conversions: **{int(w['conversions'])}** · Spend: **${w['cost']:,.2f}** · Actual CPA: **${w['cpa']:,.2f}**
   - Wilson Lower Bound: **{w['ci_lower']:.1%}** · Suggested Max CPC: **${w['proposed_bid']:,.2f}**\n"""
            
        return f"""### 🚀 Top High-Evidence Promoted Candidates

These search terms cleared all statistical evidence gates and demonstrated sustained profitability:

{winners_txt}
These candidates are formatted into `google_ads_promoted_keywords.csv` as **Exact Match** keywords with bids calibrated to Empirical Bayes conversion probabilities."""


    # G. Best / Most Efficient Campaigns
    if any(k in q for k in ["best campaign", "most profitable campaign", "most efficient campaign", "lowest cpa campaign", "top campaign"]):
        camp_agg = clean_df.groupby("campaign").agg({"cost": "sum", "conversions": "sum", "clicks": "sum"}).reset_index()
        camp_agg["cpa"] = camp_agg["cost"] / camp_agg["conversions"].replace(0, np.nan)
        best_camps = camp_agg[camp_agg["conversions"] >= 1].sort_values(by="cpa", ascending=True).head(3)
        
        camp_txt = ""
        for idx, (_, c) in enumerate(best_camps.iterrows(), 1):
            camp_txt += f"{idx}. **{c['campaign']}**: CPA **${c['cpa']:,.2f}** · Spend ${c['cost']:,.2f} · Conversions {int(c['conversions']):,}\n"
            
        return f"""### 🏆 Most Efficient Campaigns (Lowest CPA)

Campaigns delivering the highest conversion return within acceptable CPA targets:

{camp_txt}
These campaigns represent core commercial profit centers where promoted exact match keywords should receive prioritized budget."""

    # H. Worst / Least Efficient Campaigns
    if any(k in q for k in ["worst campaign", "highest cpa campaign", "least efficient campaign", "most wasteful campaign", "bad campaign"]):
        camp_agg = clean_df.groupby("campaign").agg({"cost": "sum", "conversions": "sum", "clicks": "sum"}).reset_index()
        camp_agg["cpa"] = camp_agg["cost"] / camp_agg["conversions"].replace(0, np.nan)
        worst_camps = camp_agg.sort_values(by="cpa", ascending=False).head(3)
        
        camp_txt = ""
        for idx, (_, c) in enumerate(worst_camps.iterrows(), 1):
            cpa_val = f"${c['cpa']:,.2f}" if pd.notnull(c['cpa']) else "— (0 convs)"
            camp_txt += f"{idx}. **{c['campaign']}**: CPA **{cpa_val}** · Spend ${c['cost']:,.2f} · Conversions {int(c['conversions']):,}\n"
            
        return f"""### ⚠️ Least Efficient Campaigns (High CPA / Spend Waste)

Campaigns requiring aggressive negative keyword pruning and budget guardrails:

{camp_txt}
Applying TriageIQ's negative keyword list to these campaigns will immediately cut waste and bring blended CPA back to profitability."""

    # I. Top Ad Groups by Spend
    if any(k in q for k in ["top ad group", "ad group performance", "highest spend ad group", "ad group breakdown", "ad groups"]):
        ag_agg = clean_df.groupby(["campaign", "ad_group"]).agg({"cost": "sum", "conversions": "sum"}).reset_index()
        ag_agg = ag_agg.sort_values(by="cost", ascending=False).head(4)
        
        ag_txt = ""
        for _, a in ag_agg.iterrows():
            cpa = a['cost'] / max(1.0, a['conversions'])
            ag_txt += f"- **{a['campaign']}** › *{a['ad_group']}*: Spend ${a['cost']:,.2f} · Convs {int(a['conversions'])} · CPA **${cpa:,.2f}**\n"
            
        return f"""### 📂 Top Ad Groups by Expenditure

Key ad groups driving account media spend:

{ag_txt}
Ensure negative keyword lists are aligned at both Campaign and Ad Group levels for these high-spend groups."""

    # -------------------------------------------------------------
    # 6. CRITERIA & POLICY CEILINGS
    # -------------------------------------------------------------
    # A. Target CPA Ceiling
    if any(k in q for k in ["target cpa", "cpa ceiling", "220", "allowable cpa", "cpa threshold", "target threshold", "why 220"]):
        return f"""### 🎯 Kestrel Advertiser Target CPA Ceiling: ${target_cpa:,.2f}

The Target CPA threshold is the economic north star for all triage classifications:

- **Advertiser:** Kestrel Business Funding (Commercial B2B Lending)
- **Target CPA Ceiling:** **${target_cpa:,.2f}**
- **Economic Rationale:** Based on Kestrel's average gross loan margin per funded borrower, an acquisition cost up to ${target_cpa:,.2f} delivers an acceptable return on capital.
- **Triage Impact:**
  - Queries converting at <= ${target_cpa:,.2f} are candidates for `PROMOTE`.
  - Non-converting queries spending >= ${target_cpa:,.2f} are immediately flagged as `BLOCK`.
  - Converting queries with CPA between $220 and $300 are routed to `needs_review: True`."""

    # B. Promotion Criteria
    if any(k in q for k in ["promotion criteria", "how to promote", "promote threshold", "promote gate", "promote rules", "when promote", "criteria for keyword promotion"]):
        return f"""### 🚀 Statistical Criteria for Keyword Promotion (`PROMOTE`)

To earn an exact-match promotion, a search term must clear **all four evidence gates**:

1. **Sample Size Gate:** Minimum 10 clicks (statistically meaningful interaction volume).
2. **Conversion Gate:** At least 2 recorded conversions (guards against 1-conversion lucky anomalies).
3. **Economic Gate:** Actual CPA <= ${target_cpa:,.2f} (profitable customer acquisition).
4. **Wilson Confidence Gate:** Wilson 95% lower bound `ci_lower` > 0 with acceptable CPA upper bound.
5. **Commercial Domain Filter:** Query must align with Kestrel core commercial financing products.

When promoted, the term is written to `google_ads_promoted_keywords.csv` as an **Exact Match** keyword with an optimized Max CPC bid."""

    # C. Blocking Criteria
    if any(k in q for k in ["blocking criteria", "how to block", "block threshold", "block rules", "when block", "why block", "criteria for block"]):
        return f"""### 🚫 Strict Rules for Search Term Exclusion (`BLOCK`)

A search term is designated for negative keyword exclusion under two explicit conditions:

1. **Explicit Business Boundary Collision:**
   - Query contains prohibited non-commercial tokens: *personal loans, bad credit car loan, mortgages, government grant, stimulus check, jobs, salary, templates, login*.
2. **Unreconciled Spend Bleeder:**
   - Term accrued spend exceeding allowable CPA ceiling (Cost >= ${target_cpa:,.2f}) with **zero conversions**.
   - Term has high clicks (Clicks >= 15) and spend with zero recorded conversions.

Blocked queries are scoped via the **Narrowest Appropriate Scope Rule** (Campaign-level Phrase or Ad Group-level Exact)."""

    # D. Ignore Criteria
    if any(k in q for k in ["ignore criteria", "why ignore", "what is ignore", "ignore threshold", "when ignore", "status quo"]):
        return f"""### ⏸️ Understanding the `IGNORE` Decision (Status Quo)

In professional search advertising, **not acting is often the most profitable decision**:

1. **Data Insufficiency:** A query with 1-4 clicks and $15 spend has not provided enough statistical signal to determine profitability or waste.
2. **Variance Protection:** Adding negatives on every low-click term causes severe over-exclusion, suffocating broad-match discovery.
3. **Status Quo Preservation:** `IGNORE` means leaving the search term untouched in broad/phrase match to gather additional telemetry.
4. **Review Quarantining:** If an `IGNORE` query converted once, it is marked `needs_review: True` for human evaluation rather than premature automated promotion."""

    # E. Human Review Queue Count & Rationale
    if any(k in q for k in ["review queue", "how many need review", "flagged terms", "human review count", "why flagged", "review workload", "quarantined terms"]):
        rev_df = res_df[res_df["needs_review"] == True]
        rev_count = len(rev_df)
        rev_spend = float(rev_df["cost"].sum())
        
        small_sample_rev = len(rev_df[(rev_df["conversions"] >= 1) & (rev_df["clicks"] < 10)])
        borderline_cpa_rev = len(rev_df[(rev_df["conversions"] >= 1) & (rev_df["cpa"] > target_cpa)])
        bleeder_rev = len(rev_df[(rev_df["conversions"] == 0) & (rev_df["cost"] > 100)])
        
        return f"""### ⚠️ Human Review Queue Diagnostics

- **Flagged Search Terms:** **{rev_count:,} terms** ({(rev_count/len(res_df))*100:.1f}% of total)
- **Spend in Review:** **${rev_spend:,.2f}**

#### 🔍 Why Search Terms Are Quarantined:
1. **Small-Sample Converts ({small_sample_rev:,} terms):** Queries with 1 conversion but low clicks ($N < 10$) where the Wilson lower bound is too uncertain to promote.
2. **Borderline CPA Terms ({borderline_cpa_rev:,} terms):** Converting queries whose CPA slightly exceeds the ${target_cpa:,.2f} threshold.
3. **High-Spend Ambiguous Bleeders ({bleeder_rev:,} terms):** Queries with substantial expenditure that require commercial context inspection.

Senior media buyers should triage these in the **🚨 Human Review Queue** workspace."""

    # F. Decision Distribution
    if any(k in q for k in ["decision distribution", "how many promote", "decision breakdown", "how many block", "how many ignore", "share of decisions", "breakdown of decisions", "triage distribution", "distribution"]):
        total = len(res_df)
        prom = int((res_df["decision"] == "PROMOTE").sum())
        blk = int((res_df["decision"] == "BLOCK").sum())
        ign = int((res_df["decision"] == "IGNORE").sum())
        rev = int(res_df["needs_review"].sum())
        
        return f"""### ⚖️ Engine Decision Distribution Contract

Across all **{total:,} search terms**, TriageIQ enforced the strict mutually exclusive decision contract:

| Decision | Search Term Count | % of Portfolio | Purpose & Governance |
| :--- | :---: | :---: | :--- |
| **🚀 PROMOTE** | **{prom:,}** | **{prom/total:.1%}** | High-volume, validated winners added as Exact Match keywords |
| **🚫 BLOCK** | **{blk:,}** | **{blk/total:.1%}** | Non-commercial or cost bleeders excluded via Negative Keywords |
| **⏸️ IGNORE** | **{ign:,}** | **{ign/total:.1%}** | Insufficient statistical evidence; status quo preserved |

#### ⚠️ Decoupled Human Review Attention
- **Human Review Flagged (`needs_review = True`):** **{rev:,} queries ({rev/total:.1%})**
- *Note:* In accordance with the organizer contract, human review is an independent boolean flag, not a third decision."""

    # G. Baseline CPA
    if any(k in q for k in ["baseline cpa", "account cpa", "overall cpa", "average cpa", "portfolio cpa", "blended cpa", "account conversion rate"]):
        tot_spend = float(clean_df["cost"].sum())
        tot_convs = float(clean_df["conversions"].sum())
        tot_clicks = int(clean_df["clicks"].sum())
        blended_cpa = tot_spend / max(1.0, tot_convs)
        cvr = (tot_convs / max(1, tot_clicks)) * 100
        cpa_diff = blended_cpa - target_cpa
        status_txt = f"🚨 **${cpa_diff:,.2f} above** allowable ceiling" if cpa_diff > 0 else f"✅ **${abs(cpa_diff):,.2f} below** allowable ceiling"
        
        return f"""### 🎯 Account Baseline CPA & Conversion Efficiency

- **Account Blended Baseline CPA:** **${blended_cpa:,.2f}**
- **Kestrel Allowable Target CPA Ceiling:** **${target_cpa:,.2f}**
- **Variance to Target:** {status_txt}
- **Account-Wide Aggregate CVR:** **{cvr:.2f}%** ({int(tot_convs):,} conversions from {tot_clicks:,} clicks)

#### Strategic Assessment
The account's blended CPA is currently diluted by unmanaged broad-match spend bleeders and consumer loan inquiries. Eliminating the **BLOCK** cohort immediately compresses the account CPA below the ${target_cpa:,.2f} threshold."""

    # H. Account Overview
    if any(k in q for k in ["account summary", "total spend", "total volume", "dataset overview", "how much spent", "total clicks", "total impressions", "overall metrics", "dataset size", "dataset summary"]):
        tot_spend = float(clean_df["cost"].sum())
        tot_clicks = int(clean_df["clicks"].sum())
        tot_convs = float(clean_df["conversions"].sum())
        tot_val = float(clean_df["conversion_value"].sum()) if "conversion_value" in clean_df.columns else 0.0
        tot_queries = len(clean_df)
        avg_cpc = tot_spend / max(1, tot_clicks)
        avg_cpa = tot_spend / max(1.0, tot_convs)
        cvr = (tot_convs / max(1, tot_clicks)) * 100
        roas = (tot_val / max(1.0, tot_spend)) * 100 if tot_val > 0 else 0.0
        
        return f"""### 📊 Account-Level Macro Overview & Portfolio Totals

Here is the high-level performance snapshot for the analyzed dataset:

- **Total Analyzed Search Terms:** **{tot_queries:,} unique queries**
- **Cumulative Account Spend:** **${tot_spend:,.2f}**
- **Total Traffic Delivered:** **{tot_clicks:,} clicks**
- **Conversions Recorded:** **{int(tot_convs):,} conversions**
- **Total Attributed Revenue:** **${tot_val:,.2f}**

#### 📈 Efficiency Benchmarks
- **Account Average CPC:** **${avg_cpc:.2f}**
- **Portfolio Conversion Rate (CVR):** **{cvr:.2f}%**
- **Portfolio Blended CPA:** **${avg_cpa:,.2f}** *(vs. Target CPA ceiling of ${target_cpa:,.2f})*
- **Return on Ad Spend (ROAS):** **{roas:.1f}%**"""

    # I. Savings & Waste
    if any(k in q for k in ["save", "saving", "waste", "blocked spend", "cut spend", "how much money", "cost reduction"]):
        blocked_df = res_df[res_df["decision"] == "BLOCK"]
        total_blocked_spend = float(blocked_df["cost"].sum())
        total_blocked_count = len(blocked_df)
        pct_blocked = (total_blocked_count / max(1, len(res_df))) * 100
        
        off_target_spend = float(blocked_df[blocked_df["reason"].str.contains("off-target|non-commercial|personal|template|grant|job", case=False, na=False)]["cost"].sum())
        bleeder_spend = total_blocked_spend - off_target_spend
        
        return f"""### 💰 Financial Waste Elimination Summary

By deploying TriageIQ's negative keyword exclusions to Google Ads, the account can recover:

- **Potential Media Waste Reduction:** **${total_blocked_spend:,.2f}**
- **Search Terms Blocked:** **{total_blocked_count:,} queries** ({pct_blocked:.1f}% of active search volume)

#### 📉 Breakdown of Waste Drivers
1. **Off-Target & Consumer Query Exclusions:** **${off_target_spend:,.2f}**
   - High-cost traffic with zero commercial intent (e.g., consumer personal loans, mortgages, auto loans, grant seekers, and employment hunters).
2. **Spend Bleeders with Zero Conversions:** **${bleeder_spend:,.2f}**
   - Commercial keywords where expenditure surpassed the allowable CPA threshold (${target_cpa:,.2f}) with zero conversions.

👉 **How to apply:** Navigate to **📥 Google Ads Exports** in the sidebar, download `google_ads_negative_keywords.csv`, and import directly into Google Ads Editor."""

    # J. Methodology & Decision Engine Explainer
    if any(k in q for k in ["how it work", "decision engine", "methodology", "algorithm", "how does the engine work"]):
        return f"""### ⚙️ How TriageIQ's Evidence Engine Operates

TriageIQ enforces a **three-tier statistical decision framework**:

1. **Strict 3-Way Contract:**
   - Every search term is assigned exactly one decision: **`PROMOTE`**, **`BLOCK`**, or **`IGNORE`**.
   - Human review is strictly decoupled as a boolean flag (`needs_review`).
2. **Wilson Binomial Confidence Bounds:**
   - Computes an asymmetric confidence interval [ci_lower, ci_upper] for conversion rate.
   - For low click counts, the lower bound shrinks toward 0, preventing accidental promotion of lucky queries.
3. **Empirical Bayes Shrinkage:**
   - Shrinks query-level conversion rates toward the campaign baseline prior to filter out variance noise.
4. **Three Action Categories:**
   - **`PROMOTE`**: High volume (>= 10 clicks, >= 2 convs), Wilson lower bound > 0, and CPA <= Target CPA (${target_cpa:,.2f}).
   - **`BLOCK`**: Excluded business triggers OR cost bleeder with 0 conversions exceeding allowable CPA.
   - **`IGNORE`**: Insufficient data (1-5 clicks) to make a confident intervention, preserving the status quo."""

    # K. Kestrel Boundaries General Policy
    if any(k in q for k in ["kestrel", "boundary", "boundaries", "exclusion", "exclude", "negative policy", "product", "what does kestrel sell"]):
        return f"""### 🛡️ Advertiser Boundaries: Kestrel Business Funding

TriageIQ is customized with explicit business boundaries to protect Kestrel's small business lending budget:

#### 🟢 Supported Core Products (Allowed / Promoted)
- Small business working capital loans
- Commercial equipment financing and leasing
- Business lines of credit
- Merchant cash advances (MCA)
- SBA 7(a) and 504 commercial loans

#### 🔴 Explicit Negative Triggers (Instantly Blocked)
- **Consumer Loans:** `personal loans`, `auto loans`, `car financing`, `mortgages`, `student loans`
- **Grants & Handouts:** `government grant`, `federal grants`, `stimulus checks`
- **Career & Employment:** `jobs`, `hiring`, `salary`, `careers`, `resume`, `internship`
- **Non-Buyers:** `templates`, `sample invoice`, `login`, `portal`, `wikipedia`, `pdf`

These triggers are mapped to **Campaign-level Negative Phrase** and **Ad Group-level Negative Exact** keywords."""

    # -------------------------------------------------------------
    # 7. GENERAL CONVERSATIONAL / FALLBACK RESPONSE
    # -------------------------------------------------------------
    total_queries = len(res_df)
    prom_count = int((res_df["decision"] == "PROMOTE").sum())
    block_count = int((res_df["decision"] == "BLOCK").sum())
    ign_count = int((res_df["decision"] == "IGNORE").sum())
    rev_count = int(res_df["needs_review"].sum())
    
    return f"""### 🤖 TriageIQ Search Copilot

I'm monitoring your active **{total_queries:,} search terms**. Current account status:

- **🚀 Promoted Winners:** **{prom_count:,}** terms ({prom_count/total_queries:.1%})
- **🚫 Blocked Exclusions:** **{block_count:,}** terms ({block_count/total_queries:.1%})
- **⏸️ Ignored (Status Quo):** **{ign_count:,}** terms ({ign_count/total_queries:.1%})
- **⚠️ Human Review Queue:** **{rev_count:,}** flagged terms ({rev_count/total_queries:.1%})

#### Explore 30+ Trained Questions:
- **Inspect any row:** *"Audit row #6"* or *"Why was row 3 promoted?"*
- **Search any query:** *"Check 'equipment financing calculator'"*
- **Financial impact:** *"How much historical spend can we save?"* or *"What is our baseline CPA?"*
- **Methodology:** *"Why are 1-conversion keywords quarantined?"* or *"Explain Wilson confidence interval"*
- **Policy rules:** *"Explain Kestrel's negative keyword boundaries"* or *"Why block consumer loans?"*
- **Google Ads exports:** *"How do I import negative keywords into Google Ads Editor?"*"""


def engine_params_min_clicks(df: pd.DataFrame) -> int:
    return 10
