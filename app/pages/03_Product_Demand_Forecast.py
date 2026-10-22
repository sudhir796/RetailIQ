import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.express as px

# We need to make sure the app directory is in path to import st_helper
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from st_helper import set_premium_page_config, render_page_header

set_premium_page_config("Product Demand", page_icon="📦")

render_page_header(
    title="Product Demand Forecast",
    subtitle="Model predicted unit demand vs. actual weekly units sold per item or category.",
    icon="📦",
    color="blue-70"
)

DEMAND_PRED_PATH = r"d:\RetailIQ\data\processed\demand_predictions.csv"

# Error Handling
if not os.path.exists(DEMAND_PRED_PATH):
    st.error("Error: Demand predictions dataset (demand_predictions.csv) was not found. Please run pipelines first.")
else:
    df_demand = pd.read_csv(DEMAND_PRED_PATH)
    df_demand['Date'] = pd.to_datetime(df_demand['Date'])
    
    # Model details in sidebar
    st.sidebar.subheader("Model Information")
    st.sidebar.markdown("""
    - **Algorithm:** XGBoost Regressor
    - **Key Test Metrics:**
      - **Overall RMSE:** 2.55
      - **Overall MAE:** 1.98 units
    - **Accuracy by Category (MAE):**
      - **Fashion:** 2.00 units
      - **Electronics:** 2.25 units
      - **Home Goods:** 2.47 units
    """)

    # Grid Layout: Left for Controls & Top List, Right for Chart
    col_left, col_right = st.columns([1, 1.8])

    with col_left:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("Filter Configurations")
        slice_type = st.radio("Slice data by:", ["Individual Product ID", "Product Category"])
        
        if slice_type == "Individual Product ID":
            all_products = sorted(df_demand['ProductID'].unique())
            selected_prod = st.selectbox("Select Product ID", all_products)
            plot_df = df_demand[df_demand['ProductID'] == selected_prod].sort_values('Date')
            title_str = f"Weekly Units Sold: Product {selected_prod}"
        else:
            all_categories = sorted(df_demand['Category'].unique())
            selected_cat = st.selectbox("Select Category", all_categories)
            plot_df = df_demand[df_demand['Category'] == selected_cat].groupby('Date').agg(
                ActualUnitsSold=('ActualUnitsSold', 'sum'),
                PredictedUnitsSold=('PredictedUnitsSold', 'sum')
            ).reset_index()
            title_str = f"Weekly Category Volume: {selected_cat}"
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-container section-tinted">', unsafe_allow_html=True)
        st.subheader("🔥 Top 5 High-Demand Products")
        top_products = df_demand.groupby(['ProductID', 'Category', 'SubCategory'])['PredictedUnitsSold'].mean().reset_index()
        top_products = top_products.sort_values(by='PredictedUnitsSold', ascending=False).head(5)
        st.dataframe(
            top_products.style.format({'PredictedUnitsSold': '{:.2f} units/wk'}),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card-container" style="height: 615px;">', unsafe_allow_html=True)
        st.subheader("Demand Prediction Comparison Chart")
        
        # Plot filled area/line chart
        fig = px.area(
            plot_df,
            x='Date',
            y=['ActualUnitsSold', 'PredictedUnitsSold'],
            labels={'value': 'Units Sold', 'variable': 'Legend'},
            title=title_str,
            template='plotly_dark'
        )
        fig.update_traces(line_width=2.5)
        
        # Add peak annotation
        peak_date = plot_df.loc[plot_df['ActualUnitsSold'].idxmax()]['Date']
        peak_val = plot_df['ActualUnitsSold'].max()
        fig.add_annotation(
            x=peak_date,
            y=peak_val,
            text=f"Peak: {peak_val:.1f} units",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-30,
            bgcolor="#1e293b",
            bordercolor="#00b4d8",
            borderwidth=1,
            borderpad=4,
            font=dict(color="#f8fafc", size=10)
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Outfit',
            hovermode='x unified',
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
