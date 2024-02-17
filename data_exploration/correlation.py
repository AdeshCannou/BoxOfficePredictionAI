import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

# Charger le dataset
movies_data = pd.read_csv('data/tmdb_movies_data.csv')

# Remplacer les valeurs float par des listes vides dans la colonne cast
movies_data['cast'] = movies_data['cast'].apply(lambda x: [] if pd.isna(x) else x.split('|')[:4])  # Modifier ici pour prendre en compte jusqu'à 4 acteurs

# Créer toutes les combinaisons possibles de 2 à 4 acteurs
actor_combinations = []
for cast_list in movies_data['cast']:
    for r in range(2, min(len(cast_list) + 1, 5)):  # Modifier ici pour prendre en compte jusqu'à 4 acteurs
        actor_combinations.extend(combinations(cast_list, r))

# Créer une liste de dictionnaires pour chaque combinaison d'acteurs avec les informations du film
actor_combinations_data = []
for combination in actor_combinations:
    combination_dict = {'actor_1': combination[0]}
    for i, actor in enumerate(combination[1:], start=2):
        combination_dict[f'actor_{i}'] = actor
    actor_combinations_data.append(combination_dict)

# Créer le DataFrame à partir de la liste de dictionnaires
actor_combinations_df = pd.DataFrame(actor_combinations_data)

# Fusionner avec les données originales pour obtenir les informations sur les films
actor_combinations_df = pd.merge(actor_combinations_df, movies_data, left_index=True, right_index=True, how='left')

# Sélectionner uniquement les colonnes numériques pour le calcul de la corrélation
numeric_columns = actor_combinations_df.select_dtypes(include=['float64', 'int64']).columns
correlation = actor_combinations_df[numeric_columns].corr()

# Afficher la heatmap de corrélation
plt.figure(figsize=(12, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Corrélation entre les caractéristiques')
plt.show()
