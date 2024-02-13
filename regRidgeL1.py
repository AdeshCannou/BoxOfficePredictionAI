import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import joblib
import matplotlib.pyplot as plt

# Charger les données depuis le fichier CSV
file_path = 'data/nested.csv'
data = pd.read_csv(file_path, delimiter=';')

# Sélectionner les colonnes nécessaires
selected_features = ['cast', 'director', 'runtime', 'genres', 'production_companies', 'budget_adj', 'revenue_adj']
data = data[selected_features]

# Gérer les valeurs manquantes
data = data.dropna()

# Prétraiter les colonnes catégorielles (cast, director, genres, production_companies)
mlb = MultiLabelBinarizer()
cast_df = pd.DataFrame(mlb.fit_transform(data.pop('cast')), columns=mlb.classes_, index=data.index)
cast_df.columns = [f'cast_{col}' for col in cast_df.columns]

director_df = pd.DataFrame(mlb.fit_transform(data.pop('director')), columns=mlb.classes_, index=data.index)
director_df.columns = [f'director_{col}' for col in director_df.columns]

genres_df = pd.DataFrame(mlb.fit_transform(data.pop('genres')), columns=mlb.classes_, index=data.index)
genres_df.columns = [f'genres_{col}' for col in genres_df.columns]

production_companies_df = pd.DataFrame(mlb.fit_transform(data.pop('production_companies')), columns=mlb.classes_, index=data.index)
production_companies_df.columns = [f'production_companies_{col}' for col in production_companies_df.columns]

# Joindre les DataFrames créés avec le DataFrame principal
data = data.join(cast_df).join(director_df).join(genres_df).join(production_companies_df)

# Diviser les données en ensemble d'entraînement et ensemble de test
X = data.drop('revenue_adj', axis=1)
y = data['revenue_adj']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normaliser les caractéristiques
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialiser le modèle de Régression Ridge
alpha = 100.0  # Force de régularisation, ajustez selon vos besoins
model = Ridge(alpha=alpha)

# Entraîner le modèle
model.fit(X_train_scaled, y_train)

# Prédire sur l'ensemble de test
y_pred = model.predict(X_test_scaled)

# Évaluer les performances du modèle
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R² Score: {r2}')

# Prédire sur l'ensemble de test
y_test_pred = model.predict(X_test)

# Évaluer les performances du modèle sur l'ensemble de test
mse_test = mean_squared_error(y_test, y_test_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)
print("\nPerformance sur l'ensemble de test:")
print(f'Mean Squared Error: {mse_test}')
print(f'Mean Absolute Error: {mae_test}')
print(f'R² Score: {r2_test}')

# Visualiser les prédictions par rapport aux valeurs réelles sur l'ensemble de test
plt.scatter(y_test, y_test_pred)
plt.xlabel('Valeurs réelles')
plt.ylabel('Prédictions')
plt.title('Prédictions par rapport aux valeurs réelles')
plt.show()

# Diagnostiquer le surajustement en traçant les résidus
residuals = y_test - y_test_pred
plt.scatter(y_test, residuals)
plt.xlabel('Valeurs réelles')
plt.ylabel('Résidus')
plt.title('Résidus par rapport aux valeurs réelles')
plt.axhline(y=0, color='r', linestyle='-')
plt.show()

# Validation croisée pour une évaluation plus robuste
y_pred_cv = cross_val_predict(model, X, y, cv=5)
r2_cv = r2_score(y, y_pred_cv)
print("\nR² Score avec validation croisée (cv=5):", r2_cv)

# Sauvegarder le modèle
joblib.dump(model, 'ridge_regression_model_alpha_100.joblib')
