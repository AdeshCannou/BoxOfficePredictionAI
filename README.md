# Projet de prédiction du box office

Ce projet consiste à entraîner un modèle de machine learning pour prédire le box office d'un film en fonction de diverses caractéristiques telles que le casting, le réalisateur, la durée, le genre, les sociétés de production et le budget.

## Installation des dépendances

Pour exécuter ce projet, vous devez disposer de Python 3.x installé sur votre système. Vous pouvez ensuite installer les dépendances en exécutant la commande suivante :

pip install -r requirements.txt

Assurez-vous d'avoir activé un environnement virtuel avant d'exécuter cette commande.

## Structure du projet

- `app.py`: Fichier principal contenant le code de l'API Flask.
- `ridge_regression_model_alpha_100.joblib`: Modèle entraîné sauvegardé à l'aide de Joblib.
- `data/nested.csv`: Fichier CSV contenant les données d'entraînement.
- `README.md`: Ce fichier README contenant des informations sur le projet.

## Lancer le serveur de développement

Lancement du serveur Flask
Pour lancer le serveur Flask, exécutez la commande suivante dans votre terminal :

python app.py

Cela démarrera le serveur sur le port 5000 de votre machine locale. Vous pouvez accéder à l'API en visitant l'URL http://localhost:5000/ dans votre navigateur ou en utilisant un outil comme Postman pour envoyer des requêtes.

## Utilisation de l'API

Vous pouvez utiliser l'API en envoyant une requête POST à l'URL `http://localhost:5000/predict` avec les données au format JSON. Voici un exemple de JSON à fournir :

```json
{
  "cast": ["Tom Hanks", "Matt Damon"],
  "director": ["Steven Spielberg"],
  "runtime": 150,
  "genres": ["Drama", "War"],
  "production_companies": ["Paramount Pictures"],
  "budget_adj": 60000000
}
```
