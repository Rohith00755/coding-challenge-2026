from __future__ import annotations

import io
import html
import pandas as pd
import streamlit as st

from triage import REQUIRED, analyze, normalize_columns

st.set_page_config(page_title="Search Term Triage", page_icon="🔎", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
:root { color-scheme: dark !important; --paper:#090a09; --ink:#f2f2ef; --muted:#a1a29d; --line:#30312e; --white:#111210; --lime:#e04445; --text-color:#f2f2ef; --background-color:#090a09; --secondary-background-color:#111210; --primary-color:#e04445; }
html, body, [class*="css"] { font-family:'DM Sans',Arial,sans-serif; color:var(--ink); }
.stApp, [data-testid="stAppViewContainer"] { background:var(--paper); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(9,10,9,.96); }
[data-testid="stMainBlockContainer"] { max-width:1500px; padding:1.5rem 3.2rem 4rem; }
[data-testid="stSidebar"] { background:#111210; border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child { padding-top:1.8rem; }
.stApp, [data-testid="stAppViewContainer"] { --text-color:#f2f2ef; --background-color:#090a09; --secondary-background-color:#111210; --primary-color:#e04445; }
[data-testid="stSidebar"] h2 { font:700 11px 'DM Sans',Arial,sans-serif; letter-spacing:.16em; text-transform:uppercase; color:#b4b5ae; }
.lux-hero { display:grid; grid-template-columns:1.05fr .95fr; align-items:center; gap:36px; margin:8px 0 40px; animation:riseIn .85s cubic-bezier(.2,.7,.2,1) both; }
.hero-copy { padding:18px 0 12px; }
.page-kicker { display:flex; align-items:center; gap:10px; color:#b4b5ae; font-size:10px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; margin-bottom:23px; }
.page-kicker i { width:8px; height:8px; border-radius:50%; background:var(--lime); box-shadow:0 0 18px rgba(224,68,69,.55); }
.lux-hero h1 { color:var(--ink); font:400 clamp(48px,6.1vw,82px)/.92 'DM Serif Display',Georgia,serif; letter-spacing:-.045em; margin:0; }
.lux-hero h1 em { color:#e04445; font-weight:400; }
.lux-hero p { max-width:420px; color:#b4b5ae; font-size:14px; line-height:1.8; margin:22px 0 26px; }
.hero-foot { display:flex; gap:24px; border-top:1px solid #3a3b36; padding-top:14px; color:#95968f; font-size:9px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
.hero-foot span:first-child { color:#f2f2ef; }
.signal-visual { position:relative; min-height:350px; overflow:hidden; padding:24px; border:1px solid #30312e; background:radial-gradient(ellipse at 78% 24%,#351d1e 0,transparent 42%),linear-gradient(145deg,#171515,#0d0e0d 72%); animation:riseIn .9s .12s both; }
.signal-visual:before { content:''; position:absolute; inset:0; opacity:.2; background-image:linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(135deg,#000,transparent 78%); }
.signal-top,.signal-heading,.signal-bars,.signal-examples,.visual-foot { position:relative; z-index:1; }
.signal-top { display:flex; justify-content:space-between; align-items:center; color:#a1a29d; font-size:9px; font-weight:700; letter-spacing:.17em; }
.signal-status { display:flex; align-items:center; gap:7px; color:#f07171; }
.signal-status i { width:6px; height:6px; border-radius:50%; background:#e04445; box-shadow:0 0 12px #e04445; animation:pulse 1.8s ease-in-out infinite; }
.signal-heading { margin-top:42px; padding-right:82px; display:flex; justify-content:space-between; align-items:end; gap:12px; }
.signal-heading span { color:#aaa; font-size:10px; letter-spacing:.13em; }
.signal-heading strong { color:#f2f2ef; font:italic 23px 'DM Serif Display',Georgia,serif; }
.signal-bars { height:112px; display:flex; align-items:end; gap:7px; padding:12px 3px 0; border-bottom:1px solid #4a4b46; background:repeating-linear-gradient(to bottom,transparent 0,transparent 26px,rgba(255,255,255,.08) 27px); }
.signal-bars i { flex:1; min-width:4px; height:var(--bar); background:linear-gradient(0deg,rgba(224,68,69,.18),#e04445); transform-origin:bottom; animation:barRise .8s cubic-bezier(.2,.7,.2,1) both; animation-delay:calc(var(--n)*45ms); opacity:.86; }
.signal-bars i:nth-child(3n) { background:linear-gradient(0deg,rgba(224,68,69,.08),#92948a); opacity:.58; }
.signal-examples { display:grid; grid-template-columns:repeat(3,1fr); gap:9px; margin-top:18px; }
.signal-example { padding:10px 9px; border:1px solid #353631; background:rgba(8,9,8,.58); }
.signal-example small { display:block; color:#8e9088; font-size:8px; letter-spacing:.1em; text-transform:uppercase; }
.signal-example b { display:block; margin-top:5px; color:#e5e6df; font-size:10px; font-weight:600; }
.signal-example em { color:var(--lime); font-style:normal; }
.visual-foot { position:absolute; left:24px; bottom:14px; color:#95968f; font-size:8px; font-weight:700; letter-spacing:.16em; }
.roundel { position:absolute; z-index:2; right:18px; top:44px; width:78px; height:78px; display:grid; place-content:center; text-align:center; border-radius:50%; background:var(--lime); color:#fff; font-size:7px; font-weight:700; line-height:1.45; letter-spacing:.12em; transform:rotate(8deg); animation:floatIn 1s .35s both; }
.roundel strong { display:block; font:italic 20px 'DM Serif Display',Georgia,serif; letter-spacing:-.04em; }
.section-kicker { color:#a1a29d; font-size:10px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; margin:0 0 2px; }
.insight-band { display:grid; grid-template-columns:.8fr 1.2fr; height:150px; min-height:0; margin:0 0 35px; border:1px solid #30312e; background:#111210; overflow:hidden; animation:riseIn .7s .18s both; }
.insight-quote { display:flex; flex-direction:column; justify-content:center; padding:24px 30px; border-left:3px solid #e04445; }
.insight-quote blockquote { margin:0; color:#f2f2ef; font:italic 25px/1.16 'DM Serif Display',Georgia,serif; }
.insight-quote small { margin-top:16px; color:#a1a29d; font-size:8px; font-weight:700; letter-spacing:.17em; text-transform:uppercase; }
.insight-photo { position:relative; height:150px; min-height:0; overflow:hidden; }
.insight-photo img { width:100%; height:150px; min-height:0; object-fit:cover; display:block; filter:brightness(.62) saturate(.7); transition:transform .8s ease,filter .4s ease; }
.insight-photo:hover img { transform:scale(1.035); filter:brightness(.8) saturate(.9); }
.insight-photo:after { content:''; position:absolute; inset:0; background:linear-gradient(90deg,#111210,rgba(17,18,16,.05) 70%),linear-gradient(0deg,rgba(0,0,0,.45),transparent 35%); pointer-events:none; }
.photo-credit { position:absolute; z-index:1; right:10px; bottom:8px; color:#e5e6df; font-size:8px; letter-spacing:.04em; text-shadow:0 1px 5px #000; }
.photo-credit a { color:inherit; text-decoration:underline; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color:#343531 !important; background:linear-gradient(130deg,rgba(255,255,255,.025),rgba(255,255,255,.008)) !important; transition:border-color .22s ease,transform .22s ease; }
[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color:#6b3435 !important; }
.review-card-title { font:italic 23px/1.15 'DM Serif Display',Georgia,serif; color:#f2f2ef; margin:0 0 6px; overflow-wrap:anywhere; }
.review-card-reason { color:#b4b5ae; font-size:12px; line-height:1.65; }
.review-card-meta { color:#9d9e97; font-size:9px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }
.review-stats { display:flex; flex-wrap:wrap; gap:7px; margin-top:14px; }
.review-stats span { min-width:78px; padding:7px 9px; border:1px solid #30312e; background:rgba(0,0,0,.16); }
.review-stats small,.review-stats b { display:block; }
.review-stats small { color:#92938d; font-size:8px; text-transform:uppercase; letter-spacing:.1em; }
.review-stats b { margin-top:4px; color:#f2f2ef; font-size:12px; font-weight:600; }
.review-card-chip { display:inline-block; margin:8px 0; padding:5px 8px; color:#f07171; border:1px solid rgba(224,68,69,.4); background:rgba(224,68,69,.09); font-size:8px; font-weight:700; letter-spacing:.13em; }
[data-testid="stNumberInput"] input { background:#151613; border-color:#4a4b46; color:#f2f2ef; }
@media(max-width:680px) { .insight-band { grid-template-columns:1fr; height:auto; } .insight-quote { min-height:112px; padding:17px 20px; } .insight-quote blockquote { font-size:21px; } .insight-photo { height:112px; min-height:0; } .insight-photo img { height:112px; min-height:0; } .insight-photo:after { background:linear-gradient(0deg,rgba(0,0,0,.45),transparent 55%); } }
[data-testid="stMetric"] { border-top:1px solid #444540; padding:15px 12px 10px 0; background:linear-gradient(135deg,rgba(255,255,255,.035),transparent 72%); transition:transform .25s ease,border-color .25s ease; animation:riseIn .65s both; }
[data-testid="stMetric"]:hover { transform:translateY(-3px); border-color:var(--lime); }
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] { animation-delay:.06s; }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] { animation-delay:.12s; }
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] { animation-delay:.18s; }
[data-testid="stHorizontalBlock"] > div:nth-child(5) [data-testid="stMetric"] { animation-delay:.24s; }
[data-testid="stMetricLabel"] { color:#b4b5ae; font-size:10px; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }
[data-testid="stMetricValue"] { color:var(--ink); font:600 clamp(23px,3vw,34px) 'DM Sans',Arial,sans-serif; letter-spacing:-.04em; }
[data-testid="stMetricDelta"] { color:#b4b5ae; }
[data-testid="stAlert"], [data-testid="stAlert"] *, [data-testid="stAlert"] [role="alert"] { background:#171815 !important; background-image:none !important; border-color:#3c3d39 !important; color:#f2f2ef !important; }
[data-testid="stAlert"] { border-left:3px solid var(--lime) !important; border-radius:2px; }
[data-testid="stTabs"] [role="tablist"] { gap:27px; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] [role="tab"] { color:#a1a29d !important; font-size:12px; padding:12px 0; transition:color .2s ease; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color:var(--ink) !important; border-bottom:2px solid var(--lime) !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #30312e; border-radius:2px; background:#111210; }
button[kind="primary"], [data-testid="stDownloadButton"] button { background:var(--lime); color:#fff; border:1px solid var(--lime); border-radius:2px; font-weight:700; transition:transform .2s ease,box-shadow .2s ease,background .2s ease; }
button[kind="primary"]:hover, [data-testid="stDownloadButton"] button:hover { background:#f15a5b; border-color:#f15a5b; color:#fff; transform:translateY(-2px); box-shadow:0 7px 22px rgba(224,68,69,.22); }
button[kind="secondary"] { color:#f2f2ef; border:1px solid #5a5b56; border-radius:2px; background:transparent; transition:border-color .2s ease,color .2s ease; }
button[kind="secondary"]:hover { border-color:var(--lime); color:var(--lime); }
[data-testid="stFileUploader"] section { background:#151613; border:1px dashed #555650; border-radius:2px; transition:border-color .2s ease,background .2s ease; }
[data-testid="stFileUploader"] section:hover { border-color:var(--lime); background:#191b16; }
[data-testid="stSelectbox"] label, [data-testid="stTextInput"] label { color:#b4b5ae; font-size:11px; font-weight:600; }
[data-testid="stSelectbox"] > div > div, [data-testid="stTextInput"] input { background:#151613; border-color:#4a4b46; border-radius:2px; color:#f2f2ef; }
[data-testid="stCaptionContainer"] { color:#a1a29d; }
[data-testid="stAppDeployButton"] { display:none; }
[data-testid="stToolbar"] { display:none; }
hr { border-color:var(--line); }
@keyframes riseIn { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
@keyframes floatIn { from { opacity:0; transform:translateY(10px) rotate(0); } to { opacity:1; transform:translateY(0) rotate(8deg); } }
@keyframes pulse { 50% { opacity:.35; box-shadow:0 0 3px #e04445; } }
@keyframes barRise { from { transform:scaleY(.08); opacity:.2; } to { transform:scaleY(1); opacity:.86; } }
@media(prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; scroll-behavior:auto !important; transition-duration:.01ms !important; } }
@media(max-width:800px) {
  [data-testid="stMainBlockContainer"] { padding:1rem 1.1rem 3rem; }
  .lux-hero { grid-template-columns:1fr; gap:22px; margin:0 0 30px; }
  .hero-copy { padding-top:12px; }
  .lux-hero h1 { font-size:clamp(50px,13vw,78px); }
  .signal-visual { min-height:330px; padding:18px; }
}
@media(max-width:520px) { .hero-foot { gap:13px; font-size:8px; } .signal-visual { min-height:315px; } .signal-examples { gap:5px; } .signal-example { padding:8px 6px; } .signal-example b { font-size:9px; } .roundel { width:68px;height:68px;font-size:6px;right:13px;top:37px; } .roundel strong { font-size:15px; } }
</style>
<div class="lux-hero"><div class="hero-copy"><div class="page-kicker"><i></i> Search intelligence · Google Ads</div><h1>Every query<br>has a <em>signal.</em></h1><p>Find the terms worth scaling, the spend worth stopping, and the thin evidence that deserves a human decision.</p><div class="hero-foot"><span>01 / SEARCH INTELLIGENCE</span><span>BUILT FOR 25K+ ROWS</span></div></div><div class="signal-visual"><div class="signal-top"><span>QUERY SIGNAL MAP</span><span class="signal-status"><i></i> READY TO ANALYZE</span></div><div class="signal-heading"><span>ILLUSTRATIVE SEARCH PATTERNS</span><strong>Intent, decoded.</strong></div><div class="signal-bars" aria-hidden="true"><i style="--bar:28%;--n:1"></i><i style="--bar:43%;--n:2"></i><i style="--bar:35%;--n:3"></i><i style="--bar:57%;--n:4"></i><i style="--bar:49%;--n:5"></i><i style="--bar:71%;--n:6"></i><i style="--bar:62%;--n:7"></i><i style="--bar:84%;--n:8"></i><i style="--bar:67%;--n:9"></i><i style="--bar:92%;--n:10"></i><i style="--bar:76%;--n:11"></i><i style="--bar:100%;--n:12"></i><i style="--bar:79%;--n:13"></i><i style="--bar:89%;--n:14"></i><i style="--bar:68%;--n:15"></i><i style="--bar:96%;--n:16"></i><i style="--bar:72%;--n:17"></i><i style="--bar:87%;--n:18"></i><i style="--bar:64%;--n:19"></i><i style="--bar:80%;--n:20"></i></div><div class="signal-examples"><div class="signal-example"><small>Strong intent</small><b><em>Promote</em> · explain</b></div><div class="signal-example"><small>Thin evidence</small><b><em>Review</em> · abstain</b></div><div class="signal-example"><small>Waste pattern</small><b><em>Block</em> · protect</b></div></div><div class="roundel">BUILT FOR<br><strong>BETTER</strong><br>DECISIONS</div><div class="visual-foot">ILLUSTRATIVE SIGNALS · NOT ACCOUNT DATA</div></div></div>
<div class="insight-band"><div class="insight-quote"><blockquote>“A conversion is a clue, never a verdict.”</blockquote><small>THE TRIAGE PRINCIPLE · EVIDENCE FIRST</small></div><div class="insight-photo"><img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1100&q=85" alt="Laptop displaying a marketing analytics dashboard"><span class="photo-credit">Photo by <a href="https://unsplash.com/@kmuza" target="_blank" rel="noopener">Carlos Muza</a> on Unsplash</span></div></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("01 / Upload data")
    uploaded = st.file_uploader("Google Ads search terms CSV", type=["csv"])
    st.caption("Required: search term, clicks, impressions, cost, conversions. Standard Google Ads and snake_case headers (search_term, match_type, conversion_value) are supported; campaign and ad group are retained for targeting.")

# Clear data left by the removed generated-demo workflow when this version is first loaded.
if st.session_state.get("_dataset_policy_version") != 1:
    st.session_state.result = None
    st.session_state["_dataset_policy_version"] = 1
if uploaded:
    try:
        raw = pd.read_csv(uploaded, low_memory=False, encoding="utf-8-sig")
        st.session_state.result = analyze(normalize_columns(raw))
    except Exception as exc:
        st.session_state.result = None
        st.error(f"Could not read this CSV: {exc}")

if st.session_state.result is None:
    st.info("Upload one of your Google Ads search-terms CSV files to build the dashboard. No sample rows are loaded.")
    st.stop()

df = st.session_state.result.copy()
if "Human decision" not in df:
    df["Human decision"] = ""
if "Reviewer note" not in df:
    df["Reviewer note"] = ""

total_cost = df["Cost"].sum()
conversions = df["Conversions"].sum()
review_count = int((df["Decision"] == "REVIEW").sum())
m1,m2,m3,m4,m5 = st.columns([1.3,1,1,1,1.35], gap="small")
m1.metric("Search terms", f"{len(df):,}")
m2.metric("Promote", f"{(df.Decision == 'PROMOTE').sum():,}")
m3.metric("Block", f"{(df.Decision == 'BLOCK').sum():,}")
m4.metric("Review", f"{review_count:,}")
compact = lambda value: f"{value / 1000:,.1f}k" if abs(value) >= 1000 else f"{value:,.1f}"
m5.metric("Spend", compact(total_cost))
m5.caption(f"{conversions:,.1f} conversions")

if review_count:
    st.warning(f"{review_count:,} rows need human review because evidence is limited or mixed. A conversion alone never triggers promotion.")

st.markdown('<div class="section-kicker">02 &nbsp; / &nbsp; PERFORMANCE OVERVIEW</div>', unsafe_allow_html=True)
tab_review, tab_all, tab_export = st.tabs(["Review queue", "All terms", "Export"])
with tab_review:
    queue = df[df.Decision == "REVIEW"].copy()
    if queue.empty:
        st.success("No rows currently require review.")
    else:
        filter_cols = st.columns([2, 1, 1.1])
        search_text = filter_cols[0].text_input("Find a search term", placeholder="Search the review queue", key="review_search")
        confidence_filter = filter_cols[1].selectbox("Confidence", ["All", "Low", "Medium", "High"], key="review_confidence")
        page_size = 8
        if search_text:
            queue = queue[queue["Search term"].astype(str).str.contains(search_text, case=False, na=False)]
        if confidence_filter != "All":
            queue = queue[queue["Confidence"].astype(str).str.casefold() == confidence_filter.casefold()]
        page_count = max(1, (len(queue) + page_size - 1) // page_size)
        previous_page = min(max(int(st.session_state.get("review_page", 1)), 1), page_count)
        st.session_state.review_page = previous_page
        page = filter_cols[2].number_input("Page", min_value=1, max_value=page_count, step=1, key="review_page", help=f"{page_count:,} pages · {page_size} cards per page")
        st.caption(f"{len(queue):,} terms to review · Showing page {int(page):,} of {page_count:,}")
        page_rows = queue.iloc[(int(page) - 1) * page_size:int(page) * page_size]
        for _, row in page_rows.iterrows():
            row_key = str(row["_row_id"])
            with st.container(border=True):
                details, correction = st.columns([1.7, 1], gap="large")
                with details:
                    term = html.escape(str(row["Search term"]))
                    confidence = html.escape(str(row["Confidence"]))
                    reason = html.escape(str(row["Reason"]))
                    st.markdown(f'<div class="review-card-title">{term}</div><div class="review-card-chip">HUMAN REVIEW · {confidence.upper()} CONFIDENCE</div><div class="review-card-reason">{reason}</div>', unsafe_allow_html=True)
                    context = [str(row.get("Campaign", "")), str(row.get("Ad group", "")), str(row.get("Match type", ""))]
                    context = [html.escape(value) for value in context if value and value.lower() != "nan"]
                    if context:
                        st.markdown(f'<div class="review-card-meta">{" · ".join(context)}</div>', unsafe_allow_html=True)
                    stat_fields = [("Impressions", row.get("Impressions", 0)), ("Clicks", row.get("Clicks", 0)), ("Cost", row.get("Cost", 0)), ("Conversions", row.get("Conversions", 0))]
                    if "Conversion value" in row.index:
                        stat_fields.append(("Conv. value", row["Conversion value"]))
                    stats_markup = "".join(f'<span><small>{html.escape(label)}</small><b>{html.escape(f"{float(value):,.2f}" if label in ("Cost", "Conv. value") else f"{float(value):,.0f}")}</b></span>' for label, value in stat_fields)
                    st.markdown(f'<div class="review-stats">{stats_markup}</div>', unsafe_allow_html=True)
                with correction:
                    current_choice = str(row["Human decision"] or "")
                    options = ["Use recommendation", "PROMOTE", "BLOCK", "IGNORE"]
                    choice_index = options.index(current_choice) if current_choice in options else 0
                    choice = st.selectbox("Human decision", options, index=choice_index, key=f"review_choice_{row_key}")
                    note_key = f"review_note_{row_key}"
                    st.text_input("Reviewer note (optional)", value=str(row["Reviewer note"] or ""), key=note_key, placeholder="Why are you changing it?")
                    if st.button("Apply correction", key=f"save_review_{row_key}", type="primary", use_container_width=True):
                        corrected = "" if choice == "Use recommendation" else choice
                        mask = df["_row_id"].astype(str) == row_key
                        df.loc[mask, "Human decision"] = corrected
                        df.loc[mask, "Reviewer note"] = st.session_state.get(note_key, "")
                        st.session_state.result = df
                        st.toast("Correction saved for this session and included in exports.")
                        st.rerun()

with tab_all:
    choices = st.multiselect("Decision", ["PROMOTE", "BLOCK", "IGNORE", "REVIEW"], default=["PROMOTE", "BLOCK", "IGNORE", "REVIEW"])
    q = st.text_input("Search terms contain")
    view = df[df.Decision.isin(choices)]
    if q:
        view = view[view["Search term"].astype(str).str.contains(q, case=False, na=False)]
    st.dataframe(view, hide_index=True, width="stretch", height=520)

with tab_export:
    st.write("Download the enriched audit file, plus separate promote and negative-keyword worklists. Confirm targeting and match types before importing into Google Ads.")
    final = df.copy()
    final["Final decision"] = final["Human decision"].replace("", pd.NA).fillna(final.Decision)
    audit = final.drop(columns=["_row_id"], errors="ignore")
    def csv_bytes(frame):
        return frame.to_csv(index=False).encode("utf-8-sig")
    a,b,c = st.columns(3)
    a.download_button("Download full triage CSV", csv_bytes(audit), "search_term_triage.csv", "text/csv", width="stretch")
    promotion_context = [c for c in ("Campaign", "Ad group", "Match type", "Confidence", "Reason") if c in audit.columns]
    promotions = audit[audit["Final decision"] == "PROMOTE"][["Search term", *promotion_context]].copy()
    promotions = promotions.rename(columns={"Search term": "Keyword", "Match type": "Triggering match type"})
    promotions.insert(1, "Match type", "Exact")
    b.download_button("Download promote list", csv_bytes(promotions), "promote_candidates.csv", "text/csv", width="stretch")
    negative_context = [c for c in ("Campaign", "Ad group", "Match type", "Confidence", "Reason") if c in audit.columns]
    negatives = audit[audit["Final decision"] == "BLOCK"][["Search term", *negative_context]].copy()
    negatives = negatives.rename(columns={"Match type": "Triggering match type"})
    negatives.insert(0, "Keyword", "[" + negatives["Search term"].astype(str) + "]")
    negatives = negatives.drop(columns="Search term")
    negatives.insert(1, "Match type", "Negative exact")
    negatives["Level"] = "Campaign"
    if "Ad group" in negatives:
        ad_group_present = negatives["Ad group"].fillna("").astype(str).str.strip().ne("")
        negatives.loc[ad_group_present, "Level"] = "Ad group"
    c.download_button("Download negative list", csv_bytes(negatives), "negative_candidates.csv", "text/csv", width="stretch")
    st.caption("Promotions use exact match suggestions. Negative candidates use exact negative syntax and the ad-group level when available, otherwise campaign level. Review scope, match type, and policy before importing.")
