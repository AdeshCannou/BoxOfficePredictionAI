import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
movies_data = pd.read_csv('data/tmdb_movies_data.csv')

# Initialiser un dictionnaire pour stocker le nombre de films et le total du revenu_adj par relation de genres
genre_relations = {}

# Parcourir chaque ligne du dataset
for _, row in movies_data.iterrows():
    # Vérifier si la valeur dans la colonne 'genres' est manquante
    if pd.isna(row['genres']):
        continue  # Passer à la ligne suivante si la valeur est manquante
    
    # Récupérer la liste des genres pour ce film
    genres_list = row['genres'].split('|')
    
    # Parcourir les combinaisons de deux genres dans la liste
    for i in range(len(genres_list)):
        for j in range(i+1, len(genres_list)):
            genre_pair = tuple(sorted([genres_list[i], genres_list[j]]))  # Utiliser un tuple pour représenter une relation de genre ordonnée
            # Mettre à jour le dictionnaire pour cette relation de genres
            if genre_pair not in genre_relations:
                genre_relations[genre_pair] = {'num_films': 0, 'total_revenue_adj': 0}
            genre_relations[genre_pair]['num_films'] += 1
            genre_relations[genre_pair]['total_revenue_adj'] += row['revenue_adj']

# Calculer la moyenne du revenu_adj pour chaque relation de genres
for relation in genre_relations:
    genre_relations[relation]['average_revenue_adj'] = genre_relations[relation]['total_revenue_adj'] / genre_relations[relation]['num_films']

# Trier le dictionnaire par moyenne du revenu_adj dans l'ordre décroissant
top_genre_relations = sorted(genre_relations.items(), key=lambda x: x[1]['average_revenue_adj'], reverse=True)

# Extraire les relations de genres et la moyenne du revenu_adj pour chaque relation
genre_combinations = [f"{', '.join(relation)} ({info['num_films']})" for relation, info in top_genre_relations]
average_revenues = [info['average_revenue_adj'] for _, info in top_genre_relations]

# Afficher un graphique
plt.figure(figsize=(10, 6))
plt.barh(genre_combinations, average_revenues, color='skyblue')
plt.xlabel('Moyenne du revenu ajusté')
plt.ylabel('Combinaison de genres')
plt.title('Top des combinaisons de genres par moyenne du revenu ajusté')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher la combinaison de genres avec la moyenne de revenu ajusté la plus élevée en haut
plt.show()
