import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""


init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'

BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc-data-lake-bucketname")


def upload_to_gcs(bucket, object_name, local_file):

    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, color):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = f"{i+1:02d}"

        # csv file_name
        file_name = f"{color}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{color}/{file_name}"
        r = requests.get(request_url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        print(f"Local: {file_name}")

        # read it back into a parquet file
        df = pd.read_csv(file_name, compression='gzip')
        file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")

        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{color}/{file_name}", file_name)
        print(f"GCS: {color}/{file_name}")


# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')
web_to_gcs('2019', 'fhv')
