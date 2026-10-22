import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.express as px

# We need to make sure the app directory is in path to import st_helper
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from st_helper import set_premium_page_config, render_page_header

set_premium_page_config("Customer Segments", page_icon="👥")

render_page_header(
    title="Customer Behavioral Segments",
    subtitle="Evaluate client clusters created via K-Means and profile individual customer metrics.",
    icon="👥",
    color="blue-70"
)

DIM_CUSTOMERS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "powerbi", "data", "dim_customers.csv"))
SEG_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "segmentation_dataset.csv"))

# Error Handling
if not os.path.exists(DIM_CUSTOMERS_PATH) and not os.path.exists(SEG_DATA_PATH):
    st.error("Error: Customer dataset was not found. Please run pipelines first.")
else:
    if os.path.exists(DIM_CUSTOMERS_PATH):
        df_cust = pd.read_csv(DIM_CUSTOMERS_PATH)
    else:
        df_cust = pd.DataFrame()

    # Enrich from segmentation_dataset.csv if RFM metrics or IsNegativeTenure are missing
    if os.path.exists(SEG_DATA_PATH):
        df_seg = pd.read_csv(SEG_DATA_PATH)
        if df_cust.empty:
            df_cust = df_seg
        else:
            missing_cols = [c for c in df_seg.columns if c not in df_cust.columns]
            if missing_cols:
                df_cust = df_cust.merge(df_seg[['CustomerID'] + missing_cols], on='CustomerID', how='left')

    if 'IsNegativeTenure' not in df_cust.columns:
        df_cust['IsNegativeTenure'] = (df_cust['Tenure'] < 0).astype(int) if 'Tenure' in df_cust.columns else 0
    
    # 1. Segment Profiles Section
    st.subheader("Segment Distribution & Centroids")
    
    seg_counts = df_cust.groupby(['Cluster', 'ClusterName']).size().reset_index(name='Size')
    df_valid = df_cust[df_cust['IsNegativeTenure'] == 0]
    
    seg_profiles = df_valid.groupby(['Cluster', 'ClusterName']).agg(
        AvgRecency=('Recency', 'mean'),
        AvgFrequency=('Frequency', 'mean'),
        AvgMonetary=('Monetary', 'mean'),
        AvgAOV=('AOV', 'mean'),
        AvgTenure=('Tenure', 'mean'),
        AvgAge=('Age', 'mean')
    ).reset_index()
    
    profiles_merged = seg_counts.merge(seg_profiles, on=['Cluster', 'ClusterName'], how='left')
    
    col1, col2 = st.columns([1, 1.8])
    with col1:
        st.markdown('<div class="card-container" style="height: 400px;">', unsafe_allow_html=True)
        fig_donut = px.pie(
            profiles_merged,
            values='Size',
            names='ClusterName',
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Outfit',
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-container" style="height: 400px; overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown("**Segment Profile Means (Excludes Anomalous Tenure):**")
        st.dataframe(
            profiles_merged.style.format({
                'AvgRecency': '{:.1f} days',
                'AvgFrequency': '{:.1f} orders',
                'AvgMonetary': '${:,.2f}',
                'AvgAOV': '${:,.2f}',
                'AvgTenure': '{:.1f} days',
                'AvgAge': '{:.1f} yrs'
            }, na_rep='N/A (Excluded)'),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 2. Individual Customer Profiler Section (Visual Rhythm: Tinted Background Section)
    st.write("")
    st.markdown("---")
    st.subheader("🔍 Individual Account Profiler")
    
    st.markdown('<div class="card-container section-tinted">', unsafe_allow_html=True)
    all_cust_ids = sorted(df_cust['CustomerID'].unique())
    selected_id = st.selectbox("Select Customer ID for Analysis", all_cust_ids)
    
    cust_row = df_cust[df_cust['CustomerID'] == selected_id].iloc[0]
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value" style="font-size: 1.8rem; padding-top: 8px;">{cust_row['FirstName']} {cust_row['LastName']}</div>
                <div class="kpi-label">Customer Name</div>
            </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value" style="font-size: 1.8rem; padding-top: 8px; color: #ffa600;">{cust_row['ClusterName']}</div>
                <div class="kpi-label">Segment Group</div>
            </div>
        """, unsafe_allow_html=True)
    with p3:
        if cust_row['IsNegativeTenure'] == 1:
            tenure_str = "Excluded (Anomalous)"
        else:
            tenure_str = f"{int(cust_row['Tenure']):,} days"
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value" style="font-size: 1.8rem; padding-top: 8px;">{tenure_str}</div>
                <div class="kpi-label">Customer Tenure</div>
            </div>
        """, unsafe_allow_html=True)
        
    if cust_row['IsNegativeTenure'] == 1:
        st.markdown("""
            <div class="flag-box">
                ⚠️ <b>Anomalous Join Date Flagged:</b> This customer is one of the 5 negative-tenure cases (JoinDate is after their first order due to generation artifacts). 
                To safeguard the model's distance calculations, they were excluded from K-Means training inputs and automatically mapped to Cluster -1.
            </div>
        """, unsafe_allow_html=True)
        
    seg_definitions = {
        "High-Value Premium VIPs": "Premium tier clients who make large order transactions (AOV over $4.7k) and contribute the highest overall monetary values.",
        "Core Tech Loyalists": "Highly active clients who place frequent orders (averaging 36+ orders) and purchase electronics items repeatedly.",
        "Moderate Fashion Shoppers": "Older demographical shoppers who purchase apparel items occasionally with mid-level basket values.",
        "Lapsed High-Tenure Clients": "Disengaged long-standing accounts who haven't placed an order in over 550 days. High risk of churn.",
        "Excluded (Anomalous Registration)": "Accounts with system date anomalies (order dates predating registration dates). Mapped separately for integrity."
    }
    
    st.write("")
    st.markdown(f"**Segment Description:** *{seg_definitions.get(cust_row['ClusterName'], 'Unknown segment profile')}*")
    
    st.write("")
    st.markdown("**Account Transaction Details:**")
    detail_cols = [c for c in ['CustomerID', 'Gender', 'Age', 'City', 'JoinDate', 'Recency', 'Frequency', 'Monetary', 'AOV'] if c in df_cust.columns]
    st.dataframe(df_cust[df_cust['CustomerID'] == selected_id][detail_cols], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
