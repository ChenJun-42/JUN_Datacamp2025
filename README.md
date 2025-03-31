# JUN_Datacamp2025

Week1 conclusion: 
  (1) Core Topics Covered
    Docker Basics:
        Setting up and running containers
        Using docker-compose to manage multi-container environments
        Understanding volumes and networking in Docker
    PostgreSQL Data Injection:
        Running PostgreSQL inside a Docker container
        Connecting to PostgreSQL using pgcli
        Importing data from CSV files into a database
    SQL for Data Analysis
        Writing basic SQL queries (SELECT, WHERE, JOIN)
        Performing aggregations (GROUP BY, COUNT, SUM)
        Creating and managing database schemas
  (2) Extended Topics & Insights
    Docker Networking & Ports:
        Exposing PostgreSQL on port 5432 and connecting from VS Code
    Persistent Storage in Docker: 
        Using Docker volumes to retain database data
    Database Optimization:
        Indexing, performance tuning, and best practices
    Cloud Integration:
        Running PostgreSQL in a cloud environment like Google Cloud SQL
    ETL Pipelines:
        Extracting, transforming, and loading data into PostgreSQL

  week2 conclusion:
    (1) I chose apache airflow as data orchastration tool, instead of Kestra;
    (2) Introduction to Apache Airflow
      What is Apache Airflow and why it is used for workflow orchestration
      Understanding DAGs (Directed Acyclic Graphs) and their role in defining workflows
      How Airflow schedules and executes tasks
    (3) Installing & Setting Up Airflow
      Running Airflow locally using docker-compose
      Understanding Airflow components:
        Scheduler (manages DAG execution)
        Executor (runs tasks)
        Web UI (for monitoring and managing DAGs)
        Metadata Database (stores DAG runs and task states)
    (4) Creating & Running DAGs
      Writing a basic DAG in Python
      Defining tasks using Python functions & operators
      Using PythonOperator, BashOperator, and DummyOperator
      Understanding task dependencies (set_upstream() / set_downstream())
    (5) Working with Airflow Operators
      Common Operators:
        BashOperator: Run shell commands
        PythonOperator: Execute Python functions
        PostgresOperator: Run SQL queries on PostgreSQL
        Sensor: Wait for external events or files
    (6) anaging & Monitoring Workflows
          Running DAGs manually vs. scheduled execution
          Using Airflow Web UI to monitor DAGs and troubleshoot issues
          Checking logs to debug failed tasks
    (7) Scheduling in Airflow
        Using cron expressions and timedelta for scheduling DAGs
        Understanding backfilling vs. catchup behavior
        Managing start_date, end_date and execution_date
