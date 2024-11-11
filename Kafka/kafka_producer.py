from kafka import KafkaProducer
import pandas as pd
import json

# Configurar el Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Cargar los datos
data = pd.read_csv('data/Model_Data.csv')

# Obtener el último 30% de las filas
last_30_percent = data.tail(int(len(data) * 0.3))  # Último 30% de las filas

# Enviar las filas al Kafka Consumer
for index, row in last_30_percent.iterrows():
    message = row.to_dict()  # Convertir cada fila en un diccionario
    producer.send('regression_model', message)  # Enviar al Kafka topic
    producer.flush()  # Asegurarse de que se haya enviado el mensaje

print(f"Enviadas {len(last_30_percent)} filas al Kafka consumer.")

