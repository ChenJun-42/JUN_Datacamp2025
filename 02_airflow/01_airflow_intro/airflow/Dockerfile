FROM apache/airflow:2.10.5

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

USER root

RUN apt-get update -qq && \
    apt-get install -y -qqq curl gnupg && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
        | tee /etc/apt/sources.list.d/google-cloud-sdk.list > /dev/null && \
    apt-get update -qq && \
    apt-get install -y -qqq google-cloud-sdk && \
    rm -rf /var/lib/apt/lists/* && \
    gcloud --version


WORKDIR $AIRFLOW_HOME

COPY scripts /opt/airflow/scripts
RUN chmod +x /opt/airflow/scripts/*

USER $AIRFLOW_UID