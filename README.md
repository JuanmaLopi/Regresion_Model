# HAPPINESS SCORE PREDICTION

---

Este proyecto busca anticipar los índices de felicidad en varios países mediante el uso de técnicas de aprendizaje automático. Para lograrlo, se aplican análisis exploratorios de datos, selección de variables clave, transmisión de datos en tiempo real a través de Kafka y almacenamiento de información en una base de datos PostgreSQL.

---

## Tabla de Contenidos

---

1. [DESCRIPCIÓN DEL PROYECTO](#1-descripción-del-proyecto)
2. [REQUERIMIENTOS](#2-requerimientos)
3. [ESTRUCTURA DEL PROYECTO](#3-estructura-del-proyecto)
4. [CONFIGURACIÓN DEL ENTORNO](#4-configuración-del-entorno)
5. [PROCESAMIENTO DE DATOS](#5-procesamiento-de-datos)
6. [ENTRENAMIENTO DEL MODELO](#6-model-training)
7. [IMPLEMENTACIÓN DE KAFKA](#7-implementación-de-kafka)
8. [FUNCIONAMIENTO DE KAFKA](#8-funcionamiento-de-kafka)
9. [EVIDENCIAS](#9-funcionamiento-de-la-base-de-datos)
10. [CONCLUSIÓN](#10-conclusión)
11. [AUTORES](#11-autores)
---

### 1. Descripción del Proyecto <a name="descripcion-del-proyecto"></a>

Este proyecto se centra en estimar el nivel de felicidad en distintos países utilizando factores como el ingreso per cápita, la salud de la población, la libertad individual, y otros elementos. Para llevarlo a cabo:

- Se analizan datos de felicidad recopilados a lo largo de varios años.
- Se realiza una selección de las variables más significativas.
- Se entrena un modelo basado en regresión.
- Se implementa Apache Kafka para el envío en tiempo real de las predicciones generadas.
- Se almacena los resultados obtenidos en una base de datos PostgreSQL.

---

### 2. Requerimientos <a name="requerimientos"></a>

Para realizar el proyecto, se utilizaron diferentes herramientas que ayudaron tanto en el procesamiento de datos, como en el 
entrenamiento de modelo de regresion, el streaming de datos en tiempo real y el almacenamiento de los datos necesarios. A
continuación se explican las herramientas usadas para este proyecto:

- **Python 3.8 o superior** (Lenguaje en el que esta escritó la mayoria del codigo)
- **Docker Desktop** (Aplicación que nos ayuda a Orquestar y nos ayuda con el funcionamiento de Kafka)
- **Apache Kafka** (Nos ayuda a hacer lo que es el Streaming de Datos)
- **PostgreSQL** (Base de datos en la cual se almacenaron las predicciones)
- **Pandas** (herramienta que nos ayuda con el procesamiento de datos)
- **Scikit-learn** (Libreria usada para todo lo relacionado con el entrenamiento del modelo)
- **Matplotlib, Seaborn** (Librerias usadas para realizar graficos de correlación)
- **Psycopg2** (Librería que nos ayuda para poder subir los datos a PostgreSQL)
- **Dotenv** (Libreria usada para el uso de las variables de entorno)

Para instalar todas las librerias necesarias, introduce el siguiente comando:

```bash
pip install kafka-python pandas scikit-learn matplotlib seaborn psycopg2 python-dotenv
```

Todas las dependencias usadas están en el archivo requirements.txt.

---

### 3. Estructura del Proyecto <a name="estructura-del-proyecto"></a>

La estructura del proyecto se organiza de la siguiente manera:

```plaintext
├── data
│   ├── 2015.csv             # Datos sin procesar del año 2015
│   ├── 2016.csv             # Datos sin procesar del año 2016
│   ├── 2017.csv             # Datos sin procesar del año 2017
│   ├── 2018.csv             # Datos sin procesar del año 2018
│   ├── 2019.csv             # Datos sin procesar del año 2019
│   └── model_data           # Datos de entrenamiento del modelo
│
├── Kafka
│   ├── kafka_producer.py       # Código para el productor de Kafka
│   └── kafka_consumer.py       # Código para el consumidor de Kafka
│
├── Model
│   └── Regression_Model.pkl     # Modelo de regresión
│
├── NoteBooks
│   ├── EDA.ipynb                  # Análisis exploratorio de datos
│   └── model_training.ipynb       # Entrenamiento del modelo
│
├── src
│   ├── EDA.py                  # Scripts para análisis exploratorio de datos
│   └── model_training.py       # Scripts para entrenamiento del modelo
│
├── .gitignore               # Archivo de configuración para ignorar archivos en Git
├── docker-compose.yml       # Archivo de configuración de Docker Compose
├── README.md                # Archivo de documentación principal
└── requirements.txt         # Listado de dependencias del proyecto
```

#### Create Virtual Environment

Vamos a Hacer la creación de un ambiente virtual para facilitar mucho mas el funcionamiento del codigo.

Para crearlo, abre una nueva terminal en Visual Studio Code y corre el siguiente codigo:

```bash
python -m venv .venv
```

Esto creara un ambiente virtual llamado `.venv` en la raiz del proyecto.
Para activarlo, corre el siguiente codigo en el bash de Visual Studio Code

```bash
source .venv/scripts/activate
```

---

### 4. Configuración del Entorno <a name="configuracion-del-entorno"></a>

Para la conexión con la base de datos, en nuestro caso PostgreSQL, hay ciertos parametros que se deben definir, que nos 
permiten tener la conexión con esta, por lo cual, en la raiz del proyecto se tiene que crear un archivo *.env*, donde guardaremos
nuestras variables de entorno, las cuales son las credenciales que se usan para conectarse a PostgreSQL.

DB_NAME= Nombre_De_Tu_Base_De_Datos
DB_USER= Nombre_De_Tu_Usuario
DB_PASSWORD= Contraseña_De_Tu_Base_De_Datos
DB_HOST= Host_De_La_Base_De_Datos       # Por lo general este viene definido como LocalHost
DB_PORT= Puerto_De_La_Base_De_Datos     # El puerto predefinido de PostgreSQL es el 5432

---

### 5. Procesamiento de Datos <a name="procesamiento-de-datos"></a>

Para el procesamiento de datos, se utilizará la biblioteca **Pandas**, que es una de las bibliotecas más utilizadas en Python para el análisis de datos.

Al momento de hacer el procesamiento de datos, lo que principalmente hacemos, es realizar una limpieza de datos, como borrar datos irrelevantes que no nos servirán para el entremiento del modelo, estandarización del nombre de columnas para que al final todos tengan el mismo nombre, se hace un grafico de correlación para ver las variables que más importan en el entrenamiento del modelo y por ultimo se hace una concatenación de los datos, el cual nos va a dar el csv final que usaremos para entrenar el modelo.

Para hacer este procesamiento de datos, se puede correr el documento llamado EDA dentro de la carpeta src, el cual tiene todo el codigo para hacer el procesamiento de los datos, para correrlo puedes usar el siguiente comando:

```bash
python src/EDA.py
```

Y si quieres saber más como funciona el paso a paso del procesamiento de los datos, lo puedes ver en el Notebook diseñado principalmente para esta tarea, este está ubicado en la carpeta de NoteBooks, y tiene el nombre de 000_EDA.ipynb (**NoteBooks/000_EDA.ipynb**)

este tiene la misma funcionalidad, pero con su explicación de cada codigo.

---

### 6. Model Training <a name="model-training"></a>

Abre el notebook *Notebooks/001_Model_Training.ipynb* y sigue los pasos para:

- Seleccionar las variables más relevantes.
- Entrenar un modelo de regresión para estimar la puntuación de felicidad.
- Evaluar el rendimiento del modelo, asegurándote de que el R² sea de al menos 0.80.
- Guardar el modelo entrenado en la ruta models/final_happiness_model.pkl.

---

### 7. Implementación de Kafka <a name="implementacion_de_kafka"></a>

Ya que Kafka lo implementamos con Docker, lo primero que tenemos que hacer es abrir nuestra aplicación de Docker Desktop para que se pueda poner a correr los contenedores de Kafka.

Una vez que tengamos nuestra aplicación abierta, ejecutamos en una nueva terminal el siguiente codigo que levanta los contenedores y los pone a funcionar:

```bash
docker-compose up -d
```

Para verificar que los contenedores ya están funcionando, en otra terminal, ejecutamos el siguietne codigo:

```bash
docker ps
```

Ahora ejecutamos el siguiente comando para crear un topic llamado **regression_model**:

```bash
docker exec -it happiness-score kafka-topics \
    --create \
    --topic regression_model \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1

```

Ahora nos aseguramos que el topic fue creado con este comando:

```bash
docker exec -it happiness-score kafka-topics \
  --list \
  --bootstrap-server localhost:9092
```

---

### 8. Funcionamiento de Kafka <a name="funcionamiento-de-kafka"></a>

Una vez que los contenedores esten funcionando con su topic ya creado, pasamos al siguiente paso, que es correr el producer y el consumer para hacer el streaming de los datos.

Por un lado, el producer se encarga de enviar los datos de prueba que se usaron para el entrenamiento del modelo, el cual 
corresponder al ultimo 30% del archivo *data/Model_Data.csv*.

Por otro lado, el consumer tiene la función de recibir esos datos que le envia el producer, pero además de esto recibe el dato que predice el modelo que fue entrenado y va y los guarda directamente en nuestra base de datos PostgreSQL, donde le codigo crea e inserta los datos en la tabla que esta definida.

Para correr la parte del producer, en un nuevo git bash, se corre el siguiente codigo:

```bash
python Kafka/kafka_producer.py
```

Mientras que para la parte del consumer, en otra git bash, se corre simultaneamente el siguiente codigo:

```bash
python Kafka/kafka_consumer.py
```

Cabe aclarar que es mejor que corras primero el consumer, y luego el producer, para asi darle tiempo al programa de crear la tabla.

---

### 9. Funcionamiento de la base de datos <a name="funcionamiento-de-la-base-de-datos"></a>

Una vez que ya se corrio todo, lo que nos queda es comprobar que el codigo realmente funcionó y nos guardo la información en nuestra base de datos PostgreSQL.

Para verificar esto, nos dirigimos a donde creamos nuestra base de datos en PostgreSQL, creamos un nuevo Script y corremos el siguiente comando:

```bash
SELECT * FROM happiness_score_prediction;
```

Este codigo debe devolver un total de 230 datos, en donde se encuentran los datos de prueba y el *Happiness Score* que se iba a predecir.

### 10. Conclusión <a name="conclusion"></a>
Este proyecto proporciona una solución completa para predecir y almacenar puntajes de felicidad a nivel global, integrando Machine Learning y sistemas de transmisión en tiempo real. La arquitectura construida es escalable y permite análisis continuos en base a datos actualizados de felicidad.

### 11. Autores

- **Juan Manuel Lopez Rodriguez** - *Desarrollador Principal* - [juan_m.lopez_r@uao.edu.co](mailto:juan_m.lopez_r@uao.edu.co)

En este README.md se especifico la totalidad del proyecto, desde el punto inicial de procesamiento de los datos, hasta el punto final de la verificación de nuestro modelo predictivo.