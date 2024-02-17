import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
movies_data = pd.read_csv('data/tmdb_movies_data.csv')

# Initialiser un dictionnaire pour stocker le nombre de films et le total du revenu_adj par relation de sociétés de production
production_relations = {}

# Parcourir chaque ligne du dataset
for _, row in movies_data.iterrows():
    # Vérifier si la valeur dans la colonne 'production_companies' est manquante
    if pd.isna(row['production_companies']):
        continue  # Passer à la ligne suivante si la valeur est manquante
    
    # Récupérer la liste des sociétés de production pour ce film
    production_list = row['production_companies'].split('|')
    
    # Parcourir les combinaisons de deux sociétés de production dans la liste
    for i in range(len(production_list)):
        for j in range(i+1, len(production_list)):
            production_pair = tuple(sorted([production_list[i], production_list[j]]))  # Utiliser un tuple pour représenter une relation de sociétés de production ordonnée
            # Mettre à jour le dictionnaire pour cette relation de sociétés de production
            if production_pair not in production_relations:
                production_relations[production_pair] = {'num_films': 0, 'total_revenue_adj': 0}
            production_relations[production_pair]['num_films'] += 1
            production_relations[production_pair]['total_revenue_adj'] += row['revenue_adj']

# Calculer la moyenne du revenu_adj pour chaque relation de sociétés de production
for relation in production_relations:
    production_relations[relation]['average_revenue_adj'] = production_relations[relation]['total_revenue_adj'] / production_relations[relation]['num_films']

# Trier le dictionnaire par moyenne du revenu_adj dans l'ordre décroissant
top_production_relations = sorted(production_relations.items(), key=lambda x: x[1]['average_revenue_adj'], reverse=True)

# Extraire les relations de sociétés de production et la moyenne du revenu_adj pour chaque relation
production_combinations = [f"{', '.join(relation)} ({info['num_films']})" for relation, info in top_production_relations]
average_revenues = [info['average_revenue_adj'] for _, info in top_production_relations]

# Afficher un graphique
plt.figure(figsize=(10, 6))
plt.barh(production_combinations, average_revenues, color='skyblue')
plt.xlabel('Moyenne du revenu ajusté')
plt.ylabel('Combinaison de sociétés de production')
plt.title('Top des combinaisons de sociétés de production par moyenne du revenu ajusté')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher la combinaison de sociétés de production avec la moyenne de revenu ajusté la plus élevée en haut
plt.show()
