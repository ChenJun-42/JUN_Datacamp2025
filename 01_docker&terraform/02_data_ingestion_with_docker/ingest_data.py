import os  # Import the os module to interact with the operating system
import argparse  # Import argparse to handle command-line arguments
from time import time  # Import time to measure execution time
import pandas as pd  # Import pandas for data handling
from sqlalchemy import create_engine  # Import create_engine to interact with PostgreSQL

def main(params):
    # Retrieve command-line arguments
    user = params.user  
    password = params.password  
    host = params.host  
    port = params.port  
    db = params.db  
    table_name = params.table_name  
    url = params.url  

    # Determine the file name based on the URL (supports both regular CSV and compressed CSV files)
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Download the CSV file from the provided URL and save it locally
    os.system(f"wget {url} -O {csv_name}")

    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read the CSV file in chunks of 100,000 rows to optimize memory usage
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # Read the first chunk of data
    df = next(df_iter)

    # Convert datetime columns from string format to proper datetime format
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Create an empty table in PostgreSQL with the correct schema
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Insert the first chunk of data into the table
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Loop through the remaining chunks and insert them into the database
    while True: 
        try:
            t_start = time()  # Start timing
            
            df = next(df_iter)  # Get the next chunk of data
            
            # Convert datetime columns again for the new chunk
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # Insert the chunk into the PostgreSQL table
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()  # End timing
            print('Inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:  # When there are no more chunks left
            print("Finished ingesting data into the PostgreSQL database")
            break

if __name__ == '__main__':
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='Username for PostgreSQL')
    parser.add_argument('--password', required=True, help='Password for PostgreSQL')
    parser.add_argument('--host', required=True, help='Host address of PostgreSQL server')
    parser.add_argument('--port', required=True, help='Port number for PostgreSQL')
    parser.add_argument('--db', required=True, help='Database name')
    parser.add_argument('--table_name', required=True, help='Target table name in the database')
    parser.add_argument('--url', required=True, help='URL of the CSV file to be downloaded')

    # Parse command-line arguments
    args = parser.parse_args()

    # Execute the main function with the provided arguments
    main(args)
