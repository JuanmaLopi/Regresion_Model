from kafka import KafkaProducer
import pandas as pd
import json
import time

# Configure the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Load the data
data = pd.read_csv('data/Model_Data.csv')

# Get the last 30% of the rows
last_30_percent = data.tail(int(len(data) * 0.3))  # Last 30% of the rows

# Send the rows to the Kafka Consumer
for index, row in last_30_percent.iterrows():
    message = row.to_dict()  # Convert each row into a dictionary
    producer.send('regression_model', message)  # Send to the Kafka topic
    producer.flush()  # Ensure the message is sent

    time.sleep(1)



print(f"Sent {len(last_30_percent)} rows to the Kafka consumer.")
