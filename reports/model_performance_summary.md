# Model Performance Summary

This document consolidates the evaluation metrics and business insights for the three machine learning models built for the RetailIQ platform. These results are used in the Power BI AI Insights dashboard and the final project report.

## Model Performance Summary Table

| Model | Task | Algorithm | Key Metric(s) | Test Period/Method | One-line takeaway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Daily Sales Forecast** | Sales forecasting | XGBoost Regressor | RMSE: 10,267.82<br>MAE: 8,117.92<br>MAPE (excl. 0s): 54.50% | Last 8 weeks (56 days)<br>Time-based split | Model captures general demand levels, but suffers from high daily variance (MAPE 54.5%), meaning it is better for weekly/monthly aggregation than precise daily orders. |
| **Customer Segmentation** | Behavioral customer clustering | K-Means (K=4) | Silhouette Score: 0.266<br>Inertia: 543.08 | Train set (excl. negative tenure)<br>Full-dataset evaluation | Creates highly distinct and actionable segments (Premium VIPs, Tech Loyalists, Fashion Shoppers, Lapsed), though silhouette score (0.266) suggests moderate cluster overlap. |
| **Product Demand Prediction** | Weekly product demand forecasting | XGBoost Regressor | RMSE: 2.55<br>MAE: 1.98 units | Last 8 weeks (weekly)<br>Time-based split | Predicts weekly product demand with an average error of 1.98 units. Best on Fashion (MAE 2.00) and struggles slightly on Home Goods (MAE 2.47) due to high stochasticity. |

## Model Performance Insights

### 1. Daily Sales Forecast
The daily forecasting model achieves an MAE of $8,117.92 against an average daily revenue of roughly $20,000. It successfully models weekly patterns (day-of-week) and mid-term seasonality (rolling averages). However, daily variance is high, resulting in a MAPE of 54.50%.
* **Downstream Guidance:** The model is reliable for high-level aggregate forecasting (weekly or monthly demand planning) but should not be used as a precise predictor for daily order fulfillment volumes.

### 2. Customer Segmentation
K-Means successfully isolated four primary buyer clusters based on customer RFM profiles and demographics. We identified **High-Value Premium VIPs** (high monetary, high AOV), **Core Tech Loyalists** (high frequency, tech-skewed), **Moderate Fashion Shoppers** (moderate frequency and spend), and **Lapsed High-Tenure Clients** (long inactivity periods).
* **Downstream Guidance:** The silhouette score of 0.266 indicates that while cluster centroids are highly distinct, there is moderate overlap at the boundaries. The business should use these segments for targeted campaign themes, but avoid highly rigid operational exclusions based solely on K-Means boundaries.

### 3. Product Demand Prediction
Product-level demand is modeled at a weekly frequency to reduce zero-demand sparsity. The model yields an overall MAE of 1.98 units. 
* **Downstream Guidance:** The model achieves the best accuracy in the **Fashion** category (MAE: 2.00 units), which has lower unit costs and higher volume. It struggles slightly with **Home Goods** (MAE: 2.47 units), where demand is more sparse and unit values are higher. This model is ideal for guiding baseline replenishment parameters but requires an safety stock buffer for high-value/low-volume products.
