import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Charger les données depuis le fichier CSV
file_path = 'data/nested.csv'
data = pd.read_csv(file_path, delimiter=';')

# Sélectionner les colonnes nécessaires
#selected_features = ['cast', 'director', 'runtime', 'genres', 'production_companies', 'budget_adj', 'revenue_adj']
#data = data[selected_features]

# Gérer les valeurs manquantes
#data = data.dropna()

# Prétraiter les colonnes catégorielles (cast, director, genres, production_companies)
mlb = MultiLabelBinarizer()
for feature in ['cast', 'director', 'genres', 'production_companies']:
    df = pd.DataFrame(mlb.fit_transform(data.pop(feature)), columns=mlb.classes_, index=data.index)
    df.columns = [f'{feature}_{col}' for col in df.columns]
    data = data.join(df)

# Diviser les données en ensemble d'entraînement, de validation et ensemble de test
X = data.drop('revenue_adj', axis=1)
y = data['revenue_adj']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)  # 20% pour validation

# Initialiser le modèle d'Arbre de Décision
model = DecisionTreeRegressor(random_state=42)

# Entraîner le modèle sur l'ensemble d'entraînement
model.fit(X_train, y_train)

# Prédire sur l'ensemble de validation
y_val_pred = model.predict(X_val)

# Évaluer les performances du modèle sur l'ensemble de validation
mse_val = mean_squared_error(y_val, y_val_pred)
mae_val = mean_absolute_error(y_val, y_val_pred)
r2_val = r2_score(y_val, y_val_pred)
print("Performance sur l'ensemble de validation:")
print(f'Mean Squared Error: {mse_val}')
print(f'Mean Absolute Error: {mae_val}')
print(f'R² Score: {r2_val}')

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