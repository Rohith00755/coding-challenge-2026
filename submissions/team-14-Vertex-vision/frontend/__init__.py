"""
Frontend UI Layer for TriageIQ.
Encapsulates Enterprise Design System styles, theme injection, and modular presentation components.
"""

from frontend.styles import inject_custom_css, get_custom_css
from frontend.components import render_evidence_card

__all__ = [
    "inject_custom_css",
    "get_custom_css",
    "render_evidence_card",
]
