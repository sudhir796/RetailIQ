import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import sys
import plotly.express as px

# We need to make sure the app directory is in path to import st_helper
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from st_helper import set_premium_page_config, render_page_header, apply_metric_styling

set_premium_page_config("Sales Forecasting", page_icon="🔮")

render_page_header(
    title="Sales Prediction Engine",
    subtitle="Reconstruct feature vectors and predict daily sales revenue using XGBoost.",
    icon="🔮",
    color="blue-70"
)

MODEL_PATH = r"d:\RetailIQ\models\sales_forecast_model.pkl"
FORECAST_DATA_PATH = r"d:\RetailIQ\data\processed\forecast_dataset.csv"

# Error Handling
if not os.path.exists(MODEL_PATH) or not os.path.exists(FORECAST_DATA_PATH):
    st.error("Error: Sales forecasting model or processed dataset is missing. Please run pipelines first.")
else:
    # Sidebar stats
    st.sidebar.subheader("Model Information")
    st.sidebar.markdown("""
    - **Algorithm:** XGBoost Regressor
    - **Key Test Metrics:**
      - **RMSE:** \$10,267.82
      - **MAE:** \$8,117.92
      - **MAPE:** 54.50%
    """)

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
    df_fore = pd.read_csv(FORECAST_DATA_PATH)
    df_fore['Date'] = pd.to_datetime(df_fore['Date'])

    # Setup Columns: Left for Input, Right for Output
    col_left, col_right = st.columns([1, 2.2])

    with col_left:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("Select Forecast Target")
        max_date = df_fore['Date'].max()
        selected_date = st.date_input("Target Date", max_date.date())
        selected_ts = pd.Timestamp(selected_date)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Spinner during prediction logic
        with st.spinner("Reconstructing feature vector and running prediction..."):
            features = [
                'DayOfWeek', 'Month', 'Quarter', 'Year', 'IsWeekend', 'IsHolidaySeason',
                'Revenue_Lag_7', 'Volume_Lag_7', 'Revenue_Lag_30', 'Volume_Lag_30',
                'Revenue_RollMean_7', 'Volume_RollMean_7', 'Revenue_RollMean_30', 'Volume_RollMean_30'
            ]
            
            def get_holiday_flag(dt):
                y = dt.year
                ny = (dt >= pd.Timestamp(f'{y-1}-12-31') and dt <= pd.Timestamp(f'{y}-01-02'))
                ind = (dt >= pd.Timestamp(f'{y}-07-03') and dt <= pd.Timestamp(f'{y}-07-05'))
                tg = (dt >= pd.Timestamp(f'{y}-11-20') and dt <= pd.Timestamp(f'{y}-11-30'))
                xm = (dt >= pd.Timestamp(f'{y}-12-15') and dt <= pd.Timestamp(f'{y}-12-26'))
                return 1 if (ny or ind or tg or xm) else 0

            day_of_week = selected_ts.weekday()
            month = selected_ts.month
            quarter = (month - 1) // 3 + 1
            year = selected_ts.year
            is_weekend = 1 if day_of_week in [5, 6] else 0
            is_holiday = get_holiday_flag(selected_ts)
            
            if selected_ts in df_fore['Date'].values:
                row = df_fore[df_fore['Date'] == selected_ts].iloc[0]
                lag_rev_7 = row['Revenue_Lag_7']
                lag_vol_7 = row['Volume_Lag_7']
                lag_rev_30 = row['Revenue_Lag_30']
                lag_vol_30 = row['Volume_Lag_30']
                roll_rev_7 = row['Revenue_RollMean_7']
                roll_vol_7 = row['Volume_RollMean_7']
                roll_rev_30 = row['Revenue_RollMean_30']
                roll_vol_30 = row['Volume_RollMean_30']
                actual_rev = row['TotalRevenue']
                status_label = "Historical Data"
            else:
                last_row = df_fore.iloc[-1]
                lag_rev_7 = last_row['Revenue_RollMean_7']
                lag_vol_7 = last_row['Volume_RollMean_7']
                lag_rev_30 = last_row['Revenue_RollMean_30']
                lag_vol_30 = last_row['Volume_RollMean_30']
                roll_rev_7 = last_row['Revenue_RollMean_7']
                roll_vol_7 = last_row['Volume_RollMean_7']
                roll_rev_30 = last_row['Revenue_RollMean_30']
                roll_vol_30 = last_row['Volume_RollMean_30']
                actual_rev = None
                status_label = "Extrapolated"
                
            input_vector = [
                day_of_week, month, quarter, year, is_weekend, is_holiday,
                lag_rev_7, lag_vol_7, lag_rev_30, lag_vol_30,
                roll_rev_7, roll_vol_7, roll_rev_30, roll_vol_30
            ]
            
            input_vector = [0 if np.isnan(v) else v for v in input_vector]
            pred_rev = float(model.predict(np.array([input_vector]))[0])

        # Render KPI Cards via st.metric + st_extras styling
        kp1, kp2, kp3 = st.columns(3)
        with kp1:
            st.metric(label="Predicted Revenue", value=f"${pred_rev:,.2f}")
        with kp2:
            val_str = f"${actual_rev:,.2f}" if actual_rev is not None else "N/A"
            st.metric(label="Actual Revenue", value=val_str)
        with kp3:
            st.metric(label="Prediction Status", value=status_label)
            
        apply_metric_styling()

        if actual_rev is None:
            st.markdown("""
                <div class="flag-box">
                    💡 <b>Future Date Extrapolation:</b> Feature values were automatically constructed using the final rolling momentum statistics. 
                    Expect larger error bands than the test set MAE (\$8,117.92).
                </div>
            """, unsafe_allow_html=True)

    # Line Chart below in full-width container (Alternating visual section - Tinted)
    st.write("")
    st.markdown('<div class="card-container section-tinted">', unsafe_allow_html=True)
    st.subheader("Historical vs Predicted Trend Comparison")
    
    # 60-day history for chart
    history_subset = df_fore.iloc[-60:].copy()
    historical_preds = []
    for idx, row in history_subset.iterrows():
        vec = [row[f] for f in features]
        vec = [0 if np.isnan(v) else v for v in vec]
        historical_preds.append(float(model.predict(np.array([vec]))[0]))
    history_subset['Predicted'] = historical_preds
    
    if actual_rev is None:
        future_row = pd.DataFrame({
            'Date': [selected_ts],
            'TotalRevenue': [np.nan],
            'Predicted': [pred_rev]
        })
        plot_df = pd.concat([history_subset[['Date', 'TotalRevenue', 'Predicted']], future_row])
    else:
        plot_df = history_subset[['Date', 'TotalRevenue', 'Predicted']]
        
    # Standardize comparison chart as filled area with soft gradient
    fig = px.area(
        plot_df,
        x='Date',
        y=['TotalRevenue', 'Predicted'],
        labels={'value': 'Revenue ($)', 'variable': 'Legend'},
        template="plotly_dark"
    )
    fig.update_traces(line_width=2.5)
    
    # Peak point annotation
    peak_date = history_subset.loc[history_subset['TotalRevenue'].idxmax()]['Date']
    peak_val = history_subset['TotalRevenue'].max()
    fig.add_annotation(
        x=peak_date,
        y=peak_val,
        text=f"Peak: ${peak_val:,.2f}",
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
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
