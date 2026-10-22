# RetailIQ - AI-Powered Retail Analytics & Demand Forecasting Platform

RetailIQ is an end-to-end retail intelligence platform that integrates customer, store, product, and sales data to perform advanced demand forecasting and predictive modeling. Built using a star-schema design, the platform ingests multi-table retail transactional data, establishes referential integrity, and utilizes machine learning models to help retail business managers forecast inventory demands and optimize retail operations.

---

## Folder Structure

```text
RetailIQ/
├── data/
│   ├── raw/           # Untouched source files (CSVs/Excel)
│   ├── cleaned/       # Cleaned datasets ready for analysis
│   └── processed/     # Processed SQLite database (retailiq.db) and prediction outputs
├── notebooks/         # Jupyter notebooks for ingestion, cleaning, EDA, features, and modeling
├── models/            # Predictive models and saved serialization artifacts (.pkl)
├── powerbi/           # Power BI reports, data model mapping, DAX package, and checklist
│   └── data/          # Consolidated import-ready CSVs for Power BI Desktop
├── app/               # Application code (Streamlit UI/backend APIs)
│   └── pages/         # Streamlit multipage application routes
├── reports/           # Generated PDF, static analysis charts, and model evaluation summary
├── requirements.txt   # Python dependency list
├── run_all_notebooks.py # Pipeline automation script
└── README.md          # Project documentation
```

---

## Setup & How to Run

Follow these steps to configure your environment and run the pipeline and the web application.

### 1. Set Up Virtual Environment
Create and activate a python virtual environment:

**PowerShell (Windows):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Git Bash / macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies
Install all required libraries inside the active virtual environment:
```bash
pip install -r requirements.txt
```

---

### 3. Run the Automated Notebooks Pipeline
To execute all 8 notebooks sequentially (refreshing the SQLite database, cleaning datasets, performing EDA, engineering features, training models, and generating summaries), run:
```bash
python run_all_notebooks.py
```

---

### 4. Run the Streamlit Web Application
To launch the interactive multi-page business demo, execute the following command:
```bash
streamlit run app/streamlit_app.py
```
This will open the Streamlit web portal in your default browser at `http://localhost:8501`.

---

### 5. Build Power BI Dashboards
To construct the Power BI dashboard, open **Power BI Desktop** and:
1. Import all CSV files inside `powerbi/data/`.
2. Follow the model relations mapping in [data_model.md](file:///d:/RetailIQ/powerbi/data_model.md).
3. Implement copy-paste measures from [dax_measures.md](file:///d:/RetailIQ/powerbi/dax_measures.md).
4. Lay out report pages following the detailed [build_checklist.md](file:///d:/RetailIQ/powerbi/build_checklist.md).
