"""
Frontend Reusable UI Components for TriageIQ.
Includes Evidence-First Cards, Statistical Uncertainty Badges, and Review Workflow Controls.
"""

import streamlit as st
import pandas as pd
import html
from typing import Any


def render_evidence_card(row_data: Any, is_review_queue: bool = False, key_prefix: str = "card"):
    """
    Renders a compact, clean, and evidence-first recommendation card.
    Information Hierarchy:
    1. Header: Query + Decision Badge + Confidence + Needs Review + Campaign Context
    2. Metrics Row: Clicks, Spend, Conversions, Conversion Value, CPA (when meaningful), Wilson 95% CI
    3. Reason: One clear human-readable sentence prominently visible without expanding
    4. Additional Evidence: Collapsible expander for Supporting Evidence, Limitations & Action Plan
    5. Action Buttons (if in review queue): Approve, Block, Dismiss, or Apply Precedent
    """
    row_id = row_data.get("row_id", 0)
    query_text = str(row_data.get("query_text", "")).strip()
    decision = str(row_data.get("decision", "IGNORE")).strip()
    needs_review = bool(row_data.get("needs_review", False))
    confidence = str(row_data.get("confidence", "MEDIUM")).strip()
    campaign = str(row_data.get("campaign", "")).strip()
    ad_group = str(row_data.get("ad_group", "")).strip()
    match_type = str(row_data.get("match_type", "Broad")).strip()
    
    clicks = int(row_data.get("clicks", 0))
    cost = float(row_data.get("cost", 0.0))
    conversions = float(row_data.get("conversions", 0.0))
    conv_val = float(row_data.get("conversion_value", 0.0))
    ci_lower = float(row_data.get("ci_lower", 0.0))
    ci_upper = float(row_data.get("ci_upper", 0.0))
    cpa = row_data.get("cpa")
    
    # Meaningful CPA display: only show when conversions > 0
    cpa_str = f"${cpa:,.2f}" if (cpa is not None and pd.notnull(cpa) and conversions > 0) else "—"
    
    # Statistical uncertainty display
    ci_str = f"[{ci_lower:.1%}, {ci_upper:.1%}]" if clicks > 0 else "N/A"
    
    supp_ev = str(row_data.get("supporting_evidence", "")).strip()
    counter_ev = str(row_data.get("counterevidence", "")).strip()
    reason = str(row_data.get("reason", "")).strip()
    next_action = str(row_data.get("next_action", "")).strip()
    
    with st.container(border=True):
        # 1. HEADER ROW: Query, Badges, Campaign & Ad Group
        col_hdr_left, col_hdr_right = st.columns([3, 2])
        
        with col_hdr_left:
            dec_color_map = {
                "PROMOTE": ("rgba(16, 185, 129, 0.16)", "#34D399", "rgba(16, 185, 129, 0.38)"),
                "BLOCK": ("rgba(239, 68, 68, 0.16)", "#F87171", "rgba(239, 68, 68, 0.38)"),
                "IGNORE": ("rgba(156, 163, 175, 0.14)", "#9CA3AF", "rgba(156, 163, 175, 0.3)")
            }
            bg, fg, bd = dec_color_map.get(decision, ("rgba(156, 163, 175, 0.14)", "#9CA3AF", "rgba(156, 163, 175, 0.3)"))
            dec_badge = f"<span style='background-color:{bg}; color:{fg}; border:1px solid {bd}; padding:2px 8px; border-radius:4px; font-weight:700; font-size:0.75rem; letter-spacing:0.03em;'>{decision}</span>"
            
            review_badge = ""
            if needs_review:
                review_badge = "<span style='background-color:rgba(245, 158, 11, 0.16); color:#FBBF24; border:1px solid rgba(245, 158, 11, 0.38); padding:2px 8px; border-radius:4px; font-weight:700; font-size:0.75rem; margin-left:6px;'>NEEDS REVIEW</span>"
                
            conf_badge = f"<span style='font-size:0.78rem; color:#D1CBD5; margin-left:8px;'>Confidence: <strong style='color:#FFFFFF;'>{confidence}</strong></span>"
            
            st.markdown(
                f"<div style='display:flex; align-items:center; flex-wrap:wrap; gap:6px;'>"
                f"<span style='font-size:1.02rem; font-weight:700; color:#FFFFFF;'>#{row_id}</span> "
                f"<code style='font-size:0.92rem; font-weight:600; color:#FFFFFF; background-color:#1E1030; padding:2px 6px; border-radius:4px; border:1px solid rgba(160, 80, 200, 0.35);'>{html.escape(query_text)}</code> "
                f"{dec_badge} {review_badge} {conf_badge}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        with col_hdr_right:
            st.markdown(
                f"<div style='text-align:right; font-size:0.8rem; color:#D1CBD5; padding-top:4px;'>"
                f"<span>{html.escape(campaign)}</span> &nbsp;›&nbsp; <em style='color:#D5A2FF;'>{html.escape(ad_group)}</em> ({html.escape(match_type)})"
                f"</div>",
                unsafe_allow_html=True
            )
            
        # 2. METRICS ROW (Compact, responsive flex row focused on core economics)
        st.markdown(
            f"<div style='font-size:0.81rem; color:#D1CBD5; background-color:#0E0716; padding:7px 14px; border-radius:6px; margin-top:8px; margin-bottom:8px; border:1px solid rgba(160, 80, 200, 0.22); display:flex; flex-wrap:wrap; gap:18px; align-items:center;'>"
            f"<span>Clicks: <strong style='color:#FFFFFF;'>{clicks:,}</strong></span>"
            f"<span>Spend: <strong style='color:#FFFFFF;'>${cost:,.2f}</strong></span>"
            f"<span>Conversions: <strong style='color:#FFFFFF;'>{int(conversions):,}</strong></span>"
            f"<span>Attributed Value: <strong style='color:#FFFFFF;'>${conv_val:,.2f}</strong></span>"
            f"<span>CPA: <strong style='color:#FFFFFF;'>{cpa_str}</strong></span>"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # 3. REASON (Prominently visible directly on the card without expanding)
        dec_accent = "#34D399" if decision == "PROMOTE" else ("#F87171" if decision == "BLOCK" else ("#FBBF24" if needs_review else "#9CA3AF"))
        st.markdown(
            f"<div style='margin-top:6px; margin-bottom:10px; font-size:0.85rem; color:#FFFFFF; line-height:1.45; padding:8px 14px; background-color:#140A1F; border-left:3.5px solid {dec_accent}; border-top:1px solid rgba(160, 80, 200, 0.22); border-right:1px solid rgba(160, 80, 200, 0.22); border-bottom:1px solid rgba(160, 80, 200, 0.22); border-radius:0 6px 6px 0;'>"
            f"<strong style='color:#D5A2FF;'>Reason:</strong> {html.escape(reason)}"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # 4. ADDITIONAL EVIDENCE (Compact, Expandable Section with Wilson Bounds)
        with st.expander("🔎 Statistical Bounds, Supporting Evidence & Action Plan", expanded=False):
            st.markdown(
                f"<div style='margin-bottom:8px; font-size:0.81rem; color:#D1CBD5; padding:6px 12px; background:rgba(128, 0, 255, 0.08); border-radius:6px; border:1px solid rgba(160, 80, 200, 0.2);'>"
                f"<strong>Wilson 95% Confidence Interval:</strong> <strong style='color:#FFFFFF;'>{ci_str}</strong> "
                f"<span style='color:#AFA8B8;'>&nbsp;(Estimated true binomial conversion rate bound accounting for sample volume)</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            col_supp, col_count = st.columns(2)
            with col_supp:
                st.markdown(
                    f"<div style='background-color:rgba(16, 185, 129, 0.08); border:1px solid rgba(16, 185, 129, 0.25); border-radius:6px; padding:10px 14px; height:100%;'>"
                    f"<div style='font-size:0.75rem; font-weight:700; color:#34D399; margin-bottom:4px; letter-spacing:0.04em;'>🟢 SUPPORTING EVIDENCE</div>"
                    f"<div style='font-size:0.82rem; color:#F3EFF7; line-height:1.4;'>{html.escape(supp_ev)}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col_count:
                st.markdown(
                    f"<div style='background-color:rgba(239, 68, 68, 0.08); border:1px solid rgba(239, 68, 68, 0.25); border-radius:6px; padding:10px 14px; height:100%;'>"
                    f"<div style='font-size:0.75rem; font-weight:700; color:#F87171; margin-bottom:4px; letter-spacing:0.04em;'>🔴 COUNTEREVIDENCE & LIMITATIONS</div>"
                    f"<div style='font-size:0.82rem; color:#F3EFF7; line-height:1.4;'>{html.escape(counter_ev)}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
            st.markdown(
                f"<div style='margin-top:10px; font-size:0.82rem; color:#D1CBD5; line-height:1.45;'>"
                f"<strong style='color:#FFFFFF;'>Recommended Next Action:</strong> <span style='color:#D5A2FF; font-weight:600;'>{html.escape(next_action)}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Check for reviewer precedent match
        precedent = None
        if "precedent_memory" in st.session_state and st.session_state.precedent_memory is not None:
            try:
                precedent = st.session_state.precedent_memory.find_best_precedent(query_text, target_campaign=campaign)
            except TypeError:
                try:
                    precedent = st.session_state.precedent_memory.find_best_precedent(query_text)
                except Exception:
                    precedent = None
            except Exception:
                precedent = None

        if precedent and precedent.get("similarity", 0) >= 0.45:
            sim_pct = int(precedent["similarity"] * 100)
            rev_dec = precedent["revised_decision"]
            rev_color = "#34D399" if rev_dec == "PROMOTE" else ("#F87171" if rev_dec == "BLOCK" else "#D1CBD5")
            st.markdown(
                f"<div style='background:rgba(128, 0, 255, 0.09); border:1px solid rgba(160, 80, 200, 0.35); border-radius:6px; padding:8px 12px; margin-top:8px; margin-bottom:8px;'>"
                f"<div style='font-size:0.75rem; font-weight:700; color:#D5A2FF; letter-spacing:0.04em;'>💡 CONTEXTUAL REVIEWER PRECEDENT ({sim_pct}% SIMILARITY)</div>"
                f"<div style='font-size:0.82rem; color:#F3EFF7; margin-top:2px;'>"
                f"Previous reviewer overrode similar query <code style='background-color:#1E1030; color:#FFFFFF; padding:1px 5px; border-radius:3px;'>{html.escape(precedent['query_text'])}</code> to "
                f"<strong style='color:{rev_color};'>{rev_dec}</strong>. Rationale: <em>\"{html.escape(precedent.get('reason', 'Analyst verified'))}\"</em>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # 5. REVIEWER ACTIONS (If in Review Queue)
        if is_review_queue:
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            has_valid_precedent = precedent and precedent.get("similarity", 0) >= 0.45 and precedent.get("revised_decision") != decision
            
            if has_valid_precedent:
                b_prec, b1, b2, b3 = st.columns([1.8, 1.4, 1.4, 1.4])
                with b_prec:
                    if st.button(f"⚡ Apply Precedent ({precedent['revised_decision']})", key=f"btn_prec_{key_prefix}_{row_id}", type="primary", use_container_width=True):
                        notes = f"Precedent applied from '{precedent['query_text']}': {precedent.get('reason', '')}"
                        st.session_state.reviewer_actions[query_text.lower().strip()] = {
                            "reviewer_action": f"APPLIED_PRECEDENT_{precedent['revised_decision']}",
                            "final_decision": precedent["revised_decision"],
                            "reviewer_notes": notes,
                            "reviewer": "Analyst (Precedent Guided)"
                        }
                        if "precedent_memory" in st.session_state and st.session_state.precedent_memory is not None:
                            st.session_state.precedent_memory.record_correction(
                                query_text=query_text,
                                campaign=campaign,
                                ad_group=ad_group,
                                original_decision=decision,
                                revised_decision=precedent["revised_decision"],
                                reason=notes,
                                reviewer="Analyst (Precedent Guided)",
                                metrics={"clicks": clicks, "cost": cost, "conversions": conversions}
                            )
                        st.toast(f"✓ Applied precedent: '{query_text}' -> {precedent['revised_decision']}!", icon="⚡")
                        st.rerun()
            else:
                b1, b2, b3 = st.columns(3)
                
            with b1:
                if st.button("✅ Approve Promotion", key=f"btn_prom_{key_prefix}_{row_id}", use_container_width=True):
                    notes = "Analyst verified commercial intent warrants promotion."
                    st.session_state.reviewer_actions[query_text.lower().strip()] = {
                        "reviewer_action": "APPROVED_PROMOTION",
                        "final_decision": "PROMOTE",
                        "reviewer_notes": notes,
                        "reviewer": "Human Analyst"
                    }
                    if "precedent_memory" in st.session_state and st.session_state.precedent_memory is not None:
                        st.session_state.precedent_memory.record_correction(
                            query_text=query_text,
                            campaign=campaign,
                            ad_group=ad_group,
                            original_decision=decision,
                            revised_decision="PROMOTE",
                            reason=notes,
                            reviewer="Human Analyst",
                            metrics={"clicks": clicks, "cost": cost, "conversions": conversions}
                        )
                    st.toast(f"✓ '{query_text}' updated to PROMOTE in session memory!", icon="✅")
                    st.rerun()
            with b2:
                if st.button("🚫 Confirm Block", key=f"btn_blk_{key_prefix}_{row_id}", use_container_width=True):
                    notes = "Analyst verified query is off-target or wasteful."
                    st.session_state.reviewer_actions[query_text.lower().strip()] = {
                        "reviewer_action": "CONFIRMED_BLOCK",
                        "final_decision": "BLOCK",
                        "reviewer_notes": notes,
                        "reviewer": "Human Analyst"
                    }
                    if "precedent_memory" in st.session_state and st.session_state.precedent_memory is not None:
                        st.session_state.precedent_memory.record_correction(
                            query_text=query_text,
                            campaign=campaign,
                            ad_group=ad_group,
                            original_decision=decision,
                            revised_decision="BLOCK",
                            reason=notes,
                            reviewer="Human Analyst",
                            metrics={"clicks": clicks, "cost": cost, "conversions": conversions}
                        )
                    st.toast(f"✓ '{query_text}' updated to BLOCK in session memory!", icon="🚫")
                    st.rerun()
            with b3:
                if st.button("💤 Keep Ignored", key=f"btn_dsm_{key_prefix}_{row_id}", use_container_width=True):
                    notes = "Analyst dismissed to maintain status quo."
                    st.session_state.reviewer_actions[query_text.lower().strip()] = {
                        "reviewer_action": "DISMISSED_IGNORE",
                        "final_decision": "IGNORE",
                        "reviewer_notes": notes,
                        "reviewer": "Human Analyst"
                    }
                    if "precedent_memory" in st.session_state and st.session_state.precedent_memory is not None:
                        st.session_state.precedent_memory.record_correction(
                            query_text=query_text,
                            campaign=campaign,
                            ad_group=ad_group,
                            original_decision=decision,
                            revised_decision="IGNORE",
                            reason=notes,
                            reviewer="Human Analyst",
                            metrics={"clicks": clicks, "cost": cost, "conversions": conversions}
                        )
                    st.toast(f"✓ '{query_text}' dismissed and marked resolved!", icon="💤")
                    st.rerun()
