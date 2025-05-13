# 📊 Stock Price Analysis Workflow (Airflow + dbt + Snowflake + Superset)

This project showcases a modern, automated data pipeline built to analyze historical stock price movements using a blend of orchestration, transformation, cloud warehousing, and business intelligence tools.

---

## 🔍 Project Summary

The objective is to automate the full analytics process — from fetching stock data to deriving meaningful insights. The pipeline applies technical indicators such as moving averages and RSI to help interpret price momentum and trend direction for stocks like AAPL and GOOGL.

---

## 🛠️ Tools and Technologies Used

- **Apache Airflow** – Orchestrates ETL and ELT pipelines on a schedule
- **yFinance** – Fetches historical stock data via API
- **Snowflake** – Cloud warehouse for storing and managing both raw and processed data
- **dbt (Data Build Tool)** – Transforms raw data into analytics-ready models with version control and testing
- **Apache Superset** – Creates interactive and visual dashboards for data exploration

---

## 🗂️ Folder Structure

```
.
├── airflow_dags/
│   ├── lab2_ETL.py              # ETL DAG for stock data extraction and loading
│   └── lab2_ELT.py              # ELT DAG for dbt transformation trigger
├── dbt/
│   ├── models/
│   │   ├── staging/             # Raw to intermediate layer
│   │   └── analytics/           # Business-level logic and metrics
│   ├── snapshots/               # Tracks metric changes over time
│   └── schema.yml               # Schema and test definitions
├── screenshots/
│   ├── airflow_etl_dag.png
│   ├── airflow_dbt_dag.png
│   ├── dbt_models.png
│   └── superset_dashboard.png
└── README.md
```

---

## 🔄 Pipeline Breakdown

### ⚙️ 1. Data Extraction & Loading (ETL)
- An Airflow DAG pulls historical stock prices for AAPL and GOOGL using `yfinance`.
- After light cleansing, the data is inserted into the `RAW.STOCK_PRICES` table in Snowflake.
- The process ensures repeatability and transaction safety.

### 🏗️ 2. Data Modeling & Metrics (ELT via dbt)
- dbt transforms raw stock data into insightful analytics models.
- Key metrics include:
  - 20-day and 50-day Moving Averages (MA20 & MA50)
  - Relative Strength Index (RSI)
- Snapshots monitor changes in key metrics.
- dbt tests validate schema integrity and data expectations.

### 📊 3. Data Visualization (Superset)
- Superset displays analytical dashboards:
  - RSI-based heatmaps
  - Time-series line charts for moving averages
  - Histograms for price movement analysis
- Filters allow users to slice data by stock ticker and date ranges interactively.

---

## 👨‍💻 Contributors

- **Sai Kiran Reddy Pothuganti**  
- **Vivek Varma Rudraraju**

---

## 📚 Resources & References

- [Airflow Docs](https://airflow.apache.org/docs/)
- [dbt Docs](https://docs.getdbt.com/)
- [Snowflake Platform](https://www.snowflake.com)
- [Apache Superset](https://superset.apache.org)
- [yFinance Python Package](https://pypi.org/project/yfinance/)

---

## 📘 Academic Context

This project was developed as part of an academic curriculum involving advanced data engineering and analytics workflows using modern cloud and orchestration tools.
