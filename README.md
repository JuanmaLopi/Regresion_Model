# HAPPINESS SCORE PREDICTION

---

Este proyecto busca anticipar los índices de felicidad en varios países mediante el uso de técnicas de aprendizaje automático. Para lograrlo, se aplican análisis exploratorios de datos, selección de variables clave, transmisión de datos en tiempo real a través de Kafka y almacenamiento de información en una base de datos PostgreSQL.

---

## Tabla de Contenidos

---

1. [DESCRIPCIÓN DEL PROYECTO](#1-descripción-del-proyecto)
2. [REQUERIMIENTOS](#2-requerimientos)

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


## 3. Estructura del Proyecto <a name="estructura-del-proyecto"></a>

La estructura del proyecto se organiza de la siguiente manera:

```plaintext
├── data
│   ├── raw                 # Datos sin procesar
│   ├── processed           # Datos después de preprocesamiento
│   └── external            # Datos externos o adicionales
│
├── notebooks               # Jupyter Notebooks de análisis y experimentación
│
├── src
│   ├── data                # Scripts para manipulación y preparación de datos
│   ├── models              # Scripts para entrenar y evaluar modelos
│   └── utils               # Funciones de utilidad y auxiliares
│
├── tests                   # Pruebas automatizadas del proyecto
│
├── config                  # Configuración y parámetros del proyecto
│
├── README.md               # Archivo de documentación principal
│
└── requirements.txt        # Listado de dependencias del proyecto

