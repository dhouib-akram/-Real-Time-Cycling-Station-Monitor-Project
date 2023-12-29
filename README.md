# Real-Time Cycling Station Monitor

## Overview

The Real-Time Cycling Station Monitor is a system designed to track and analyze the status of cycling stations. It utilizes a data pipeline comprising Kafka, Spark, Elasticsearch, and Kibana to process and visualize real-time data. This enables users to identify cycling stations with no available bikes and understand usage patterns.

## System Architecture

- **Kafka**: Ingests real-time data from cycling stations.
- **Spark**: Processes and analyzes the data.
- **Elasticsearch**: Stores and indexes the processed data.
- **Kibana**: Visualizes insights on an interactive dashboard, including a map highlighting stations with no available bikes.

## Prerequisites

- Docker Desktop: Ensure Docker Desktop is installed and running on your system.
- Python: Ensure Python is installed for running the Kafka producer script.

## Setup and Running Instructions

### 1. Build and Run Containers

Before running the services, you need to build the Docker images and initialize the containers.

```sh
docker-compose build
docker-compose up -d

```
This will set up Kafka, Spark, Elasticsearch, and Kibana.

2. Copy Spark Consumer Script
Transfer the pyspark_consumer.py script to the Spark master container.

```sh
docker cp -L ./pyspark_consumer.py spark-master:/opt/bitnami/spark/pyspark_consumer.py

```

3. Submit the Spark Job
Run the Spark job to start processing the streaming data.

```sh
docker-compose exec spark-master spark-submit \
--class consumer \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,org.elasticsearch:elasticsearch-spark-30_2.12:7.17.0,commons-httpclient:commons-httpclient:3.1 \
pyspark_consumer.py



```
4. Run Kafka Producer Script
Execute the Kafka producer script to send data to the Kafka topic.

```sh

python ./kafka_producer.py

```

Ensure to replace the apiKey in the kafka_producer.py script with your own API key.

5. Visualize Data in Kibana
Access Kibana by visiting http://localhost:5601. Set up an index pattern for Elasticsearch data and create a dashboard with a map visualization to view the status of the cycling stations.

Conclusion
This project provides a comprehensive solution for monitoring cycling stations in real-time. By leveraging a robust data pipeline and advanced visualization tools, it delivers critical insights promptly and effectively. Customize the system according to your specific needs and enjoy a deeper understanding of cycling station dynamics.