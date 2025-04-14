FROM apache/airflow:2.10.5

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

USER root

RUN apt-get update -qq && \
    apt-get install -y procps && \
    apt-get install -y -qqq curl gnupg && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update -qq && \
    apt-get install -y -qqq google-cloud-sdk && \
    rm -rf /var/lib/apt/lists/* && \
    gcloud --version

RUN apt-get update \
&& apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
&& apt-get autoremove -yqq --purge \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

COPY scripts /opt/airflow/scripts
RUN chmod +x /opt/airflow/scripts/*
USER airflow

WORKDIR $AIRFLOW_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark==2.1.3

USER $AIRFLOW_UID