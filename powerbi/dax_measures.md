# RetailIQ DAX Measure Library

This document provides ready-to-paste DAX measures organized by dashboard page. 

---

## Standalone Calendar Table Setup
Before creating measures, create a continuous date table by clicking **New Table** in Modeling and pasting:
```dax
Calendar = 
VAR MinDate = MIN(fact_sales[Date])
VAR MaxDate = MAX(fact_sales[Date])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "MonthNum", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "Weekday", FORMAT([Date], "DDDD"),
    "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, 1, 0)
)
```

---

## Page 1 — Executive Dashboard

### 1. Total Revenue
* **DAX Code:**
  ```dax
  Total Revenue = SUMX(fact_sales, fact_sales[OrderValue] * (1 - fact_sales[Discount]))
  ```
* **Explanation:** Calculates total gross revenue post-discount across all completed transactions.
* **Target Visual:** Card, Line Chart (sales over time).

### 2. Total Profit
* **DAX Code:**
  ```dax
  Total Profit = SUMX(fact_sales, (fact_sales[OrderValue] * (1 - fact_sales[Discount])) * fact_sales[ProfitMargin])
  ```
* **Explanation:** Calculates total gross profit post-discount (Revenue * Profit Margin).
* **Target Visual:** Card, KPI indicator.

### 3. Total Orders
* **DAX Code:**
  ```dax
  Total Orders = DISTINCTCOUNT(fact_sales[TransactionID])
  ```
* **Explanation:** Count of unique transactional order IDs.
* **Target Visual:** Card.

### 4. Average Order Value (AOV)
* **DAX Code:**
  ```dax
  Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
  ```
* **Explanation:** Calculates average basket revenue per order.
* **Target Visual:** Card.

### 5. Month-over-Month Growth %
* **DAX Code:**
  ```dax
  MoM Growth % = 
  VAR CurrentMonthRevenue = [Total Revenue]
  VAR PreviousMonthRevenue = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
  RETURN
  DIVIDE(CurrentMonthRevenue - PreviousMonthRevenue, PreviousMonthRevenue, 0)
  ```
* **Explanation:** Calculates the percentage change in revenue compared to the previous calendar month.
* **Target Visual:** KPI Indicator with trend-axis.

---

## Page 2 — Sales Dashboard

### 1. YoY Sales Growth %
* **DAX Code:**
  ```dax
  YoY Sales Growth % = 
  VAR CurrentRevenue = [Total Revenue]
  VAR PriorYearRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))
  RETURN
  DIVIDE(CurrentRevenue - PriorYearRevenue, PriorYearRevenue, 0)
  ```
* **Explanation:** Calculates revenue growth percentage relative to the same period in the prior year.
* **Target Visual:** Gauge, Card.

---

## Page 3 — Customer Dashboard

### 1. Customers per Segment
* **DAX Code:**
  ```dax
  Customers per Segment = COUNT(dim_customers[CustomerID])
  ```
* **Explanation:** Counts customers belonging to each cluster segment.
* **Target Visual:** Bar Chart, Donut Chart (legend: `ClusterName`).

### 2. Repeat Customer Rate
* **DAX Code:**
  ```dax
  Repeat Customer Rate = 
  VAR ValidCustomers = CALCULATE(COUNTROWS(dim_customers), dim_customers[IsNegativeTenure] = 0)
  VAR RepeatCustomers = CALCULATE(COUNTROWS(dim_customers), dim_customers[IsNegativeTenure] = 0 && dim_customers[Frequency] > 1)
  RETURN
  DIVIDE(RepeatCustomers, ValidCustomers, 0)
  ```
* **Explanation:** Calculates the percentage of active (tenure-valid) customers who have placed more than one order.
* **Target Visual:** Card (formatted as %).

### 3. Average Tenure
* **DAX Code:**
  ```dax
  Average Tenure Days = CALCULATE(AVERAGE(dim_customers[Tenure]), dim_customers[IsNegativeTenure] = 0)
  ```
* **Explanation:** Calculates average customer lifetime tenure in days, strictly excluding negative-tenure anomalies.
* **Target Visual:** Card.

---

## Page 4 — Product Dashboard

### 1. Top 10 Products by Revenue
* **DAX Code:**
  ```dax
  Top 10 Products Revenue = 
  CALCULATE(
      [Total Revenue],
      TOPN(10, ALLSELECTED(dim_products), [Total Revenue], DESC)
  )
  ```
* **Explanation:** Limits revenue display to the top 10 products.
* **Target Visual:** Bar Chart.

### 2. Category Profit Margin %
* **DAX Code:**
  ```dax
  Category Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
  ```
* **Explanation:** Calculates gross profit margin ratio at product category grain.
* **Target Visual:** Matrix, Column Chart.

---

## Page 5 — Regional Dashboard

### 1. Store Count
* **DAX Code:**
  ```dax
  Store Count = DISTINCTCOUNT(dim_stores[StoreID])
  ```
* **Explanation:** Count of operational retail store locations.
* **Target Visual:** Card, Map Bubble Size.

---

## Page 6 — Forecast Dashboard

### 1. Actual Sales (Test Set)
* **DAX Code:**
  ```dax
  Actual Sales (Test) = SUM(fact_forecast[ActualRevenue])
  ```
* **Explanation:** Sum of actual sales recorded during the model's test period.
* **Target Visual:** Line Chart (value y-axis).

### 2. Forecasted Sales (Test Set)
* **DAX Code:**
  ```dax
  Forecasted Sales (Test) = SUM(fact_forecast[PredictedRevenue])
  ```
* **Explanation:** Sum of XGBoost predictions during the test period.
* **Target Visual:** Line Chart (secondary y-axis).

### 3. Forecast MAPE (Card)
* **DAX Code:**
  ```dax
  Forecast MAPE = 
  AVERAGEX(
      FILTER(fact_forecast, fact_forecast[ActualRevenue] > 0),
      DIVIDE(ABS(fact_forecast[ActualRevenue] - fact_forecast[PredictedRevenue]), fact_forecast[ActualRevenue])
  )
  ```
* **Explanation:** Calculates the Mean Absolute Percentage Error dynamically across the test predictions.
* **Target Visual:** Card (formatted as %).

---

## Page 7 — AI Insights Dashboard

### 1. High-Demand Weekly Volume
* **DAX Code:**
  ```dax
  High Demand Predicted Volume = SUM(fact_demand[PredictedUnitsSold])
  ```
* **Explanation:** Aggregated weekly prediction volume for demand forecasting.
* **Target Visual:** Table/Matrix (rows: `ProductID`, `Category`).
