"""
Architectural Regression Tests.
Verifies decoupled stack boundaries: frontend, backend, CLI, and engine layers.
"""

import unittest


class TestStackArchitecture(unittest.TestCase):
    """Verifies that all decoupled frontend and backend modules import correctly."""

    def test_backend_submodules_import(self):
        import backend
        from backend.rules import TriageEngine, AdvertiserProfile
        from backend.stats import wilson_score_interval, empirical_bayes_cvr
        from backend.clustering import cluster_search_queries
        from backend.copilot import generate_copilot_response
        from backend.negatives import generate_context_aware_negative_suggestions
        from backend.learning import ReviewerPrecedentMemory
        from backend.exporter import export_triage_results

        self.assertIsNotNone(TriageEngine)
        self.assertIsNotNone(AdvertiserProfile)
        self.assertIsNotNone(wilson_score_interval)
        self.assertIsNotNone(empirical_bayes_cvr)
        self.assertIsNotNone(cluster_search_queries)
        self.assertIsNotNone(generate_copilot_response)
        self.assertIsNotNone(generate_context_aware_negative_suggestions)
        self.assertIsNotNone(ReviewerPrecedentMemory)
        self.assertIsNotNone(export_triage_results)

    def test_frontend_submodules_import(self):
        import frontend
        from frontend.styles import get_custom_css, inject_custom_css
        from frontend.components import render_evidence_card

        self.assertIsNotNone(get_custom_css)
        self.assertIsNotNone(inject_custom_css)
        self.assertIsNotNone(render_evidence_card)
        css = get_custom_css()
        self.assertIn("<style>", css)
        self.assertIn("hero-container", css)

    def test_backward_compatibility_triage_engine(self):
        import triage_engine
        from triage_engine.rules import TriageEngine
        from triage_engine.stats import wilson_score_interval

        self.assertIsNotNone(TriageEngine)
        self.assertIsNotNone(wilson_score_interval)


if __name__ == "__main__":
    unittest.main()
