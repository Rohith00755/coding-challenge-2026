# SearchPilot AI — Intelligent Google Ads Search Term Triage Engine

**SearchPilot AI** is a modern, enterprise-grade SaaS web platform built to help digital marketing teams triage thousands of Google Ads search terms into three explainable actions:

- 🟢 **PROMOTE**: Recommend adding a relevant, high-potential search term as a deliberate target keyword (Exact/Phrase match).
- 🔴 **BLOCK**: Recommend excluding an irrelevant or clearly unwanted search term using a negative keyword.
- 🟡 **IGNORE**: Keep monitoring the search term because the evidence is insufficient for a reliable decision.

---

## 🌟 Key Highlights & Philosophy

1. **Statistical Uncertainty First**:
   - Computes the **Wilson Score 95% confidence lower bound** on conversion rate (CVR).
   - **Mitigates the Single-Conversion Trap**: Never automatically promotes a search term just because it recorded 1 click and 1 conversion (100% naive CVR). Low click volume has high volatility and is routed to human review.
   - Low conversion count alone **never** justifies blocking a relevant term.

2. **Explainable AI**:
   - Every recommendation is accompanied by a confidence percentage (80-100% High, 60-79% Medium, <60% Low), human-readable rationale, factor breakdown, and missing data alerts.

3. **Human-in-the-Loop Review Center**:
   - Dedicated review workbench for analysts to approve, override, add contextual notes, and inspect a full session audit trail.

4. **Negative Keyword Studio with Collision Checking**:
   - Auto-formats negative keywords as Phrase (`"query"`) or Exact (`[query]`).
   - Automatically cross-references proposed negative phrases against converting queries to prevent accidental exclusion of high-value traffic.
   - 1-click export formatted for Google Ads Editor.

5. **25,000-Row Vectorized Performance**:
   - High-throughput Pandas pipeline capable of triaging 25,000 rows in under 2 seconds.

6. **Robust CSV Import**:
   - Reads real Google Ads exports as-is: title/date rows above the header, UTF-8/UTF-16/Windows-1252, comma/tab/semicolon delimiters, `$1,234.50` / `12%` / `--` / `< 10` values, and `Total:` rows. Missing columns are filled with safe defaults and flagged with a warning.

---

## 🏗️ Architecture & Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons.
- **Backend**: Python 3.12, FastAPI, Pandas, Scikit-learn, Pydantic, SQLite (`searchpilot.db`).
- **Statistical Engine**: Wilson score lower bounds, Bayesian sample size shrinkage, TF-IDF n-gram token overlap, intent lexicons.

---

## 🚀 Quick Start (single address)

SearchPilot AI runs on **one address**: the backend serves both the API and the web app.

**Easiest:** double-click `setup_and_run.bat`. It installs everything, builds the web app, starts the server and opens **http://localhost:8000**.

**Manual:**

```bash
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt

cd ..\frontend
npm.cmd install
npm.cmd run build

cd ..\backend
.\venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open **http://localhost:8000** (API docs at `http://localhost:8000/docs`).

Next time, just run `run_backend.bat`. (`run_frontend.bat` is a developer-only hot-reload mode on port 3000.)

---

## 💻 Run in VS Code

1. **File > Open Folder...** and choose the `searchpilot-ai` folder. Accept the "install recommended extensions" prompt.
2. Press **Ctrl+Shift+B** (runs "Setup everything and run"): installs the backend, builds the web app, starts the server.
3. Open **http://localhost:8000**.

Next time: **Terminal > Run Task > 3. Run SearchPilot AI**, or press **F5** to run with the debugger.

---

## 🧪 Automated Testing & Benchmarks

Run the test suite:

```bash
cd backend
.\venv\Scripts\python test_suite.py
```

Tests verify:
- Single-conversion trap avoidance ($N=1, Conv=1 \to$ IGNORE / Review).
- Irrelevant intent detection ($Cost>0, Negative Intent \to$ BLOCK).
- High performer targeting ($Conv\ge 2, Strong ROAS \to$ PROMOTE).
- Benchmark: 25,000 rows triaged in sub-2 seconds.

---
