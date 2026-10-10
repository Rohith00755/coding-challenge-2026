import csv
import math
import re
from collections import defaultdict

def erf_inverse(y):
    """Accurate numerical approximation of inverse error function."""
    a = 0.147
    sgn = 1.0 if y > 0 else (-1.0 if y < 0 else 0.0)
    ln_term = math.log(max(1e-15, 1.0 - y * y))
    term1 = 2.0 / (math.pi * a) + ln_term / 2.0
    inner = term1 * term1 - ln_term / a
    return sgn * math.sqrt(max(0.0, math.sqrt(max(0.0, inner)) - term1))

def wilson_score_lower(conversions, clicks, confidence=0.95):
    """Calculates the conservative lower bound of conversion rate using Wilson interval."""
    if clicks <= 0:
        return 0.0
    alpha = 1.0 - confidence
    z = math.sqrt(2.0) * erf_inverse(1.0 - alpha)
    p = conversions / clicks
    denominator = 1.0 + (z * z) / clicks
    center = p + (z * z) / (2.0 * clicks)
    spread = z * math.sqrt(max(0.0, (p * (1.0 - p) + (z * z) / (4.0 * clicks)) / clicks))
    return max(0.0, (center - spread) / denominator)

def tokenize(text):
    return re.findall(r'[a-z0-9]+', str(text).lower())

