import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import joblib

file_path = 'data/Model_Data.csv'
data = pd.read_csv(file_path)

data = pd.get_dummies(data, columns=['Country'], drop_first=True)

X = data.drop(columns=['Happiness Score'])
y = data['Happiness Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Elastic Net Regression": ElasticNet(alpha=0.1, l1_ratio=0.5),
    "K-Nearest Neighbors Regression": KNeighborsRegressor(n_neighbors=5),
    "Random Forest Regression": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost Regression": XGBRegressor(n_estimators=100, random_state=42)
}

results = {}
best_model_name = None
best_model = None
best_r2_score = float('-inf')

for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    results[model_name] = {"R2 Score": r2}
    
    # Check if this model has the best R2 score
    if r2 > best_r2_score:
        best_r2_score = r2
        best_model = model
        best_model_name = model_name

# Imprime los resultados
for model_name, metrics in results.items():
    print(f"{model_name}: R2 Score = {metrics['R2 Score']:.4f}")

print(f"\nBest model: {best_model_name} with R2 Score = {best_r2_score:.4f}")

# Guardar el mejor modelo
joblib.dump(best_model, 'Model/Regression_Model.pkl')
print("Best model saved as 'Regression_Model.pkl'")