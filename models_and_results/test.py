import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

# Charger le dataset
df = pd.read_csv("data/nested.csv", sep=";")

# Sélectionner les caractéristiques et la cible
selected_features = ['cast', 'director', 'runtime', 'genres', 'production_companies', 'budget_adj']
X = df[selected_features]
y = df['revenue_adj']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prétraitement des caractéristiques catégorielles
categorical_features = ['cast', 'director', 'genres', 'production_companies']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'
)

# Appliquer le prétraitement
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Créer et entraîner le modèle Ridge
ridge_model = Ridge()
ridge_model.fit(X_train_preprocessed, y_train)

# Faire des prédictions sur l'ensemble de test
y_pred = ridge_model.predict(X_test_preprocessed)

# Évaluer le modèle
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R² Score: {r2}')


test_data = {
    "cast": ["Sam Worthington"],
    "director": ["James Cameron"],
    "runtime": 162,
    "genres": ["Action"],
    "production_companies": ["Ingenious Film Partners"],
    "budget_adj": 240886902.9
}

# Convertir les données de test en DataFrame Pandas
test_df = pd.DataFrame(test_data)

# Appliquer le même prétraitement que celui utilisé lors de l'entraînement
test_df_preprocessed = preprocessor.transform(test_df)

# Prédire le box-office avec le modèle entraîné
predicted_revenue = ridge_model.predict(test_df_preprocessed)

print("Predicted Box Office Revenue:", predicted_revenue[0])

# Sauvegarder le modèle entraîné
joblib.dump(ridge_model, 'ridge_model.pkl')
