# 🎯 TriageIQ — Evidence-First Search Intelligence (PS-01)

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![CI Tests](https://img.shields.io/badge/Unit%20Tests-66%20Passing-brightgreen?logo=github-actions&logoColor=white)](https://github.com/Rohith00755/search-term-triage-engine/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/Code%20Style-Production%20Grade-blueviolet)](#)

> **Audited, Contract-Compliant Search Term Triage Engine & Executive Intelligence Cockpit**  
> Built for Google Ads Search Term Reports with **Wilson 95% Confidence Intervals**, **Empirical Bayes Shrinkage**, **Near-Duplicate Intent Clustering**, **Context-Aware Negative Suggestions**, and an **Interactive AI Copilot with 38+ Trained PPC Diagnostic Handlers**.

---

## 🏛️ Project Architecture & Decoupled Stacks

The repository is cleanly structured into decoupled, modular stacks (**Frontend**, **Backend**, **Core Engine**, **CLI**, **Tests**, and **Exports**), ensuring maximum code clarity for hackathon judges while preserving the working execution flow and Streamlit Community Cloud deployment without downtime:

```
search-term-triage-engine/
│
├── frontend/                    # [FRONTEND STACK] Presentation, Themes & UI Components
│   ├── __init__.py              # Unified frontend package exports
│   ├── styles.py                # Enterprise Design System, CSS variables & Dark Plum styling
│   └── components.py            # Evidence-First UI cards, Wilson CI badges & reviewer actions
│
├── backend/                     # [BACKEND STACK] Decoupled Engine Facade & Public Services
│   ├── __init__.py              # Unified backend entry point & public API contract
│   ├── rules.py                 # Multi-tiered business rules & threshold matrix
│   ├── stats.py                 # Wilson Score intervals & Empirical Bayes shrinkage
│   ├── copilot.py               # AI PPC Copilot diagnostic brain (38+ intents)
│   ├── clustering.py            # Near-duplicate search-intent clustering
│   ├── negatives.py             # Context-aware negative keyword extraction & scoring
│   ├── learning.py              # Reviewer Precedent Memory & active learning
│   └── exporter.py              # Google Ads Editor CSV & audit report generator
│
├── triage_engine/               # [CORE ALGORITHMIC ENGINE] Pure statistical & business logic
│   ├── __init__.py              # Engine package initialization
│   ├── rules.py                 # Core TriageEngine logic & AdvertiserProfile configuration
│   ├── stats.py                 # Closed-form binomial Wilson bounds & Bayes prior
│   ├── copilot.py               # 38+ specialized query intents with mathematical grounding
│   ├── clustering.py            # TF-IDF & character n-gram intent grouping
│   ├── negatives.py             # N-gram token waste scoring & collision risk detection
│   ├── learning.py              # Levenshtein distance & precedent correction memory
│   └── exporter.py              # Google Ads Editor CSV formatting
│
├── tests/                       # [TEST STACK] 66 automated unit tests (<0.05s execution)
│   ├── test_architecture.py    # Stack decoupling & backward compatibility verification
│   ├── test_triage.py           # Core triage engine & Wilson bounds verification
│   ├── test_copilot.py          # AI Copilot audit reasoning & intent verification
│   ├── test_copilot_30q.py      # Verification of 38+ specialized PPC query handlers
│   └── test_enhancements.py     # Intent clustering, precedents & negative scoping
│
├── data/                        # Benchmark and input search-term reports
│   ├── production_search_terms_25k.csv   # Canonical 25,000-term Kestrel production dataset
│   └── search_terms_25k.csv              # Synthetic test search-term report
│
├── output/                      # Canonical contract-compliant Google Ads exports
│   ├── full_triage_audit.csv             # 100% complete audit log with Wilson bounds & rationale
│   ├── google_ads_promoted_keywords.csv  # 1-Click Exact Match keyword upload for Google Ads Editor
│   ├── google_ads_negative_keywords.csv  # 1-Click Campaign/Ad Group negative exclusions
│   ├── human_review_queue.csv            # Quarantined ambiguous & small-sample queries
│   ├── negative_keyword_suggestions.csv  # Candidate exclusions with collision risk flags
│   └── reviewer_corrections_log.csv      # Audit trail of analyst overrides & precedents
│
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI test runner (executes all 66 unit tests)
│
├── app.py                       # Cloud Web UI entry point & orchestrator (Streamlit Cloud compatible)
├── run_cli.py                   # High-performance batch CLI pipeline for enterprise runs
├── generate_dataset.py          # Synthetic search-term report generator
├── requirements.txt             # Minimal production dependencies (wheel-only, 0 compiler issues)
├── .python-version              # Python 3.11 runtime specification
├── run_app.bat                  # 1-click Windows batch launcher
├── run_app.ps1                  # 1-click PowerShell launcher
└── README.md                    # Executive and technical documentation
```

---

## 📋 1. Organizer Output Contract Compliance

Every input search-term record is assigned **strictly one** of the three mandated primary decisions:
* **`PROMOTE`**: Statistically validated winners meeting interaction volume criteria, profitable CPA ceiling, and narrow Wilson intervals.
* **`BLOCK`**: Excluded queries violating advertiser business scope (e.g., consumer loans, car financing, mortgages, student loans, grants, jobs) or sustained spend bleeders.
* **`IGNORE`**: Dormant long-tail terms preserved without cluttering account limits, or terms with insufficient evidence to intervene.

### Decoupled Human Review Handling (`needs_review`)
Human review is strictly decoupled as an independent boolean flag (**`needs_review`**):
* When sample size is underpowered (e.g. 1 click, 1 conversion) or signals conflict, the row receives **`decision = "IGNORE"`** and **`needs_review = True`**.
* **Why this design?** Human Review is an operational state of management attention, not an execution status in Google Ads Editor. A keyword in Google Ads is either added as an exact match (`PROMOTE`), excluded (`BLOCK`), or left alone in broad match (`IGNORE`).
* The complete audit CSV (`full_triage_audit.csv`) contains **100% of input rows** (exactly 25,000 rows for the official dataset) with complete evidence cards, confidence intervals, and audit trails.

---

## 📐 2. The Statistical Evidence Framework & Variance Trap

### The Trap: 1 Click, 1 Conversion (`apply business loan approval`)
* **Observed CVR**: $100\%$ ($1 / 1$)
* **Nominal CPA**: $\$12.50$ (Appears wildly profitable)
* **Wilson 95% Confidence Interval**: $[20.6\%, 100.0\%]$ (Width: $79.4\%$)
* **Why Wilson Lower Bound $> 1.5\%$ Alone Fails**: At $n=1$, the Wilson lower bound is $20.6\% > 1.5\%$. Relying purely on lower bound thresholding would erroneously promote this lucky anomaly, risking thousands of dollars in budget.
* **TriageIQ Multi-Gate Evidence Policy**:
  1. **Evidence Prerequisite**: Clicks $\ge 10$ and Conversions $\ge 2$.
  2. **Interval Quality**: Wilson 95% interval width $\le 40\%$.
  3. **Economic Ceiling**: CPA $\le \text{Target CPA} (\$220.00)$.
  4. **Intent Alignment**: Query must align with B2B commercial loan offerings.
* **Result**: Safely quarantined to `IGNORE` with `needs_review = True`, `confidence = "MEDIUM"`, and an explicit statistical rationale citing sample variance.

---

## 🏢 3. Advertiser Business Boundaries (Kestrel Business Funding)

Configurable `AdvertiserProfile` encapsulates business boundaries:
* **Supported Commercial Products**: Working capital loans, commercial equipment financing and leasing, business lines of credit, merchant cash advances (MCA), SBA 7(a) and 504 loans.
* **Explicit Negative Triggers**:
  - *Consumer Loans:* `personal loans`, `auto loans`, `car financing`, `mortgages`, `student loans`
  - *Grants & Handouts:* `government grant`, `federal grants`, `stimulus checks`
  - *Career & Employment:* `jobs`, `hiring`, `salary`, `careers`, `resume`, `internship`
  - *Non-Buyers:* `templates`, `sample invoice`, `login`, `portal`, `wikipedia`, `pdf`
* **Narrowest Appropriate Scope Rule**:
  - Universal off-target themes are blocked at the **Campaign level** as **Negative Phrase**.
  - Product-specific bleeders are excluded at the **Ad Group level** as **Negative Exact** to prevent cross-ad-group damage.

---

## 🤖 4. AI Search Copilot (38+ Specialized PPC Handlers)

The application includes an integrated **Conversational AI Search Copilot** trained on 38+ distinct search-term diagnostic questions:

| Category | Handled Queries & Diagnostics |
| :--- | :--- |
| **📊 Financial & ROI** | Macro account overview, potential spend waste elimination, account baseline CPA vs. Target CPA, portfolio decision distributions, zero-conversion waste aggregates. |
| **🔬 Statistical Rigor** | Small-sample variance trap breakdown, Wilson Score binomial interval formula, Empirical Bayes shrinkage, 3-way decision contract specification. |
| **🛡️ Advertiser Policies** | Kestrel Target CPA ceiling ($220), commercial loan products, consumer loan exclusions, grant/stimulus policies, employment exclusions, non-buyer queries. |
| **🚀 Winners & Bleeders** | Top 5 promoted exact-match candidates, top 5 spend bleeders, most efficient campaigns, least efficient campaigns, low-CTR diagnostics. |
| **⚙️ Match Types & Bids** | Broad vs. Exact performance comparison, internal keyword cannibalization, suggested Max CPC bidding formula, narrowest scope rule, over-exclusion collision risks. |
| **📥 Exports & Learning** | Google Ads Editor CSV formatting, step-by-step Editor import guide, near-duplicate intent clustering, cluster decision conflicts, session precedent learning. |

---

## 📊 5. Verification & Benchmark on Production Dataset (25k Search Terms)

Evaluated against the 25,000-row Kestrel Business Funding production report (`search_terms_report.csv`) in **1.28 seconds**:

| Metric | Production Benchmark Value | Description |
| :--- | :---: | :--- |
| **Total Ingested Rows** | **25,000** | 100% input preservation (zero dropped/duplicated rows) |
| **`PROMOTE` Decisions** | **1,179 (4.7%)** | Statistically verified exact match candidates |
| **`BLOCK` Decisions** | **5,267 (21.1%)** | Excluded off-target queries and sustained bleeders |
| **`IGNORE` Decisions** | **18,554 (74.2%)** | Dormant long-tail and unproven traffic (status quo) |
| **`needs_review = True`** | **4,155 (16.6%)** | Underpowered conversions, borderline spend, and conflicts |
| **Historical Spend on Blocked Terms** | **$372,126.02** | Potential future media waste reduction |
| **Attributed Conversion Value** | **$18,673,641.00** | Across 8,521 tracked commercial loan applications |
| **Intent Clusters** | **16,775 clusters** | 6,219 multi-variant clusters consolidated |

---

## 🧪 6. Automated Unit Tests (66/66 Passing)

All **66 unit tests** execute in **0.045 seconds**:
```bash
python -m unittest discover tests -v
```

### Test Suite Breakdown:
1. **`tests/test_architecture.py` (3 tests)**: Verifies decoupled frontend/backend import boundaries, design system exports, and 100% backward compatibility.
2. **`tests/test_triage.py` (11 tests)**: Wilson confidence intervals, small-sample guardrails, advertiser business policy enforcement, numerical boundary edge cases, output contract field validity.
3. **`tests/test_copilot.py` (8 tests)**: Row audit lookups, natural language query searches, savings calculations, variance trap explanations, Kestrel boundaries, top winners.
4. **`tests/test_copilot_30q.py` (38 tests)**: End-to-end verification of all 38 specialized PPC diagnostic queries, intent routing order, and mathematical grounding.
5. **`tests/test_enhancements.py` (6 tests)**: Near-duplicate clustering, qualifier preservation, decision conflict detection, reviewer precedent memory, negative keyword suggestion scoring.

---

## 🖥️ 7. Quickstart & How to Run

### Prerequisites
* Python 3.10 or 3.11
* Dependencies: `streamlit`, `pandas`, `numpy`, `altair`, `pyarrow`

```bash
# Clone the repository
git clone https://github.com/Rohith00755/search-term-triage-engine.git
cd search-term-triage-engine

# Install dependencies (fast binary wheels, zero compilers required)
pip install -r requirements.txt
```

### Launch the Streamlit Intelligence Console
```bash
python -m streamlit run app.py
```
*(On Windows, you can also simply double-click `run_app.bat` or run `./run_app.ps1`)*

### Run the High-Performance Batch CLI
```bash
python run_cli.py --input "data/production_search_terms_25k.csv" --output-dir "output"
```

---

## 👥 Authors & Team
- **Team:** Team 14 — Vertex Vision
- **Challenge:** PS-01 Search Term Triage Engine (Srishti 2K26)
- **Repository:** [https://github.com/Rohith00755/search-term-triage-engine](https://github.com/Rohith00755/search-term-triage-engine)
