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

# Load the data
data = pd.read_csv('data/Model_Data.csv')

# Define features and target variable
X = data.drop(columns=['Happiness Score'])
y = data['Happiness Score']

# Preprocess the data: apply One-Hot Encoding to the 'Country' column and scale the rest
preprocessor = ColumnTransformer(
    transformers=[
        ('country', OneHotEncoder(handle_unknown='ignore'), ['Country']),  # Encode the 'Country' column and handle unknown categories
        ('num', SimpleImputer(strategy='mean'), X.columns.difference(['Country', 'Year']))  # Impute missing values for other numeric columns
    ])

# Create a dictionary of models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'AdaBoost': AdaBoostRegressor(random_state=42),
    'Support Vector Regression': SVR(),
    'K-Nearest Neighbors': KNeighborsRegressor()
}

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Variables to store the best model and its performance
best_model = None
best_r2 = float('-inf')  # Initialize with the worst possible R^2 value
best_model_name = ""  # To store the name of the best model

# Train and evaluate each model
for model_name, model in models.items():
    # Create a pipeline for each model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Evaluate the model
    r2 = r2_score(y_test, y_pred)
    
    print(f'\nModel: {model_name}')
    print(f'R^2 Score: {r2}')
    
    # If the current model is the best, we save it
    if r2 > best_r2:
        best_r2 = r2
        best_model = pipeline
        best_model_name = model_name

print(f"\nBest model: {best_model_name} with R^2 Score = {best_r2:.4f}")

# Save the best model to a .pkl file
with open('Model/Regression_Model.pkl', 'wb') as file:
    pickle.dump(best_model, file)

print("Model successfully saved in 'Model/Regression_Model.pkl'")
