# HAPPINESS SCORE PREDICTION

---

This project aims to predict happiness indexes in various countries using machine learning techniques. To achieve this, exploratory data analysis, feature selection, real-time data streaming through Kafka, and information storage in a PostgreSQL database are applied.


---

## Table of Contents


---

1. [PROJECT DESCRIPTION](#1-project-description)
2. [REQUIREMENTS](#2-requirements)
3. [PROJECT STRUCTURE](#3-project-structure)
4. [ENVIRONMENT SETUP](#4-environment-setup)
5. [DATA PROCESSING](#5-data-processing)
6. [MODEL TRAINING](#6-model-training)
7. [KAFKA IMPLEMENTATION](#7-kafka-implementation)
8. [KAFKA OPERATION](#8-kafka-operation)
9. [EVIDENCES](#9-database-operation)
10. [CONCLUSIÓN](#10-conclusión)
11. [AUTHORS](#11-authors)
---

### 1. Project Description <a name="project-description"></a>

This project focuses on estimating the happiness level in different countries using factors such as income per capita, population health, individual freedom, and other elements. To carry it out:

- Happiness data collected over several years is analyzed.
- The most significant variables are selected.
- A regression model is trained.
- Apache Kafka is implemented to send real-time predictions.
- The results are stored in a PostgreSQL database.

---

### 2. Requirements <a name="requirements"></a>

For this project, various tools were used to assist with data processing, regression model training, real-time data streaming, and storing the necessary data. Below are the tools used in this project:

- Python 3.8 or higher (Programming language used for most of the code)
- Docker Desktop (Application to orchestrate and run Kafka containers)
- Apache Kafka (Used for data streaming)
- PostgreSQL (Database where predictions were stored)
- Pandas (Library used for data processing)
- Scikit-learn (Library used for model training)
- Matplotlib, Seaborn (Libraries used for correlation charts)
- Psycopg2 (Library for connecting to PostgreSQL)
- Dotenv (Library used for environment variables)

To install all required libraries, use the following command:

```bash
pip install kafka-python pandas scikit-learn matplotlib seaborn psycopg2 python-dotenv
```

All dependencies used are listed in the **requirements.txt** file.

---

### 3. Project Structure <a name="project-structure"></a>

The project is structured as follows:

```plaintext
├── data
│   ├── 2015.csv             # Raw data for 2015
│   ├── 2016.csv             # Raw data for 2016
│   ├── 2017.csv             # Raw data for 2017
│   ├── 2018.csv             # Raw data for 2018
│   ├── 2019.csv             # Raw data for 2019
│   └── model_data           # Model training data
│
├── Kafka
│   ├── kafka_producer.py       # Kafka producer code
│   └── kafka_consumer.py       # Kafka consumer code
│
├── Model
│   └── Regression_Model.pkl     # Regression model
│
├── Notebooks
│   ├── EDA.ipynb                  # Exploratory data analysis
│   └── model_training.ipynb       # Model training
│
├── src
│   ├── EDA.py                  # Scripts for exploratory data analysis
│   └── model_training.py       # Scripts for model training
│
├── .gitignore               # Git ignore configuration file
├── docker-compose.yml       # Docker Compose configuration file
├── README.md                # Main documentation file
└── requirements.txt         # List of project dependencies
```

#### Create Virtual Environment

To create a virtual environment to make the code run more efficiently:

Open a new terminal in Visual Studio Code and run the following code:

```bash
python -m venv .venv
```

This will create a virtual environment called .venv in the project root. To activate it, run the following command in the Visual Studio Code bash:

```bash
source .venv/scripts/activate
```

---

### 4. Environment Setup <a name="environment-setup"></a>

To connect to the database, in this case, PostgreSQL, there are certain parameters that need to be defined, which allow us to establish the connection. Therefore, a .env file should be created in the project root, where we will store our environment variables, which include the credentials used to connect to PostgreSQL.

DB_NAME= Your_Database_Name
DB_USER= Your_Username
DB_PASSWORD= Your_Database_Password
DB_HOST= Database_Host       # Typically, this is defined as LocalHost
DB_PORT= Database_Port       # The default port for PostgreSQL is 5432

---

### 5. Data Processing <a name="data-processing"></a>

For data processing, the Pandas library is used, which is one of the most widely used libraries in Python for data analysis.

During the data processing, the main tasks are cleaning the data by removing irrelevant entries, standardizing column names, generating a correlation chart to identify the most important variables for model training, and finally concatenating the data to create the final CSV file used for training the model.

To process the data, you can run the EDA file located in the src folder, which contains all the code for data processing. You can execute it with the following command:

```bash
python src/EDA.py
```

If you'd like to learn more about how the data processing works step by step, you can check the notebook designed for this task, which is located in the Notebooks folder and is named 000_EDA.ipynb (Notebooks/000_EDA.ipynb). 

This notebook serves the same purpose but includes explanations for each piece of code.

---

### 6. Model Training <a name="model-training"></a>

Open the notebook Notebooks/001_Model_Training.ipynb and follow the steps to:

- Select the most relevant features.
- Train a regression model to predict the happiness score.
- Evaluate the model performance, ensuring that the R² is at least 0.80.
- Save the trained model at Model/Regression_Model.pkl.

---

### 7. Kafka Implementation <a name="kafka-implementation"></a>

Since Kafka is implemented using Docker, the first step is to open the Docker Desktop application to start the Kafka containers.

Once the application is open, execute the following code in a new terminal to start the containers:

```bash
docker-compose up -d
```

To check if the containers are running, use the following command in another terminal:

```bash
docker ps
```

Now, execute the following command to create a topic named **regression_model**:

```bash
docker exec -it happiness-score kafka-topics \
    --create \
    --topic regression_model \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1

```

To verify that the topic was created, use this command:

```bash
docker exec -it happiness-score kafka-topics \
  --list \
  --bootstrap-server localhost:9092
```

---

### 8. Kafka Operation <a name="kafka-operation"></a>

Once the containers are running with the topic created, proceed to the next step, which is running the producer and the consumer to stream the data.

On one side, the producer is responsible for sending the test data used for model training, corresponding to the last 30% of the data/Model_Data.csv file.

On the other side, the consumer receives the data sent by the producer and also receives the predicted value from the trained model. It then stores this data directly in the PostgreSQL database, where the code creates and inserts the data into the defined table.

To run the producer, execute the following code in a new Git bash:

```bash
python Kafka/kafka_producer.py
```

At the same time, run the following code for the consumer in another Git bash:

```bash
python Kafka/kafka_consumer.py
```

It is better to run the consumer first and then the producer to give the program time to create the table.

---

### 9. Database Operation <a name="database-operation"></a>

Once everything has run, verify that the code worked correctly and stored the data in the PostgreSQL database.

To check this, navigate to where you created the PostgreSQL database, create a new script, and run the following command:

```bash
SELECT * FROM happiness_score_prediction;
```

This code should return a total of 230 records, containing the test data and the predicted Happiness Score.

### 10. Conclusión <a name="conclusion"></a>

This project provides a complete solution to predict and store global happiness scores, integrating Machine Learning and real-time streaming systems. The architecture built is scalable and allows continuous analysis based on updated happiness data.

### 11. Authors <a name="authors"></a>

- Juan Manuel Lopez Rodriguez - Lead Developer - juan_m.lopez_r@uao.edu.co

This README.md outlines the entire project, from the initial data processing to the final verification of our predictive model.