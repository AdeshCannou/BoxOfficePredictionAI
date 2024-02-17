import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Charger les données depuis le fichier CSV
file_path = 'finalData_and_scripts/nested.csv'
data = pd.read_csv(file_path, delimiter=';')

# Sélectionner les caractéristiques et la valeur cible
selected_features = ['cast', 'director', 'runtime', 'genres', 'production_companies', 'budget_adj']
target = 'revenue_adj'

# Prétraitement des caractéristiques textuelles (encodage one-hot pour chaque colonne)
data_encoded = pd.get_dummies(data[selected_features])

# sauvegarder le nom des colonnes dans un fichier
with open('columns.txt', 'w') as f:
    for col in data_encoded.columns:
        f.write(col + '\n')
        
# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(data_encoded, data[target], test_size=0.2, random_state=42)

# Initialiser et entraîner le modèle LinearRegression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Faire des prédictions sur l'ensemble de test
y_pred = linear_model.predict(X_test)

# Calculer MSE
mse = mean_squared_error(y_test, y_pred)
print("MSE:", mse)

# Calculer MAE
mae = mean_absolute_error(y_test, y_pred)
print("MAE:", mae)

# Calculer le score R²
r2 = r2_score(y_test, y_pred)
print("R² score:", r2)

# Sauvegarder le modèle
import joblib
joblib.dump(linear_model, 'linear_model.pkl')

# MSE: 1.081493154393007e+16
# MAE: 59557973.45564847
# R² score: 0.7960822255835147
