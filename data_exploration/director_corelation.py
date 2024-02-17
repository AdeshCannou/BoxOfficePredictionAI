import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
movies_data = pd.read_csv('data/tmdb_movies_data.csv')

# Initialiser un dictionnaire pour stocker le nombre de films et le total du revenu_adj par relation de réalisateurs
director_relations = {}

# Parcourir chaque ligne du dataset
for _, row in movies_data.iterrows():
    # Vérifier si la valeur dans la colonne 'director' est manquante
    if pd.isna(row['director']):
        continue  # Passer à la ligne suivante si la valeur est manquante
    
    # Récupérer la liste des réalisateurs pour ce film
    directors_list = row['director'].split('|')
    
    # Parcourir les combinaisons de deux réalisateurs dans la liste
    for i in range(len(directors_list)):
        for j in range(i+1, len(directors_list)):
            director_pair = tuple(sorted([directors_list[i], directors_list[j]]))  # Utiliser un tuple pour représenter une relation de réalisateur ordonnée
            # Mettre à jour le dictionnaire pour cette relation de réalisateurs
            if director_pair not in director_relations:
                director_relations[director_pair] = {'num_films': 0, 'total_revenue_adj': 0}
            director_relations[director_pair]['num_films'] += 1
            director_relations[director_pair]['total_revenue_adj'] += row['revenue_adj']

# Calculer la moyenne du revenu_adj pour chaque relation de réalisateurs
for relation in director_relations:
    director_relations[relation]['average_revenue_adj'] = director_relations[relation]['total_revenue_adj'] / director_relations[relation]['num_films']

# Trier le dictionnaire par moyenne du revenu_adj dans l'ordre décroissant
top_director_relations = sorted(director_relations.items(), key=lambda x: x[1]['average_revenue_adj'], reverse=True)

# Extraire les relations de réalisateurs et la moyenne du revenu_adj pour chaque relation
director_combinations = [f"{', '.join(relation)} ({info['num_films']})" for relation, info in top_director_relations]
average_revenues = [info['average_revenue_adj'] for _, info in top_director_relations]

# Afficher un graphique
plt.figure(figsize=(10, 6))
plt.barh(director_combinations, average_revenues, color='skyblue')
plt.xlabel('Moyenne du revenu ajusté')
plt.ylabel('Combinaison de réalisateurs')
plt.title('Top des combinaisons de réalisateurs par moyenne du revenu ajusté')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher la combinaison de réalisateurs avec la moyenne de revenu ajusté la plus élevée en haut
plt.show()
