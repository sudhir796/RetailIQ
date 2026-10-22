# Power BI Desktop Build Checklist

Follow this step-by-step checklist to assemble the RetailIQ Analytics Dashboard in Power BI Desktop.

---

## Phase 1: Data Import
1. Open **Power BI Desktop**.
2. Click **Get Data** &rarr; **Text/CSV**.
3. Import the following files from `powerbi/data/`:
   - `dim_customers.csv`
   - `dim_products.csv`
   - `dim_stores.csv`
   - `fact_sales.csv`
   - `fact_forecast.csv`
   - `fact_demand.csv`
   - `fact_model_summary.csv`
4. Click **Transform Data** to open Power Query Editor:
   - Verify that all ID columns (`CustomerID`, `ProductID`, `StoreID`, `TransactionID`) are formatted as **Text** across all tables.
   - Verify that date columns (`Date`, `BirthDate`, `JoinDate`, `Week`) are formatted as **Date**.
   - Verify numeric fields (`OrderValue`, `Quantity`, `Discount`, `ProfitMargin`, `ActualRevenue`, `PredictedRevenue`) are formatted as **Decimal Number** or **Whole Number**.
5. Click **Close & Apply**.

---

## Phase 2: Create Date Table & Establish Model Relationships
1. In the Report View, navigate to Modeling &rarr; **New Table**.
2. Paste the `Calendar` table DAX formula from [dax_measures.md](file:///d:/RetailIQ/powerbi/dax_measures.md) to generate the date dimension.
3. Switch to the **Model View** (relationship canvas):
   - Power BI may auto-detect some links. Delete incorrect links and manually build these exact relationships:
     * `dim_customers[CustomerID]` (1) &rarr; `fact_sales[CustomerID]` (*) [Single direction]
     * `dim_products[ProductID]` (1) &rarr; `fact_sales[ProductID]` (*) [Single direction]
     * `dim_stores[StoreID]` (1) &rarr; `fact_sales[StoreID]` (*) [Single direction]
     * `Calendar[Date]` (1) &rarr; `fact_sales[Date]` (*) [Single direction]
     * `Calendar[Date]` (1) &rarr; `fact_forecast[Date]` (*) [Single direction]
     * `dim_products[ProductID]` (1) &rarr; `fact_demand[ProductID]` (*) [Both directions filter]
   - Keep the standalone reference table `fact_model_summary` disconnected.

---

## Phase 3: Create DAX Measures
Create a dedicated measure table for organization:
1. Click **Enter Data** on the Home tab, name the table `_Measures`, and click Load.
2. For each measure listed in [dax_measures.md](file:///d:/RetailIQ/powerbi/dax_measures.md):
   - Right-click `_Measures` &rarr; **New Measure**.
   - Paste the DAX code.
   - Set formatting (e.g. currency `$` for Revenue/Profit/AOV, percent `%` for MoM/YoY growth/MAPE, whole number for Counts).

---

## Phase 4: Build Report Pages

### Page 1 — Executive Dashboard
* **Purpose:** High-level summary of company performance.
* **Suggested Layout:**
  - Cards along the top: `[Total Revenue]`, `[Total Profit]`, `[Total Orders]`, `[Average Order Value]`.
  - Line Chart (middle): `[Total Revenue]` by `Calendar[YearMonth]` showing monthly trend.
  - KPI Visual: `[Total Revenue]` with trend axis `Calendar[MonthName]` and Target `MoM Growth %`.

### Page 2 — Sales Dashboard
* **Purpose:** Analyzing revenue trends and time comparisons.
* **Suggested Layout:**
  - Card: `[YoY Sales Growth %]`.
  - Line Chart: `[Total Revenue]` (Y-axis) by `Calendar[MonthName]` (X-axis) with `Calendar[Year]` as Legend (compares 2024 vs 2025 seasonal curves).
  - Donut Chart: `[Total Revenue]` by `dim_products[Category]`.

### Page 3 — Customer Dashboard
* **Purpose:** Client segments and lifecycle metrics.
* **Suggested Layout:**
  - Donut Chart: `[Customers per Segment]` by `dim_customers[ClusterName]`.
  - Matrix Table: Rows: `dim_customers[ClusterName]`. Columns: Average Age, Average `[Average Tenure Days]`, Average AOV, Total Monetary.
  - Card: `[Repeat Customer Rate]` (respects tenure exclusions).

### Page 4 — Product Dashboard
* **Purpose:** Item level performance.
* **Suggested Layout:**
  - Clustered Bar Chart: `[Top 10 Products Revenue]` by `dim_products[ProductName]`.
  - Scatter Chart: X-Axis: `[Category Profit Margin %]`. Y-Axis: `[Total Revenue]`. Play Axis: `dim_products[ProductName]`. (Highlights high-revenue vs high-margin items).

### Page 5 — Regional Dashboard
* **Purpose:** Geographical performance.
* **Suggested Layout:**
  - Map Visual: Location: `dim_stores[City]`. Bubble size: `[Total Revenue]`. Color: `dim_stores[Region]`.
  - Clustered Column Chart: `[Total Revenue]` and `[Category Profit Margin %]` (Dual Y-Axis) by `dim_stores[Region]`.

### Page 6 — Forecast Dashboard
* **Purpose:** XGBoost sales model test-period validation.
* **Suggested Layout:**
  - Line Chart: `[Actual Sales (Test)]` and `[Forecasted Sales (Test)]` plotted by `Calendar[Date]` (shows model alignment over the final 8 weeks).
  - Card: `[Forecast MAPE]` (formatted as percentage, shows 54.50%).

### Page 7 — AI Insights Dashboard
* **Purpose:** Model summaries and weekly demand predictions.
* **Suggested Layout:**
  - Matrix Table: Standalone reference from `fact_model_summary` (displays K-Means Silhouette, Forecast MAPE, Demand MAE, and takeaways).
  - Table Visual: `ProductID`, `Category`, `SubCategory`, `[High Demand Predicted Volume]` sorted descending (shows products with top forecasted demand for stock orders).
  - Column Chart: `[Customers per Segment]` showing cluster sizes.
