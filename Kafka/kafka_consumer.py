import os
from kafka import KafkaConsumer
import pickle
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import time

load_dotenv()  # Carga las variables de entorno desde el archivo .env

# Leer las variables de entorno para la conexión a la base de datos
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')  
db_port = os.getenv('DB_PORT')   

# Cargar el modelo desde el archivo PKL
with open('Model/Regression_Model.pkl', 'rb') as file:
    best_model = pickle.load(file)

# Configurar el Kafka consumer
consumer = KafkaConsumer('regression_model', bootstrap_servers='localhost:9092', 
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')), 
                         consumer_timeout_ms=10000)  # Timeout para esperar más mensajes

# Crear una lista para almacenar los resultados de las predicciones
predictions = []

# Conexión a la base de datos PostgreSQL usando las variables de entorno
connection = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=3000
)

# Crear un cursor para ejecutar las operaciones SQL
cursor = connection.cursor()

# Crear la tabla en PostgreSQL si no existe, incluyendo las nuevas columnas al final
create_table_query = """
    CREATE TABLE IF NOT EXISTS happiness_score_prediction (
        Country VARCHAR(255),
        Year INT,
        Economy_GDP_per_Capita FLOAT,
        Social_support FLOAT,
        Health_Life_Expectancy FLOAT,
        Freedom FLOAT,
        Trust_Government_Corruption FLOAT,
        Generosity FLOAT,
        Happiness_Score FLOAT,
        Predicted_Happiness_Score FLOAT
    );
"""
# Ejecutar la consulta para crear la tabla
cursor.execute(create_table_query)
connection.commit()
print("Tabla 'happiness_score_prediction' creada o ya existe.")

# Contador de filas procesadas
rows_processed = 0
total_rows = 234  # Último 30% de las filas que debe procesar el consumidor

# Recibir los mensajes del Kafka topic
for message in consumer:
    if rows_processed >= total_rows:
        break  # Detener el consumidor después de procesar 234 filas
    
    row = message.value  # Los datos recibidos
    
    # Convertir los datos a DataFrame para hacer predicciones
    input_data = pd.DataFrame([row])
    X_new = input_data.drop(columns=['Happiness Score'])
    
    # Realizar la predicción
    y_pred = best_model.predict(X_new)
    
    # Agregar la predicción y la verdadera 'Happiness Score'
    row['Predicted_Happiness_Score'] = y_pred[0]
    predictions.append(row)
    
    rows_processed += 1

    # Si ya hemos recibido los datos y se acumularon 10 mensajes, guardamos en PostgreSQL
    if len(predictions) >= 10:  # Ajusta el número según tu caso
        # Convertir la lista de predicciones a un DataFrame
        result_df = pd.DataFrame(predictions)
        
        # Insertar los resultados en la base de datos PostgreSQL
        insert_query = """
            INSERT INTO happiness_score_prediction (Country, Year, Economy_GDP_per_Capita, Social_support, 
                                           Health_Life_Expectancy, Freedom, Trust_Government_Corruption, 
                                           Generosity, Happiness_Score, Predicted_Happiness_Score)
            VALUES %s
        """
        
        # Preparamos los datos a insertar como una lista de tuplas
        data_to_insert = [
            (row['Country'], row['Year'], row['Economy (GDP per Capita)'], row['Social support'], 
             row['Health (Life Expectancy)'], row['Freedom'], row['Trust (Government Corruption)'], 
             row['Generosity'], row['Happiness Score'], row['Predicted_Happiness_Score']) 
            for index, row in result_df.iterrows()
        ]
        
        # Usar execute_values para insertar múltiples filas de manera eficiente
        execute_values(cursor, insert_query, data_to_insert)
        
        # Hacer commit para guardar los cambios en la base de datos
        connection.commit()
        
        # Imprimir mensaje de éxito
        print("Datos guardados en la base de datos PostgreSQL.")
        
        # Borrar las predicciones acumuladas para continuar con el siguiente conjunto
        predictions = []

# Confirmación cuando todos los datos hayan sido procesados
if rows_processed == total_rows:
    print("Todos los datos han sido guardados correctamente.")
else:
    print(f"Aún faltan {total_rows - rows_processed} datos para ser procesados.")
