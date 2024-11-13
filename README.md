# HAPPINESS SCORE PREDICTION

---

Este proyecto busca anticipar los índices de felicidad en varios países mediante el uso de técnicas de aprendizaje automático. Para lograrlo, se aplican análisis exploratorios de datos, selección de variables clave, transmisión de datos en tiempo real a través de Kafka y almacenamiento de información en una base de datos PostgreSQL.

---

## Tabla de Contenidos

---

1. [DESCRIPCIÓN DEL PROYECTO](#1-descripción-del-proyecto)

---

### 1. Descripción del Proyecto <a name="descripcion-del-proyecto"></a>
Este proyecto se centra en estimar el nivel de felicidad en distintos países utilizando factores como el ingreso per cápita, la salud de la población, la libertad individual, y otros elementos. Para llevarlo a cabo:

- Se analizan datos de felicidad recopilados a lo largo de varios años.
- Se realiza una selección de las variables más significativas.
- Se entrena un modelo basado en regresión.
- Se implementa Apache Kafka para el envío en tiempo real de las predicciones generadas.
- Se almacena los resultados obtenidos en una base de datos PostgreSQL.