import unittest
import pandas as pd
import numpy as np

from triage_engine.copilot import generate_copilot_response

class TestCopilot30Questions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res_df = pd.DataFrame([
            {
                "row_id": 1,
                "query_text": "business loan equipment",
                "decision": "PROMOTE",
                "confidence": "HIGH",
                "needs_review": False,
                "reason": "Sustained volume and low CPA",
                "clicks": 45,
                "cost": 300.0,
                "conversions": 5.0,
                "conversion_value": 2500.0,
                "cpa": 60.0,
                "proposed_bid": 4.50,
                "ci_lower": 0.04,
                "ci_upper": 0.22,
                "campaign": "Equipment Financing",
                "ad_group": "Loans",
                "match_type": "Exact",
                "supporting_evidence": "Consistent conversions",
                "counterevidence": "None",
                "next_action": "Promote as Exact Match keyword",
                "cluster_has_conflict": False,
                "impressions": 1000
            },
            {
                "row_id": 6,
                "query_text": "equipment financing calculator",
                "decision": "IGNORE",
                "confidence": "MEDIUM",
                "needs_review": True,
                "reason": "1 conversion observed with 4 clicks",
                "clicks": 4,
                "cost": 45.0,
                "conversions": 1.0,
                "conversion_value": 200.0,
                "cpa": 45.0,
                "proposed_bid": 2.10,
                "ci_lower": 0.045,
                "ci_upper": 0.58,
                "campaign": "Equipment Financing",
                "ad_group": "Calculators",
                "match_type": "Broad",
                "supporting_evidence": "Recorded 1 conversion",
                "counterevidence": "Sample size too small (n=4)",
                "next_action": "Hold in human review queue",
                "cluster_has_conflict": True,
                "impressions": 500
            },
            {
                "row_id": 12,
                "query_text": "personal loans for bad credit",
                "decision": "BLOCK",
                "confidence": "HIGH",
                "needs_review": False,
                "reason": "Non-commercial consumer query matches negative policy",
                "clicks": 18,
                "cost": 120.0,
                "conversions": 0.0,
                "conversion_value": 0.0,
                "cpa": None,
                "proposed_bid": 0.0,
                "ci_lower": 0.0,
                "ci_upper": 0.15,
                "campaign": "General",
                "ad_group": "Loans",
                "match_type": "Broad",
                "supporting_evidence": "Matches consumer exclusion",
                "counterevidence": "None",
                "next_action": "Add to negative keywords",
                "cluster_has_conflict": False,
                "impressions": 300
            }
        ])
        cls.clean_df = cls.res_df.copy()

    def _ask(self, q):
        return generate_copilot_response(q, self.res_df, self.clean_df, 220.0)

    # Category 1: Executive & Portfolio Metrics (Questions 1-6)
    def test_q01_row_audit(self):
        resp = self._ask("Audit row #6")
        self.assertIn("Row #6", resp)
        self.assertIn("equipment financing calculator", resp)

    def test_q02_specific_query_search(self):
        resp = self._ask("about query 'business loan equipment'")
        self.assertIn("business loan equipment", resp)

    def test_q03_potential_savings(self):
        resp = self._ask("How much wasted spend can we save?")
        self.assertIn("Waste Reduction", resp)

    def test_q04_account_overview(self):
        resp = self._ask("Give me an account summary of total spend and volume")
        self.assertIn("Macro Overview", resp)

    def test_q05_baseline_cpa(self):
        resp = self._ask("What is our account baseline CPA?")
        self.assertIn("Baseline CPA", resp)

    def test_q06_decision_distribution(self):
        resp = self._ask("Show decision breakdown across the portfolio")
        self.assertIn("Distribution", resp)

    # Category 2: Human Review & Variance Traps (Questions 7-10)
    def test_q07_review_queue(self):
        resp = self._ask("How many terms are in the human review queue?")
        self.assertIn("Review Queue", resp)

    def test_q08_small_sample_variance_trap(self):
        resp = self._ask("Why are terms with 1 conversion quarantined in review?")
        self.assertIn("Variance Trap", resp)

    def test_q09_wilson_score_interval(self):
        resp = self._ask("How does the Wilson confidence interval work?")
        self.assertIn("Wilson Score", resp)

    def test_q10_empirical_bayes_shrinkage(self):
        resp = self._ask("Explain Empirical Bayes shrinkage")
        self.assertIn("Empirical Bayes", resp)

    # Category 3: Decision Contract & Policies (Questions 11-16)
    def test_q11_three_way_contract(self):
        resp = self._ask("Explain the strict 3-way decision contract")
        self.assertIn("Contract", resp)

    def test_q12_promotion_criteria(self):
        resp = self._ask("What are the promotion criteria for keywords?")
        self.assertIn("Criteria for Keyword Promotion", resp)

    def test_q13_blocking_criteria(self):
        resp = self._ask("What are the blocking criteria?")
        self.assertIn("Exclusion", resp)

    def test_q14_ignore_criteria(self):
        resp = self._ask("Why ignore keywords and keep status quo?")
        self.assertIn("IGNORE", resp)

    def test_q15_target_cpa_ceiling(self):
        resp = self._ask("Explain the 220 Target CPA ceiling")
        self.assertIn("220", resp)

    def test_q16_kestrel_boundaries(self):
        resp = self._ask("What are Kestrel negative policy boundaries?")
        self.assertIn("Kestrel Business Funding", resp)

    # Category 4: Exclusions & Bleeders (Questions 17-22)
    def test_q17_consumer_loans(self):
        resp = self._ask("Why are personal loans and mortgages blocked?")
        self.assertIn("Consumer Loan", resp)

    def test_q18_grants_stimulus(self):
        resp = self._ask("Why block government grant queries?")
        self.assertIn("Grant", resp)

    def test_q19_jobs_hiring(self):
        resp = self._ask("Why exclude jobs and salary searches?")
        self.assertIn("Employment", resp)

    def test_q20_non_buyer_queries(self):
        resp = self._ask("Why are templates and pdf downloads excluded?")
        self.assertIn("Non-Buyer", resp)

    def test_q21_top_promoted_winners(self):
        resp = self._ask("Show me top promoted winners")
        self.assertIn("Promoted Candidates", resp)

    def test_q22_top_spend_bleeders(self):
        resp = self._ask("Show biggest bleeders with zero conversions")
        self.assertIn("Bleeders", resp)

    # Category 5: Campaigns & Performance (Questions 23-28)
    def test_q23_best_campaigns(self):
        resp = self._ask("Which are the most efficient campaigns?")
        self.assertIn("Efficient Campaigns", resp)

    def test_q24_worst_campaigns(self):
        resp = self._ask("Which are the least efficient campaigns with high CPA?")
        self.assertIn("Least Efficient Campaigns", resp)

    def test_q25_zero_conv_spend(self):
        resp = self._ask("How much spend was wasted on zero conversion queries?")
        self.assertIn("Zero-Conversion", resp)

    def test_q26_low_ctr_diagnostics(self):
        resp = self._ask("Analyze low CTR high impression terms")
        self.assertIn("Low CTR", resp)

    def test_q27_match_type_performance(self):
        resp = self._ask("Show match type performance breakdown")
        self.assertIn("Match Type", resp)

    def test_q28_keyword_cannibalization(self):
        resp = self._ask("Explain internal keyword cannibalization")
        self.assertIn("Cannibalization", resp)

    # Category 6: Bidding, Scope & Exports (Questions 29-35)
    def test_q29_top_ad_groups(self):
        resp = self._ask("Which are the top ad groups by spend?")
        self.assertIn("Ad Groups", resp)

    def test_q30_suggested_max_cpc(self):
        resp = self._ask("How is the proposed Max CPC bid calculated?")
        self.assertIn("Max CPC", resp)

    def test_q31_narrow_scope_rule(self):
        resp = self._ask("Explain the narrowest scope rule for negatives")
        self.assertIn("Scope Rule", resp)

    def test_q32_over_exclusion_risk(self):
        resp = self._ask("What is over-exclusion risk and collateral damage?")
        self.assertIn("Over-Exclusion", resp)

    def test_q33_negative_suggestions(self):
        resp = self._ask("How are candidate negative suggestions generated?")
        self.assertIn("Negative Keyword", resp)

    def test_q34_google_ads_export_specs(self):
        resp = self._ask("What is the Google Ads export CSV format?")
        self.assertIn("Google Ads", resp)

    def test_q35_google_ads_import_guide(self):
        resp = self._ask("How do I import negative keywords into Google Ads Editor?")
        self.assertIn("Google Ads Editor", resp)

    def test_q36_search_intent_clustering(self):
        resp = self._ask("How does search intent clustering work?")
        self.assertIn("Clustering", resp)

    def test_q37_cluster_conflicts(self):
        resp = self._ask("Why do decision conflicts occur in a cluster?")
        self.assertIn("Conflicts", resp)

    def test_q38_reviewer_precedents(self):
        resp = self._ask("How does session learning from reviewer precedents work?")
        self.assertIn("Precedents", resp)


if __name__ == "__main__":
    unittest.main()
