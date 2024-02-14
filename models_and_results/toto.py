import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

# Charger les données depuis le fichier CSV
file_path = 'data/nested.csv'
data = pd.read_csv(file_path, delimiter=';')

# Diviser les colonnes catégorielles en listes
data['cast'] = data['cast'].str.split('|')
data['director'] = data['director'].str.split('|')
data['genres'] = data['genres'].str.split('|')
data['production_companies'] = data['production_companies'].str.split('|')

# Initialiser MultiLabelBinarizer avec le séparateur approprié
mlb = MultiLabelBinarizer()

# Pour chaque colonne catégorielle, appliquer fit_transform sur les données divisées
for column in ['cast', 'director', 'genres', 'production_companies']:
    transformed_data = mlb.fit_transform(data[column])
    transformed_df = pd.DataFrame(transformed_data, columns=mlb.classes_, index=data.index)
    transformed_df.columns = [f'{column}_{col}' for col in transformed_df.columns]
    data = data.join(transformed_df)

# Sélectionner les colonnes nécessaires pour l'entraînement
selected_features = ['runtime', 'budget_adj']
X = pd.concat([data[selected_features], data.filter(regex='cast_|director_|genres_|production_companies_')], axis=1)
y = data['revenue_adj']

# Diviser les données en ensemble d'entraînement et ensemble de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialiser le modèle de Régression Ridge
alpha = 100.0  # Force de régularisation, ajustez selon vos besoins
model = Ridge(alpha=alpha)

# Entraîner le modèle
model.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred = model.predict(X_test)

# Calculer le R² score
r2 = r2_score(y_test, y_pred)
print(f'R² Score: {r2}')

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R² Score: {r2}')

# Sauvegarder le modèle
joblib.dump(model, 'ridge_regression_model.joblib')
