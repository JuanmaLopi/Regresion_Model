import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_predict
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import joblib
from sklearn.pipeline import Pipeline

# Cargar los datos
file_path = 'data/Model_Data.csv'
data = pd.read_csv(file_path)

# Realizar codificación one-hot para la columna 'Country'
data = pd.get_dummies(data, columns=['Country'], drop_first=True)

# Separar las características (X) y la variable objetivo (y)
X = data.drop(columns=['Happiness Score'])
y = data['Happiness Score']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Definir los modelos y sus hiperparámetros para la búsqueda
models = {
    "Linear Regression": {
        "model": LinearRegression(),
        "params": {}
    },
    "Ridge Regression": {
        "model": Ridge(),
        "params": {"alpha": [0.1, 1.0, 10.0]}
    },
    "Lasso Regression": {
        "model": Lasso(),
        "params": {"alpha": [0.01, 0.1, 1.0]}
    },
    "Elastic Net Regression": {
        "model": ElasticNet(),
        "params": {"alpha": [0.01, 0.1, 1.0], "l1_ratio": [0.2, 0.5, 0.8]}
    },
    "K-Nearest Neighbors Regression": {
        "model": KNeighborsRegressor(),
        "params": {"n_neighbors": [3, 5, 7, 10]}
    },
    "Random Forest Regression": {
        "model": RandomForestRegressor(random_state=42),
        "params": {"n_estimators": [200, 300, 500], "max_depth": [None, 10, 20]}
    },
    "Gradient Boosting Regression": {
        "model": GradientBoostingRegressor(random_state=42),
        "params": {"n_estimators": [200, 300, 500], "learning_rate": [0.05, 0.1, 0.2], "max_depth": [3, 5, 7]}
    },
    "XGBoost Regression": {
        "model": XGBRegressor(random_state=42),
        "params": {"n_estimators": [200, 300, 500], "learning_rate": [0.05, 0.1, 0.2], "max_depth": [3, 5, 7]}
    }
}

# Evaluación de modelos y búsqueda de hiperparámetros
results = {}
best_model_name = None
best_model = None
best_r2_score = float('-inf')

for model_name, model_dict in models.items():
    pipe = Pipeline([
        ('scaler', StandardScaler()),  # Solo escalado
        ('model', model_dict["model"])
    ])
    
    # Configurar GridSearchCV con los hiperparámetros del modelo actual
    grid = GridSearchCV(pipe, {'model__' + key: value for key, value in model_dict["params"].items()},
                        cv=5, scoring='r2', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    # Predicciones y evaluación del modelo
    y_pred = grid.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    results[model_name] = {"R2 Score": r2, "Best Params": grid.best_params_}
    
    # Guardar el mejor modelo según el R2 Score
    if r2 > best_r2_score:
        best_r2_score = r2
        best_model = grid.best_estimator_
        best_model_name = model_name

# Prueba con VotingRegressor usando los mejores modelos
voting_reg = VotingRegressor(estimators=[
    ('KNN', KNeighborsRegressor(n_neighbors=3)),
    ('RandomForest', RandomForestRegressor(n_estimators=300, max_depth=None, random_state=42)),
    ('XGBoost', XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42))
])
voting_reg.fit(X_train, y_train)
y_pred_voting = voting_reg.predict(X_test)
r2_voting = r2_score(y_test, y_pred_voting)

# Prueba con StackingRegressor usando los mejores modelos
stacking_reg = StackingRegressor(
    estimators=[
        ('KNN', KNeighborsRegressor(n_neighbors=3)),
        ('RandomForest', RandomForestRegressor(n_estimators=300, max_depth=None, random_state=42)),
        ('XGBoost', XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42))
    ],
    final_estimator=GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42)
)
stacking_reg.fit(X_train, y_train)
y_pred_stacking = stacking_reg.predict(X_test)
r2_stacking = r2_score(y_test, y_pred_stacking)

# Agregar los resultados de VotingRegressor y StackingRegressor
results["Voting Regressor"] = {"R2 Score": r2_voting, "Best Params": "N/A"}
results["Stacking Regressor"] = {"R2 Score": r2_stacking, "Best Params": "N/A"}

if r2_voting > best_r2_score:
    best_r2_score = r2_voting
    best_model = voting_reg
    best_model_name = "Voting Regressor"

if r2_stacking > best_r2_score:
    best_r2_score = r2_stacking
    best_model = stacking_reg
    best_model_name = "Stacking Regressor"

# Imprimir los resultados de R2 y los mejores parámetros para cada modelo
for model_name, metrics in results.items():
    print(f"{model_name}: R2 Score = {metrics['R2 Score']:.4f}, Best Params = {metrics['Best Params']}")

print(f"\nBest model: {best_model_name} with R2 Score = {best_r2_score:.4f}")

# Guardar el mejor modelo
joblib.dump(best_model, 'Model/Regression_Model.pkl')
print("Best model saved as 'Regression_Model.pkl'")


# Cargar el modelo desde el archivo PKL
pipeline = joblib.load('Model/Regression_Model.pkl')

# Realizar predicciones en el conjunto de prueba
y_pred_test = pipeline.predict(X_test)

# Crear un DataFrame con las características, predicciones y valores reales
test_results = X_test.copy()
test_results['Predicted_Happiness_Score'] = y_pred_test
test_results['Actual_Happiness_Score'] = y_test.values

# Guardar el DataFrame con los resultados
test_results.to_csv('data/test_results.csv', index=False)
print("Archivo 'test_results.csv' guardado con éxito.")