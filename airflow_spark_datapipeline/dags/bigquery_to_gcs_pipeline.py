from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

GCP_PROJECT = "seventh-league-447908-t0"
GCS_BUCKET = "seventh-league-447908-t0--terra-bucket"
BQ_PUBLIC_DATASET = "bigquery-public-data.crypto_bitcoin"
TABLE_NAME = "transactions"

default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 5)
}

# PySpark processing function
def process_bitcoin_transactions(**kwargs):

    spark = SparkSession.builder \
        .appName("ProcessBitcoinTransactions") \
        .config("spark.jars", "/usr/lib/jvm/gcs-connector-hadoop3-latest.jar") \
        .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
        .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
        .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/.google/credentials/google_credentials.json") \
        .config("spark.hadoop.fs.gs.project.id", "seventh-league-447908-t0") \
        .getOrCreate()

    hadoop_conf = spark._jsc.hadoopConfiguration()

    hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")

    hadoop_conf.set("google.cloud.auth.service.account.json.keyfile", "/.google/credentials/google_credentials.json")

    hadoop_conf.set("fs.gs.project.id", "seventh-league-447908-t0")

    process_date = kwargs["ds"]
    input_path = f"gs://{GCS_BUCKET}/raw/crypto_bitcoin/{process_date}/*.parquet"
    output_path = f"gs://{GCS_BUCKET}/processed/crypto_bitcoin/{process_date}/"

    df = spark.read.parquet(input_path)

    processed_df = df \
        .withColumn("input", explode(col("inputs"))) \
        .withColumn("output", explode(col("outputs"))) \
        .select(
            "block_timestamp",
            "transaction_id",
            col("input.addresses").alias("sender"),
            col("output.addresses").alias("receiver"),
            col("output.value").alias("amount_btc")
        ) \
        .filter(col("amount_btc") > 0)

    processed_df.write.parquet(output_path, mode="overwrite")

    spark.stop()

dag = DAG(
    dag_id="bigquery_to_gcs_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=True,
)

export_to_gcs = BigQueryInsertJobOperator(
    task_id="export_to_gcs",
    configuration={
        "query": {
            "query": f"""
                EXPORT DATA OPTIONS(
                  uri='gs://{GCS_BUCKET}/raw/crypto_bitcoin/{{{{ ds }}}}/*.parquet',
                  format='PARQUET',
                  overwrite=true
                ) AS
                SELECT *
                FROM `{BQ_PUBLIC_DATASET}.{TABLE_NAME}`
                WHERE DATE(block_timestamp) = '{{{{ ds }}}}'
            """,
            "useLegacySql": False,
        }
    },
    dag=dag,
)

process_transactions = PythonOperator(
    task_id="process_transactions",
    python_callable=process_bitcoin_transactions,
    provide_context=True,
    dag=dag,
)

export_to_gcs >> process_transactions