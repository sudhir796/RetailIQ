import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

def set_premium_page_config(title, page_icon="📊"):
    # Set page configuration with page_icon parameter
    st.set_page_config(
        page_title=f"RetailIQ - {title}",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject Custom CSS for Premium Glassmorphism Theme and Visual Rhythm
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Font and overall scroll styling */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Premium Hero Banner (Gradient Header) */
        .premium-hero {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            padding: 35px 40px;
            border-radius: 20px;
            color: #ffffff;
            margin-bottom: 28px;
            border-left: 8px solid #00b4d8;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        .premium-hero h1 {
            margin: 0;
            font-weight: 700;
            font-size: 2.8rem;
            letter-spacing: -1px;
            color: #f8fafc;
        }
        .premium-hero p {
            margin: 10px 0 24px 0;
            font-size: 1.15rem;
            color: #94a3b8;
        }
        .hero-metric-box {
            background: rgba(0, 180, 216, 0.08);
            border: 1px solid rgba(0, 180, 216, 0.25);
            padding: 16px 24px;
            border-radius: 12px;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(0, 180, 216, 0.1);
        }
        .hero-metric-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 1px;
        }
        .hero-metric-val {
            font-size: 2.4rem;
            font-weight: 700;
            color: #00b4d8;
            margin-top: 4px;
        }
        
        /* Warning and Alert Box Styles */
        .flag-box {
            background: rgba(245, 158, 11, 0.08);
            border-left: 4px solid #f59e0b;
            padding: 16px;
            border-radius: 10px;
            color: #f59e0b;
            margin-bottom: 24px;
            font-weight: 400;
            font-size: 0.95rem;
            border-top: 1px solid rgba(245, 158, 11, 0.1);
            border-right: 1px solid rgba(245, 158, 11, 0.1);
            border-bottom: 1px solid rgba(245, 158, 11, 0.1);
        }
        .flag-box code {
            color: #fbbf24;
            background: rgba(0, 0, 0, 0.2);
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        /* Container Card wrapping for layout groups */
        .card-container {
            background: rgba(30, 41, 59, 0.35);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.15);
            margin-bottom: 24px;
        }
        
        /* Visual Rhythm Alternating Section Colors */
        .section-tinted {
            background: rgba(0, 180, 216, 0.03) !important;
            border: 1px solid rgba(0, 180, 216, 0.08) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle, icon="📊", color="blue-70"):
    colored_header(
        label=f"{icon} {title}",
        description=subtitle,
        color_name=color
    )
    add_vertical_space(1)

def apply_metric_styling():
    style_metric_cards(
        background_color="#1e293b",
        border_left_color="#00b4d8",
        border_color="rgba(255,255,255,0.05)",
        box_shadow="0 6px 20px rgba(0,0,0,0.3)"
    )
