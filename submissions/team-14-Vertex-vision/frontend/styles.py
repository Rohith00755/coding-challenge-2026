"""
Enterprise Design System & Theme Stylesheet for TriageIQ.
"""

import streamlit as st

def get_custom_css() -> str:
    """Returns the comprehensive custom CSS stylesheet for TriageIQ."""
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html {
        scroll-behavior: smooth;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #FFFFFF;
    }
    
    .stApp {
        background-color: #08050D;
        color: #FFFFFF;
    }
    
    /* ========================================================= */
    /* TRIAGEIQ RESTRAINED DARK PLUM DESIGN SYSTEM               */
    /* ========================================================= */
    
    /* Responsive Content Container & Max-Width */
    .main .block-container {
        max-width: 1360px !important;
        margin: 0 auto !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        overflow-x: hidden !important;
    }

    html {
        scroll-behavior: smooth;
    }

    /* ========================================================= */
    /* HERO SHOWCASE LANDING SECTION                             */
    /* ========================================================= */
    .hero-container {
        position: relative;
        background: radial-gradient(circle at 50% 16%, #18051F 0%, #08050D 68%);
        border: 1px solid rgba(160, 80, 200, 0.22);
        border-radius: 12px;
        margin-top: -1.2rem;
        margin-bottom: 2rem;
        padding: 24px 40px 65px 40px;
        overflow: hidden;
        text-align: center;
        box-sizing: border-box;
        box-shadow: 0 12px 48px rgba(8, 5, 13, 0.7);
        width: 100%;
    }
    
    /* Subtle Purple Ambient Lighting */
    .hero-ambient-glow {
        position: absolute;
        width: 650px;
        height: 650px;
        background: radial-gradient(circle, rgba(128, 0, 255, 0.22) 0%, rgba(24, 5, 31, 0.08) 50%, transparent 70%);
        top: 40px;
        left: 50%;
        transform: translateX(-50%);
        filter: blur(60px);
        pointer-events: none;
        z-index: 1;
    }
    
    .hero-ambient-left {
        position: absolute;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(128, 0, 255, 0.14) 0%, transparent 70%);
        top: 100px;
        left: 5%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 1;
    }
    
    .hero-ambient-right {
        position: absolute;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(160, 32, 240, 0.14) 0%, transparent 70%);
        top: 100px;
        right: 5%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 1;
    }

    /* Abstract Circular Arc behind Hero Content */
    .hero-arc-wrapper {
        position: absolute;
        top: 115px;
        left: 50%;
        transform: translateX(-50%);
        width: 860px;
        max-width: 90%;
        height: 480px;
        border-radius: 50% 50% 0 0 / 100% 100% 0 0;
        border-top: 1.5px solid rgba(180, 100, 255, 0.45);
        border-left: 1px solid rgba(128, 0, 255, 0.22);
        border-right: 1px solid rgba(128, 0, 255, 0.22);
        border-bottom: none;
        box-shadow: 0 -12px 50px rgba(128, 0, 255, 0.35), inset 0 8px 40px rgba(128, 0, 255, 0.16);
        background: radial-gradient(ellipse at 50% 0%, rgba(128, 0, 255, 0.14) 0%, rgba(24, 5, 31, 0.02) 60%, transparent 80%);
        pointer-events: none;
        z-index: 2;
    }

    /* Transparent Horizontal Navigation at Top */
    .hero-nav {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 12px 16px 12px;
    }
    
    .hero-logo-box {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }
    
    .hero-logo-icon {
        background: #8000FF;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.95rem;
        width: 32px;
        height: 32px;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 16px rgba(128, 0, 255, 0.6);
        letter-spacing: -0.02em;
    }
    
    .hero-logo-title {
        color: #FFFFFF;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .hero-nav-menu {
        display: flex;
        align-items: center;
        gap: 28px;
    }
    
    .hero-nav-item {
        color: #D1CBD5 !important;
        font-size: 0.88rem;
        font-weight: 500;
        text-decoration: none !important;
        transition: color 0.2s ease;
    }
    .hero-nav-item:hover {
        color: #FFFFFF !important;
    }
    
    .hero-nav-btn {
        background-color: #8000FF;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 8px 22px;
        border-radius: 24px;
        text-decoration: none !important;
        box-shadow: 0 2px 14px rgba(128, 0, 255, 0.45);
        transition: all 0.2s ease;
        display: inline-block;
    }
    .hero-nav-btn:hover {
        background-color: #921aff;
        box-shadow: 0 4px 20px rgba(128, 0, 255, 0.65);
    }
    
    /* Thin Purple Divider below Header */
    .hero-nav-divider {
        position: relative;
        z-index: 10;
        height: 1px;
        background-color: rgba(160, 80, 200, 0.18);
        margin-bottom: 45px;
    }
    
    /* Hero Content Container */
    .hero-body {
        position: relative;
        z-index: 10;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Lavender Eyebrow Text */
    .hero-eyebrow {
        color: #D5A2FF;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 16px;
        text-shadow: 0 0 16px rgba(213, 162, 255, 0.35);
    }
    
    /* Large Two-Line Headline */
    .hero-title {
        color: #FFFFFF;
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-top: 0;
        margin-bottom: 18px;
    }
    
    .hero-title-accent {
        color: #8000FF;
        background: linear-gradient(135deg, #A844FF 0%, #8000FF 55%, #6B00D6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 32px rgba(128, 0, 255, 0.4);
    }
    
    /* Muted White-Gray Supporting Description */
    .hero-desc {
        color: #D1CBD5;
        font-size: 1.05rem;
        line-height: 1.65;
        max-width: 720px;
        margin: 0 auto 34px auto;
        font-weight: 400;
    }
    
    /* Adjacent CTA Buttons */
    .hero-actions {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
        margin-top: 6px;
        margin-bottom: 6px;
    }
    
    .hero-btn-primary {
        background-color: #FFFFFF !important;
        color: #08050D !important;
        font-size: 0.95rem;
        font-weight: 700;
        padding: 13px 32px;
        border-radius: 30px;
        text-decoration: none !important;
        box-shadow: 0 4px 22px rgba(255, 255, 255, 0.22);
        transition: all 0.2s ease;
        display: inline-block;
        border: none;
    }
    .hero-btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(255, 255, 255, 0.35);
    }
    
    .hero-btn-secondary {
        background-color: transparent !important;
        color: #FFFFFF !important;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 12px 30px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        text-decoration: none !important;
        transition: all 0.2s ease;
        display: inline-block;
    }
    .hero-btn-secondary:hover {
        border-color: #D5A2FF;
        background-color: rgba(213, 162, 255, 0.1) !important;
        color: #D5A2FF !important;
        transform: translateY(-2px);
    }

    /* Native Hero Review Button (100% In-Memory State Switch - Zero Web Refresh) */
    div[data-testid="stHorizontalBlock"]:has(.hero-btn-primary) button,
    div[data-testid="stHorizontalBlock"]:has(.hero-btn-primary) div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #7928CA 0%, #581C87 100%) !important;
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 12px 30px !important;
        height: 48px !important;
        min-height: 48px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 4px 18px rgba(121, 40, 202, 0.45) !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.hero-btn-primary) button:hover,
    div[data-testid="stHorizontalBlock"]:has(.hero-btn-primary) div[data-testid="stButton"] button:hover {
        border-color: #D5A2FF !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 26px rgba(138, 43, 226, 0.65) !important;
    }

    /* Executive Top Header */
    .top-header {
        background: radial-gradient(circle at 50% 16%, #18051F 0%, #0E0717 100%);
        border: 1px solid rgba(160, 80, 200, 0.22);
        border-radius: 10px;
        padding: 16px 22px;
        margin-top: -1rem;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
    .header-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .header-subtitle {
        font-size: 0.86rem;
        color: #D1CBD5;
        margin-top: 3px;
        margin-bottom: 0;
        line-height: 1.4;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: rgba(16, 185, 129, 0.16);
        color: #34D399;
        border: 1px solid rgba(160, 80, 200, 0.22);
        border: 1px solid rgba(16, 185, 129, 0.38);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Primary KPI & Summary Cards */
    .kpi-card {
        background-color: #12091B;
        border: 1px solid rgba(160, 80, 200, 0.22);
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    .kpi-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 0.75rem;
        margin-top: 4px;
    }
    
    /* Global Container & Card Overrides */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #12091B !important;
        border: 1px solid rgba(160, 80, 200, 0.22) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Streamlit Expander Dark Theme */
    div[data-testid="stExpander"] {
        background-color: #12091B !important;
        border: 1px solid rgba(160, 80, 200, 0.22) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #D5A2FF !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0B0713 !important;
        border-right: 1px solid rgba(160, 80, 200, 0.18) !important;
    }
    [data-testid="stSidebar"] * {
        color: #D1CBD5;
    }
    [data-testid="stSidebar"] strong, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    /* Sidebar Navigation Radio Buttons: Sleek Pill Cards with Instant Smooth Transition */
    [data-testid="stSidebar"] div[data-testid="stRadio"] {
        width: 100% !important;
        margin-top: 4px !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 10px 14px !important;
        margin: 0 !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(160, 80, 200, 0.20) !important;
        cursor: pointer !important;
        position: relative !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        pointer-events: auto !important;
        user-select: none !important;
    }
    /* Hide native radio input element visually without breaking DOM click dispatch */
    [data-testid="stSidebar"] div[role="radiogroup"] label input[type="radio"] {
        position: absolute !important;
        opacity: 0 !important;
        width: 1px !important;
        height: 1px !important;
        margin: -1px !important;
        padding: 0 !important;
        border: 0 !important;
        clip: rect(0 0 0 0) !important;
        pointer-events: none !important;
    }
    /* Hide ONLY the circular radio dot */
    [data-testid="stSidebar"] div[role="radiogroup"] label > div > div:first-child:not([data-testid="stMarkdownContainer"]) {
        display: none !important;
    }
    /* Pass all clicks through children directly to the interactive label card */
    [data-testid="stSidebar"] div[role="radiogroup"] label * {
        pointer-events: none !important;
    }
    /* Label wrapper div should display flex to align text nicely */
    [data-testid="stSidebar"] div[role="radiogroup"] label > div {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        background: transparent !important;
    }
    /* Explicitly format text container */
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] {
        width: 100% !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] span {
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #D1CBD5 !important;
        letter-spacing: 0.01em !important;
        margin: 0 !important;
        line-height: 1.35 !important;
        visibility: visible !important;
        opacity: 1 !important;
        transition: color 0.18s ease !important;
    }
    /* Hover State */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(128, 0, 255, 0.16) !important;
        border-color: rgba(213, 162, 255, 0.45) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 16px rgba(128, 0, 255, 0.3) !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover [data-testid="stMarkdownContainer"] span {
        color: #FFFFFF !important;
    }
    /* Active / Checked State */
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked),
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-selected="true"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(128, 0, 255, 0.38) 0%, rgba(55, 12, 95, 0.6) 100%) !important;
        border: 1px solid #A855F7 !important;
        border-left: 4px solid #D5A2FF !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 22px rgba(128, 0, 255, 0.42), inset 0 0 12px rgba(128, 0, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-selected="true"] label [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-selected="true"] label [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] [data-testid="stMarkdownContainer"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    /* Click / Active press feedback */
    [data-testid="stSidebar"] div[role="radiogroup"] label:active {
        transform: scale(0.97) translateX(3px) !important;
        transition: transform 0.05s ease !important;
    }

    /* Smooth page content view transition */
    .main .block-container {
        animation: smoothPageFade 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    @keyframes smoothPageFade {
        0% {
            opacity: 0.72;
            transform: translateY(5px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Input & Select Controls */
    .stTextInput input, .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div {
        background-color: #160B22 !important;
        border-color: rgba(160, 80, 200, 0.3) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #8000FF !important;
        box-shadow: 0 0 10px rgba(128, 0, 255, 0.45) !important;
    }
    
    /* Brand Mark in Sidebar */
    .brand-mark {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 6px 0 14px 0;
        border-bottom: 1px solid rgba(160, 80, 200, 0.2);
        margin-bottom: 14px;
    }
    .brand-icon {
        background-color: #8000FF;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.05rem;
        width: 34px;
        height: 34px;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        letter-spacing: -0.03em;
        box-shadow: 0 0 16px rgba(128, 0, 255, 0.6);
    }
    .brand-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .brand-subtext {
        font-size: 0.72rem;
        color: #D5A2FF;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    
    /* Tag Badges */
    .tag-promote { background-color: rgba(16, 185, 129, 0.16); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.38); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.76rem; }
    .tag-block   { background-color: rgba(239, 68, 68, 0.16); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.38); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.76rem; }
    .tag-ignore  { background-color: rgba(156, 163, 175, 0.14); color: #9CA3AF; border: 1px solid rgba(156, 163, 175, 0.3); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.76rem; }
    .tag-review  { background-color: rgba(245, 158, 11, 0.16); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.38); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.76rem; }
    .tag-neutral { background-color: rgba(128, 0, 255, 0.16); color: #D5A2FF; border: 1px solid rgba(128, 0, 255, 0.38); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.76rem; }
    
    /* Sidebar Navigation item custom styling */
    div[data-testid="stSidebarNav"] { display: none; }
    
    /* Clean button styling */
    .stButton>button {
        background-color: #8000FF !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(180, 100, 255, 0.4) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem;
        box-shadow: 0 2px 12px rgba(128, 0, 255, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #921AFF !important;
        box-shadow: 0 4px 20px rgba(128, 0, 255, 0.65) !important;
        transform: translateY(-1px);
    }
    
    .stDownloadButton>button {
        background-color: #1A0D28 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(160, 80, 200, 0.35) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton>button:hover {
        background-color: #26133B !important;
        border-color: #8000FF !important;
        color: #D5A2FF !important;
        box-shadow: 0 2px 14px rgba(128, 0, 255, 0.3) !important;
    }
    
    /* Modal Dialog Overrides */
    div[data-baseweb="modal"] > div, div[role="dialog"] {
        background-color: #0E0717 !important;
        border: 1px solid rgba(160, 80, 200, 0.35) !important;
        border-radius: 14px !important;
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.85), 0 0 30px rgba(128, 0, 255, 0.25) !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="modal"] header, div[role="dialog"] header, div[role="dialog"] h2 {
        color: #FFFFFF !important;
    }
    div[data-baseweb="modal"] button[aria-label="Close"], div[role="dialog"] button[aria-label="Close"] {
        color: #D5A2FF !important;
    }

    /* Chat Messages inside Copilot */
    div[data-testid="stChatMessage"] {
        background-color: #140A1F !important;
        border: 1px solid rgba(160, 80, 200, 0.22) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stChatMessage"] * {
        color: #E2DCF0 !important;
    }
    div[data-testid="stChatMessage"] strong, div[data-testid="stChatMessage"] h1, div[data-testid="stChatMessage"] h2, div[data-testid="stChatMessage"] h3, div[data-testid="stChatMessage"] h4 {
        color: #FFFFFF !important;
    }
    div[data-testid="stChatMessage"] code {
        background-color: #200E33 !important;
        color: #D5A2FF !important;
        border: 1px solid rgba(160, 80, 200, 0.3) !important;
        padding: 2px 5px !important;
        border-radius: 4px !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 10px !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: #160B22 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(160, 80, 200, 0.35) !important;
        border-radius: 8px !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #8000FF !important;
        box-shadow: 0 0 12px rgba(128, 0, 255, 0.4) !important;
    }
</style>
"""

def inject_custom_css() -> None:
    """Injects the custom design system stylesheet into the active Streamlit app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

