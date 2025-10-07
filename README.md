# ETL Pipeline with Airflow, PostgreSQL and Python
# Overview
This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using:
- Airflow: For Orchestration
- PostgreSQL: As The Database
- Python (Pandas, Matplotlib): For Data Processing and Visualization

The pipeline extracts data from PostgreSQL containing data about orders, their details and their product names, runs SQL queries and transformations using Pandas and generates:
- sales_data.csv: csv file that contains the needed order details for transformations
- Revenue_Per_Day.csv: csv file after transforming the data and extracting the needed result which is the total revenues per day
- Total_Revenue_Per_Day.png: a chart visualizing the relationship between each day and the revenue in that exact day

 ## 🧩 Components
### 1. **Airflow DAG (`Airflow_Assignment.py`)**
- Connects to PostgreSQL using Airflow `PostgresHook`
- Runs SQL queries
- Calls Python functions for data wrangling
- Exports results as CSV and PNG

### 2. **Data Processing**
- Uses Pandas for cleaning and analysis
- Generates a sales summary and visualization

### 3. **Visualization**
- Creates charts using Matplotlib (e.g., Total_Revenue_Per_Day.png)

Technologies Used:
-Python
-Pandas, Matplotlib
-PostgreSQL
-Apache Airflow
