from __future__ import annotations
import re
import pandas as pd

REQUIRED = ["Search term", "Clicks", "Impressions", "Cost", "Conversions"]
ALIASES = {
    "search term": "Search term", "search terms": "Search term", "query": "Search term",
    "clicks": "Clicks", "impr.": "Impressions", "impr": "Impressions", "impressions": "Impressions",
    "cost": "Cost", "cost (inr)": "Cost", "conversions": "Conversions", "campaign": "Campaign",
    "campaign name": "Campaign", "ad group": "Ad group", "ad group name": "Ad group",
    "row id": "Row ID", "match type": "Match type", "conversion value": "Conversion value",
}

def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    rename = {}
    for c in out.columns:
        key = re.sub(r"\s+", " ", str(c).strip().lower().replace("_", " ").replace("\ufeff", ""))
        if key in ALIASES: rename[c] = ALIASES[key]
    out = out.rename(columns=rename)
    missing = [c for c in REQUIRED if c not in out.columns]
    if missing: raise ValueError("Missing required columns: " + ", ".join(missing))
    for col in ["Clicks", "Impressions", "Cost", "Conversions", "Conversion value"]:
        if col not in out:
            continue
        out[col] = pd.to_numeric(out[col].astype(str).str.replace(",", "", regex=False).str.replace(r"[^\d.\-]", "", regex=True), errors="coerce").fillna(0)
    out["Search term"] = out["Search term"].fillna("").astype(str).str.strip()
    if "Campaign" not in out: out["Campaign"] = ""
    if "Ad group" not in out: out["Ad group"] = ""
    out = out[~out["Search term"].eq("")].reset_index(drop=True)
    return out

def analyze(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df["_row_id"] = range(len(df))
    # Conservative transparent rules: enough evidence is required both to promote and to block.
    spend = df["Cost"]
    clicks = df["Clicks"]
    conv = df["Conversions"]
    conv_value = df.get("Conversion value", pd.Series(0, index=df.index))
    decisions, confidence, reasons = [], [], []
    for c, cv, cost, value in zip(clicks, conv, spend, conv_value):
        if cv == 0 and value > 0:
            decisions.append("REVIEW"); confidence.append("Low")
            reasons.append(f"Conversion value {value:g} is recorded with zero conversions; reconcile the source data before acting.")
        elif c >= 20 and cv >= 2:
            decisions.append("PROMOTE"); confidence.append("High" if cv >= 4 and c >= 30 else "Medium")
            value_note = f" Recorded conversion value is {value:g}." if value > 0 else ""
            reasons.append(f"{cv:g} conversions across {c:g} clicks meet the minimum volume rule; verify intent and value.{value_note}")
        elif c >= 25 and cv == 0 and cost > 0:
            decisions.append("BLOCK"); confidence.append("High" if c >= 50 else "Medium" if c >= 35 else "Low")
            reasons.append(f"{c:g} clicks and {cost:g} spend with no conversions indicate likely wasted spend; check attribution lag.")
        elif c < 8 and cv > 0:
            decisions.append("REVIEW"); confidence.append("Low")
            reasons.append(f"Only {c:g} clicks support {cv:g} conversion(s); thin data, so review before promoting.")
        elif c < 8:
            decisions.append("REVIEW"); confidence.append("Low")
            reasons.append(f"Only {c:g} clicks; insufficient evidence for a reliable promote or block decision.")
        elif cv > 0:
            decisions.append("REVIEW"); confidence.append("Low")
            reasons.append(f"{cv:g} conversion(s) but below the 2-conversion and 20-click promotion thresholds; human review required.")
        else:
            decisions.append("IGNORE"); confidence.append("Low")
            reasons.append(f"{c:g} clicks and no conversions; below the evidence threshold for blocking, so monitor.")
    df["Decision"], df["Confidence"], df["Reason"] = decisions, confidence, reasons
    df["Normalized query"] = df["Search term"].str.lower().str.replace(r"[^\w\s]", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
    df["Duplicate group size"] = df.groupby("Normalized query")["Normalized query"].transform("size")
    df["Duplicate group"] = df["Normalized query"].where(df["Duplicate group size"] > 1, "")
    return df
