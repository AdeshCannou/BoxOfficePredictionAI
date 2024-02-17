import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
movies_data = pd.read_csv('data/tmdb_movies_data.csv')

# Nom de l'acteur pour lequel vous souhaitez obtenir le top 10 des relations
actor_name = "Robert De Niro"

# Initialiser un dictionnaire pour stocker le nombre de films et le total du revenu_adj par relation
relation_info = {}

# Parcourir chaque ligne du dataset
for _, row in movies_data.iterrows():
    # Vérifier si la valeur dans la colonne 'cast' est manquante
    if pd.isna(row['cast']):
        continue  # Passer à la ligne suivante si la valeur est manquante
    
    # Récupérer la liste des acteurs pour ce film
    cast_list = row['cast'].split('|')
    
    # Vérifier si l'acteur est présent dans la liste
    if actor_name in cast_list:
        # Parcourir les autres acteurs dans la liste
        for other_actor in cast_list:
            if other_actor != actor_name:
                # Mettre à jour le dictionnaire pour cette relation
                if other_actor not in relation_info:
                    relation_info[other_actor] = {'num_films': 0, 'total_revenue_adj': 0}
                relation_info[other_actor]['num_films'] += 1
                relation_info[other_actor]['total_revenue_adj'] += row['revenue_adj']

# Calculer la moyenne du revenu_adj pour chaque relation
for relation in relation_info:
    relation_info[relation]['average_revenue_adj'] = relation_info[relation]['total_revenue_adj'] / relation_info[relation]['num_films']

# Trier le dictionnaire par moyenne du revenu_adj dans l'ordre décroissant
top_relations = sorted(relation_info.items(), key=lambda x: x[1]['average_revenue_adj'], reverse=True)

# Extraire les noms des relations (autres acteurs) et la moyenne du revenu_adj pour chaque relation
relations = [f"{relation} ({info['num_films']})" for relation, info in top_relations]
average_revenues = [info['average_revenue_adj'] for _, info in top_relations]

# Afficher un graphique
plt.figure(figsize=(10, 6))
plt.barh(relations, average_revenues, color='skyblue')
plt.xlabel('Moyenne du revenu ajusté')
plt.ylabel('Relation (autre acteur)')
plt.title(f'Top des relations de {actor_name} par moyenne du revenu ajusté')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher la relation avec la moyenne de revenu ajusté la plus élevée en haut
plt.show()
