from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, to_date

def main():
    spark = SparkSession.builder \
        .appName("ProcessBitcoinTransactions") \
        .getOrCreate()

    GCS_BUCKET = spark.conf.get("spark.gcs.bucket", "default-bucket-name")

    process_date = spark.conf.get("spark.process.date", "2025-04-05")
    input_path = f"gs://{GCS_BUCKET}/raw/crypto_bitcoin/{process_date}/*.parquet"
    df = spark.read.parquet(input_path)

    processed_df = df \
        .withColumn("input", explode(col("inputs"))) \
        .withColumn("output", explode(col("outputs"))) \
        .select(
            "block_timestamp",
            col("input.addresses").alias("sender"),
            col("output.addresses").alias("receiver"),
            col("output.value").alias("amount_btc")
        ) \
        .filter(col("amount_btc") > 0)

    output_path = f"gs://{GCS_BUCKET}/processed/crypto_bitcoin/{process_date}/"
    processed_df.write.parquet(output_path, mode="overwrite")

    spark.stop()

if __name__ == "__main__":
    main()