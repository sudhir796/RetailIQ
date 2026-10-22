import streamlit as st
import pandas as pd
import os
import plotly.express as px
from st_helper import set_premium_page_config, render_page_header, apply_metric_styling

# Set premium styling
set_premium_page_config("Executive Overview", page_icon="📊")

# Data paths
CLEAN_SALES_PATH = r"d:\RetailIQ\data\cleaned\clean_sales.csv"

# Error handling
if not os.path.exists(CLEAN_SALES_PATH):
    st.error(f"Error: Cleansed sales dataset was not found at `{CLEAN_SALES_PATH}`. Please run the data pipelines first.")
else:
    # Load dataset
    df = pd.read_csv(CLEAN_SALES_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate KPIs
    # Post-discount revenue = OrderValue * (1 - Discount)
    df['Revenue'] = df['OrderValue'] * (1 - df['Discount'])
    total_rev = df['Revenue'].sum()
    total_profit = (df['Revenue'] * df['ProfitMargin']).sum()
    total_orders = df['TransactionID'].nunique()
    aov = total_rev / total_orders
    
    # 1. Premium Hero Banner at the top
    st.markdown(f"""
        <div class="premium-hero">
            <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: #00b4d8; font-weight: 700; margin-bottom: 8px;">RetailIQ Platform</div>
            <h1>AI-Powered Retail Analytics</h1>
            <p>Predictive demand forecasting, customer segmentation, and enterprise operational intelligence.</p>
            <div class="hero-metric-box">
                <div class="hero-metric-label">Lifetime Gross Revenue</div>
                <div class="hero-metric-val">${total_rev:,.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Section Header & Spacing
    render_page_header(
        title="Executive Performance metrics",
        subtitle="Business-critical operational indicators and profit statistics.",
        icon="⚡",
        color="blue-70"
    )

    # 3. KPI Grid Layout using st.metric + st_extras styling
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    with kpi2:
        st.metric(label="Total Orders", value=f"{total_orders:,}")
    with kpi3:
        st.metric(label="Average Order Value", value=f"${aov:,.2f}")
        
    apply_metric_styling()
    st.write("")
    
    # Data Quality Box
    st.markdown("""
        <div class="flag-box">
            ⚠️ <b>Data Quality Caveat:</b> 19.9% of transactions (996 records) occurred prior to the customer's official join date due to data generation artifact.
            These are highlighted via <code>pre_registration_flag</code>. 5 customers have negative lifetime tenure as a result and are excluded from customer lifecycle metric calculations.
        </div>
    """, unsafe_allow_html=True)
    
    # 4. Alternating Section (Tinted Background) for Visual Rhythm
    st.markdown('<div class="card-container section-tinted">', unsafe_allow_html=True)
    st.subheader("📈 Monthly Sales Volume & Seasonality")
    
    # Group by Year-Month
    df['YearMonth'] = df['Date'].dt.to_period('M').dt.start_time
    monthly_df = df.groupby('YearMonth')['Revenue'].sum().reset_index()
    
    # Filled Area Chart (Soft Gradient Theme)
    fig = px.area(
        monthly_df,
        x='YearMonth',
        y='Revenue',
        labels={'Revenue': 'Revenue ($)', 'YearMonth': 'Month'},
        template='plotly_dark'
    )
    fig.update_traces(line_color='#00b4d8', fillcolor='rgba(0, 180, 216, 0.12)', line_width=3)
    
    # Annotation on the Peak Month
    peak_row = monthly_df.loc[monthly_df['Revenue'].idxmax()]
    peak_date = peak_row['YearMonth']
    peak_val = peak_row['Revenue']
    
    fig.add_annotation(
        x=peak_date,
        y=peak_val,
        text=f"Peak: ${peak_val:,.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-35,
        bgcolor="#1e293b",
        bordercolor="#00b4d8",
        borderwidth=1,
        borderpad=4,
        font=dict(color="#f8fafc", size=11)
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Outfit',
        hovermode='x unified',
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
