import streamlit as st
import pandas as pd
import os
import sys

# We need to make sure the app directory is in path to import st_helper
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from st_helper import set_premium_page_config, render_page_header

set_premium_page_config("Model Performance", page_icon="🔍")

render_page_header(
    title="Model Performance & Self-Documentation",
    subtitle="A transparent evaluation summary detailing the reliability, metrics, and caveats of our AI models.",
    icon="🔍",
    color="blue-70"
)

SUMMARY_PATH = r"d:\RetailIQ\reports\model_performance_summary.csv"

# Error Handling
if not os.path.exists(SUMMARY_PATH):
    st.error("Error: Model performance summary CSV was not found. Please run pipelines first.")
else:
    df_summary = pd.read_csv(SUMMARY_PATH)
    
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("Model Evaluation Summary Table")
    st.markdown("This table summarizes the core metrics across all three machine learning tasks built for RetailIQ:")
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    st.markdown('<div class="card-container section-tinted">', unsafe_allow_html=True)
    st.subheader("⚠️ Honest Deployment Guidance & Borderline Models")
    
    st.markdown("""
    To ensure the downstream dashboard and application are used responsibly, the business must respect the following caveats:
    
    1. **Daily Sales Forecast Volatility (High Daily Variance)**
       - **Observation:** The daily sales forecast model exhibits a **54.50% MAPE** (Mean Absolute Percentage Error) on the test set. 
       - **Meaning:** Daily sales are highly stochastic and noisy. **Do not use this model as a precise indicator for daily order fulfillment.**
       - **Better Use Case:** It is highly reliable for high-level aggregate trends (such as weekly/monthly store-level demand planning).
       
    2. **Customer Segmentation Boundary Overlaps**
       - **Observation:** The K-Means model (K=4) yielded a **0.266 Silhouette Score**.
       - **Meaning:** While the four centroids represent highly distinct customer profiles, there is moderate overlap at the cluster boundaries.
       - **Better Use Case:** Use these segments for targeted marketing themes, but avoid making rigid operational restrictions (e.g. blocking credit or account features) solely based on segment boundaries.
       
    3. **Product-Level Restocking Safety Buffers**
       - **Observation:** Weekly product demand prediction has an overall **MAE of 1.98 units**. However, error varies by category: **Fashion** is highly accurate (MAE 2.00 vs average demand 2.46), while **Home Goods** has larger relative error (MAE 2.47 vs average demand 2.88).
       - **Meaning:** Demand for Home items is more volatile.
       - **Better Use Case:** Include a larger safety stock buffer for Home products in inventory calculations compared to high-volume Apparel items.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
