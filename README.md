# Sales Data Analysis Dashboard (Basic)

A beginner-friendly sales dashboard built with Python, Streamlit, Pandas and Plotly.

## Features
- Total revenue, total profit, order count and product count
- Category and region filters
- Revenue by category and region charts
- Product performance chart
- Sales records table
- Download filtered sales data as CSV

## Requirements
- Python 3.9 or later
- Internet connection for the first package installation

## Run on Windows

Open Command Prompt in this folder and run:

```cmd
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## Optional summary script

```cmd
python analysis.py
```

## Dataset note
The included CSV contains 10 illustrative sample records. It is a demonstration dataset, not actual business data. Replace `dataset/superstore.csv` with your own data while keeping the same column names:
`Order_ID, Product, Category, Region, Sales, Profit`.

This basic version intentionally uses CSV only. It does not require MySQL, a `.env` file, database credentials, or a forecasting model.
