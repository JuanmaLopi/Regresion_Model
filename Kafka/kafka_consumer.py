import os
from kafka import KafkaConsumer
import pickle
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import time

load_dotenv()  # Load environment variables from the .env file

# Read environment variables for the database connection
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')  
db_port = os.getenv('DB_PORT')   

# Load the model from the PKL file
with open('Model/Regression_Model.pkl', 'rb') as file:
    best_model = pickle.load(file)

# Configure the Kafka consumer
consumer = KafkaConsumer('regression_model', bootstrap_servers='localhost:9092', 
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')), 
                         consumer_timeout_ms=10000)  # Timeout to wait for more messages

# Create a list to store prediction results
predictions = []

# Connect to the PostgreSQL database using environment variables
connection = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=3000
)

# Create a cursor to execute SQL operations
cursor = connection.cursor()

# Create the table in PostgreSQL if it doesn't exist, including the new columns at the end
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
# Execute the query to create the table
cursor.execute(create_table_query)
connection.commit()
print("Table 'happiness_score_prediction' created or already exists.")

# Row counter
rows_processed = 0
total_rows = 234  # Last 30% of rows to process for the consumer

# Receive messages from the Kafka topic
for message in consumer:
    if rows_processed >= total_rows:
        break  # Stop the consumer after processing 234 rows
    
    row = message.value  # Received data
    
    # Convert data to DataFrame for predictions
    input_data = pd.DataFrame([row])
    X_new = input_data.drop(columns=['Happiness Score'])
    
    # Make the prediction
    y_pred = best_model.predict(X_new)
    
    # Add the prediction and the true 'Happiness Score'
    row['Predicted_Happiness_Score'] = y_pred[0]
    predictions.append(row)
    
    rows_processed += 1

    # If 10 messages have been received and accumulated, save to PostgreSQL
    if len(predictions) >= 10:  # Adjust the number as per your case
        # Convert the list of predictions to a DataFrame
        result_df = pd.DataFrame(predictions)
        
        # Insert the results into the PostgreSQL database
        insert_query = """
            INSERT INTO happiness_score_prediction (Country, Year, Economy_GDP_per_Capita, Social_support, 
                                           Health_Life_Expectancy, Freedom, Trust_Government_Corruption, 
                                           Generosity, Happiness_Score, Predicted_Happiness_Score)
            VALUES %s
        """
        
        # Prepare the data to insert as a list of tuples
        data_to_insert = [
            (row['Country'], row['Year'], row['Economy (GDP per Capita)'], row['Social support'], 
             row['Health (Life Expectancy)'], row['Freedom'], row['Trust (Government Corruption)'], 
             row['Generosity'], row['Happiness Score'], row['Predicted_Happiness_Score']) 
            for index, row in result_df.iterrows()
        ]
        
        # Use execute_values to efficiently insert multiple rows
        execute_values(cursor, insert_query, data_to_insert)
        
        # Commit to save changes to the database
        connection.commit()
        
        # Print success message
        print("Data saved to the PostgreSQL database.")
        
        # Clear the accumulated predictions to continue with the next set
        predictions = []
        
        time.sleep(1)


# Confirmation when all data has been processed
if rows_processed == total_rows:
    print("All data has been saved successfully.")
else:
    print(f"{total_rows - rows_processed} data points remain to be processed.")
