from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

# Charger votre ensemble de données à partir du fichier CSV
# Assurez-vous d'ajuster le chemin du fichier selon votre configuration
data = pd.read_csv("data/tmdb_movies_data.csv")

# Supposons que X représente vos caractéristiques et y le box office
X = data.drop("box_office", axis=1)
y = data["box_office"]

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Liste des modèles à tester
models = [
    ("Régression Linéaire", LinearRegression()),
    ("Forêt Aléatoire", RandomForestRegressor(n_estimators=100, random_state=42)),
    ("Réseau Neuronal", MLPRegressor(hidden_layer_sizes=(100,), max_iter=500, random_state=42))
]

# Boucle pour tester chaque modèle
for model_name, model in models:
    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Faire des prédictions sur l'ensemble de test
    predictions = model.predict(X_test)

    # Évaluer la performance avec la racine carrée de l'erreur quadratique moyenne (RMSE)
    rmse = mean_squared_error(y_test, predictions, squared=False)

    # Afficher les résultats
    print(f"Modèle : {model_name}")
    print(f"RMSE : {rmse}")
    print("-" * 50)
