import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Cargar los datos
data = pd.read_csv('data/Model_Data.csv')

# Definir las características y la variable objetivo
X = data.drop(columns=['Happiness Score'])
y = data['Happiness Score']

# Preprocesar los datos: aplicar One-Hot Encoding a la columna 'Country' y escalar el resto
preprocessor = ColumnTransformer(
    transformers=[
        ('country', OneHotEncoder(handle_unknown='ignore'), ['Country']),  # Codificar la columna 'Country' y manejar categorías desconocidas
        ('num', SimpleImputer(strategy='mean'), X.columns.difference(['Country', 'Year']))  # Imputar valores faltantes para otras columnas numéricas
    ])

# Crear un diccionario de modelos
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'AdaBoost': AdaBoostRegressor(random_state=42),
    'Support Vector Regression': SVR(),
    'K-Nearest Neighbors': KNeighborsRegressor()
}

# Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Variables para almacenar el mejor modelo y su rendimiento
best_model = None
best_r2 = float('-inf')  # Inicializamos con el peor valor posible para R^2
best_model_name = ""  # Para almacenar el nombre del mejor modelo

# Entrenar y evaluar cada modelo
for model_name, model in models.items():
    # Crear un pipeline para cada modelo
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])
    
    # Entrenar el modelo
    pipeline.fit(X_train, y_train)
    
    # Hacer predicciones
    y_pred = pipeline.predict(X_test)
    
    # Evaluar el modelo
    r2 = r2_score(y_test, y_pred)
    
    print(f'\nModelo: {model_name}')
    print(f'R^2 Score: {r2}')
    
    # Si el modelo actual es el mejor, lo guardamos
    if r2 > best_r2:
        best_r2 = r2
        best_model = pipeline
        best_model_name = model_name

print(f"\nBest model: {best_model_name} with R2 Score = {best_r2:.4f}")

# Guardar el mejor modelo en un archivo .pkl
with open('Model/Regression_Model.pkl', 'wb') as file:
    pickle.dump(best_model, file)

print("Modelo guardado exitosamente en 'Model/Regression_Model.pkl'")
