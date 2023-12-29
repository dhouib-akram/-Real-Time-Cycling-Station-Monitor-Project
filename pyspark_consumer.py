from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *
from elasticsearch import Elasticsearch

# Create an Elasticsearch client
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])

# Define the index name
index_name = "bike"

# Check if the Elasticsearch index exists
if es.indices.exists(index=index_name):
    # Delete the index
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' has been deleted.")
else:
    print(f"Index '{index_name}' does not exist.")

# Define the mapping for your Elasticsearch index
mapping = {
    "mappings": {
        "properties": {
        "numbers": { "type": "integer" },
        "contract_name": { "type": "text" },
        "banking": { "type": "text" },
        "bike_stands": { "type": "integer" },
        "available_bike_stands": { "type": "integer" },
        "available_bikes": { "type": "integer" },
        "address": { "type": "text" },
        "status": { "type": "text" },
        "position": {
            "type": "geo_point"
        },
        "timestamps": { "type": "text" }
        }
    }
    }

# Create the Elasticsearch index with the specified mapping
es.indices.create(index=index_name, body=mapping)



schema = StructType([
# Define the schema of your Kafka messages 
    StructField("numbers", IntegerType(), True),
    StructField("contract_name", StringType(), True),
    StructField("banking", StringType(), True),
    StructField("bike_stands", IntegerType(), True),
    StructField("available_bike_stands", IntegerType(), True),
    StructField("available_bikes", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("status", StringType(), True),
    StructField("position", StructType([
        StructField("lat", DoubleType(), True),
        StructField("lon", DoubleType(), True)
    ]), True),
    StructField("timestamps", StringType(), True),
])

# Create a SparkSession
spark = SparkSession.builder \
    .appName("consumer") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from the Kafka topic 'bike'
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "bike") \
    .load()

# Deserialize the JSON from the Kafka message
json_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Print the schema of the DataFrame
json_df.printSchema()

# Show the data read from Kafka on the console
query = json_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
data = json_df.writeStream \
        .format("org.elasticsearch.spark.sql") \
        .outputMode("append")\
        .option("es.nodes", "elasticsearch")\
        .option("es.port", "9200")\
        .option("es.resource", "bike")\
        .option("es.nodes.wan.only", "true") \
        .option("checkpointLocation", "tmp/") \
        .start()

query.awaitTermination()