def run_pipeline():
    print("Loading search_terms_report.csv...")
    rows = []
    with open("search_terms_report.csv", "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                imp = float(r.get('impressions', 0) or 0)
                clk = float(r.get('clicks', 0) or 0)
                cost = float(r.get('cost', 0) or 0)
                conv = float(r.get('conversions', 0) or 0)
                val = float(r.get('conversion_value', 0) or 0)
                if clk <= imp and cost >= 0 and conv >= 0 and conv <= clk:
                    r['impressions'] = imp
                    r['clicks'] = clk
                    r['cost'] = cost
                    r['conversions'] = conv
                    r['conversion_value'] = val
                    rows.append(r)
            except Exception:
                continue

    if not rows:
        print("Error: No valid rows found in search_terms_report.csv!")
        return

    # 1. Empirical Bayes Beta-Binomial shrinkage parameters
    total_clicks = sum(r['clicks'] for r in rows)
    total_convs = sum(r['conversions'] for r in rows)
    global_cvr = total_convs / max(total_clicks, 1.0)
    prior_weight = total_clicks / max(len(rows), 1.0)
    alpha_prior = global_cvr * prior_weight
    beta_prior = (1.0 - global_cvr) * prior_weight

    # 2. Token / N-Gram waste tracking
    word_stats = defaultdict(lambda: {'cost': 0.0, 'conversions': 0.0})
    for r in rows:
        words = set(tokenize(r['search_term']))
        for w in words:
            if len(w) > 2:
                word_stats[w]['cost'] += r['cost']
                word_stats[w]['conversions'] += r['conversions']

    # Identify macro-waste tokens
    ngram_negatives = []
    for w, stats in word_stats.items():
        if stats['cost'] >= 50.0 and stats['conversions'] == 0:
            ngram_negatives.append({
                'Campaign': 'Account Level',
                'Ad Group': '--',
                'Keyword': w,
                'Criterion Type': 'Negative Broad',
                'Status': 'Enabled',
                'Reason': f"N-Gram Waste: Token '{w}' spent ${stats['cost']:.2f} account-wide with 0 conversions."
            })

    # 3. Intent Cluster Aggregation (Semantic Jaccard/Token Clustering)
    cluster_groups = defaultdict(list)
    for r in rows:
        tokens = tokenize(r['search_term'])
        root_token = " ".join(tokens[:2]) if len(tokens) >= 2 else (tokens[0] if tokens else "other")
        cluster_groups[root_token].append(r)

    cluster_metrics = {}
    for cl_name, cl_rows in cluster_groups.items():
        cluster_metrics[cl_name] = {
            'cost': sum(x['cost'] for x in cl_rows),
            'conversions': sum(x['conversions'] for x in cl_rows)
        }

    # 4. Triage Classification & Cannibalization Prevention
    forbidden_terms = ['personal', 'mortgage', 'car', 'student', 'grant', 'job', 'internship', 'salary', 'underwriter']
    target_roas = 2.0
    triage_results = []

    for r in rows:
        term = str(r['search_term']).lower()
        clk = r['clicks']
        conv = r['conversions']
        cost = r['cost']
        val = r['conversion_value']
        
        # Empirical Bayes estimate
        eb_cvr = (conv + alpha_prior) / (clk + alpha_prior + beta_prior)
        wilson_lb = wilson_score_lower(conv, clk, confidence=0.95)
        roas = (val / cost) if cost > 0 else 0.0

        tokens = tokenize(r['search_term'])
        root_token = " ".join(tokens[:2]) if len(tokens) >= 2 else (tokens[0] if tokens else "other")
        c_stats = cluster_metrics.get(root_token, {'cost': 0.0, 'conversions': 0.0})

        # Decision hierarchy
        if any(w in term for w in forbidden_terms):
            action = "Block"
            reason = "Client does not offer this product/service (Kestrel Business Funding Rule)."
        elif cost > 50.0 and conv == 0:
            action = "Block"
            reason = f"Financial bleed: High spend (${cost:.2f}) with zero conversions."
        elif c_stats['conversions'] == 0 and c_stats['cost'] > 100.0:
            action = "Block"
            reason = f"Semantic Bleed: Intent group '{root_token}' spent ${c_stats['cost']:.2f} with 0 conversions."
        elif conv > 0 and roas < (target_roas * 0.5):
            action = "Block"
            reason = f"Unprofitable: ROAS ({roas:.2f}x) falls severely below targets."
        elif wilson_lb > 0.03 and eb_cvr > 0.05:
            action = "Promote"
            reason = f"Statistically significant performer (Empirical CVR {eb_cvr:.1%}, Wilson Lower Bound {wilson_lb:.1%})."
        else:
            action = "Ignore"
            reason = "Insufficient statistical evidence. Kept in observation."

        # Schema output mapping + Cannibalization isolation
        if action == "Promote":
            triage_results.append({
                'Campaign': r['campaign'] + " - EXACT WINNERS",
                'Ad Group': r['ad_group'],
                'Keyword': r['search_term'],
                'Criterion Type': 'Exact',
                'Status': 'Enabled',
                'Reason': reason
            })
            triage_results.append({
                'Campaign': r['campaign'],
                'Ad Group': r['ad_group'],
                'Keyword': r['search_term'],
                'Criterion Type': 'Negative Exact',
                'Status': 'Enabled',
                'Reason': 'Search Term Isolation: Negative exact applied to original campaign to prevent cannibalization.'
            })
        elif action == "Block":
            triage_results.append({
                'Campaign': r['campaign'],
                'Ad Group': r['ad_group'],
                'Keyword': r['search_term'],
                'Criterion Type': 'Negative Exact',
                'Status': 'Enabled',
                'Reason': reason
            })
        else:
            triage_results.append({
                'Campaign': r['campaign'],
                'Ad Group': r['ad_group'],
                'Keyword': r['search_term'],
                'Criterion Type': 'Broad',
                'Status': 'Paused',
                'Reason': reason
            })

    # 5. Export Google Ads Editor compliant CSVs
    fieldnames = ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type', 'Status', 'Reason']
    
    with open("google_ads_editor_triage.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(triage_results)

    with open("google_ads_editor_ngram_negatives.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ngram_negatives)

    print("\n✅ Full Pipeline Complete!")
    print(f"Generated: google_ads_editor_triage.csv ({len(triage_results)} rows)")
    print(f"Generated: google_ads_editor_ngram_negatives.csv ({len(ngram_negatives)} rows)")

if __name__ == "__main__":
    run_pipeline()