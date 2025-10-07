from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import matplotlib.pyplot as plt

PG_CONN_ID = 'postgres_conn'

default_args = {
    'owner': 'kiwilytics',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}
def get_conn():
    hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    return hook.get_conn()

#Task 1: fetching sales data
def fetch_order_data():
    conn = get_conn()
    query= """
        select o.orderdate::date as sale_date, od.productid, p.productname, od.quantity, p.price
        from orders o
        join order_details od on o.orderid = od.orderid 
        join products p on od.productid = p.productid 
    """
    df = pd.read_sql(query,conn)
    df.to_csv("/home/kiwilytics/airflow_assignment/outputs/sales_data.csv", index= False)


#Task 2: Calculating revenue per day by SQL
#Calculate_Total_Revenue_per_day_SQL = """
#    select  o.orderdate , sum(p.price * od.quantity ) as total_revenue
#    from orders o 
#    join order_details od on o.orderid = od.orderid
#    join products p  on od.productid = p.productid 
#    group by o.orderdate 
#    order by o.orderdate;
#"""

#Task 2: Calculating revenue per day
def calculating_daily_revenue():
    df = pd.read_csv("/home/kiwilytics/airflow_assignment/outputs/sales_data.csv")
    df["Total_Revenue"] = df["price"] * df["quantity"]
    revenue_per_day = df.groupby("sale_date")["Total_Revenue"].sum()
    revenue_per_day.to_csv("/home/kiwilytics/airflow_assignment/outputs/Revenue_Per_Day.csv")

#Task 3: visulaizing the data using matplotlib
def visualizing_revenue_per_day():
    df = pd.read_csv("/home/kiwilytics/airflow_assignment/outputs/Revenue_Per_Day.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    plt.figure(figsize=(10,6))
    plt.plot(df["sale_date"], df["Total_Revenue"], marker="o", linestyle="-")
    plt.title("Total Revenue Per Day")
    plt.xlabel("Date")
    plt.ylabel("Total Revenue")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    outputpath = "/home/kiwilytics/airflow_assignment/outputs/Total_Revenue_Per_Day.png"
    plt.savefig(outputpath)

with DAG(
    dag_id = "daily_sales_revenue_analysis",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= "@daily",
    catchup=False,
    description="Compute and visualize daily revenue using pandas and matplotlib in airflow",
) as dag:
    task_fetch_data = PythonOperator(
        task_id='fetch_order_data',
        python_callable=fetch_order_data,
    )

    task_process_revenue = PythonOperator(
        task_id = 'calculating_daily_revenue',
        python_callable= calculating_daily_revenue,
    )

    task_plot_revenue= PythonOperator(
        task_id='visualizing_revenue_per_day',
        python_callable=visualizing_revenue_per_day,
    )

    task_fetch_data >> task_process_revenue >> task_plot_revenue