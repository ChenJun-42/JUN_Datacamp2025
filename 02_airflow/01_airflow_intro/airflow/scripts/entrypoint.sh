#!/usr/bin/env bash

export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT=${AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT}

airflow db upgrade

airflow users create \
    -r Admin \
    -u admin \
    -p admin \
    -e admin@example.com \
    -f admin \
    -l airflow

airflow webserver --port 8080
