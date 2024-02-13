import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Supprimer les lignes avec des valeurs nulles dans la colonne 'cast'
data = data.dropna(subset=['cast'])

# Créer un ensemble pour stocker les acteurs uniques
unique_actors = set()

# Itérer sur la colonne 'cast' pour ajouter chaque acteur à l'ensemble
for cast in data['cast'].str.split('|'):
    unique_actors.update(cast)

# Afficher le nombre d'acteurs distincts dans le dataset
total_unique_actors = len(unique_actors)
print("Nombre d'acteurs distincts dans le dataset :", total_unique_actors)

# Créer un DataFrame pour stocker les acteurs et leur revenu moyen par film
actor_revenue_df = pd.DataFrame(columns=['Actor', 'Mean_Revenue_Adj'])

# Itérer sur la colonne 'cast'
for index, row in data.iterrows():
    cast = row['cast'].split('|')
    revenue_adj = row['revenue_adj']
    
    # Calculer le revenu moyen par film pour chaque acteur dans le cast
    for actor in cast:
        # Vérifier si l'acteur est déjà dans le DataFrame
        if actor in actor_revenue_df['Actor'].values:
            actor_revenue_df.loc[actor_revenue_df['Actor'] == actor, 'Mean_Revenue_Adj'] += revenue_adj
        else:
            actor_revenue_df = actor_revenue_df._append({'Actor': actor, 'Mean_Revenue_Adj': revenue_adj}, ignore_index=True)

# Diviser le revenu total par le nombre de films dans lesquels chaque acteur a joué
actor_revenue_df['Mean_Revenue_Adj'] /= actor_revenue_df.groupby('Actor').cumcount() + 1

# Trier le DataFrame par revenu moyen par film en ordre décroissant
actor_revenue_df = actor_revenue_df.sort_values(by='Mean_Revenue_Adj', ascending=False)

# Sélectionner les 20 premiers acteurs avec le revenu moyen par film le plus élevé
top_20_actors = actor_revenue_df.head(20)

def get_actor_number_of_movies(actor):
    return data['cast'].str.contains(actor).sum()

# Ajouter le nombre de films dans l'abscisse à côté du nom de chaque acteur
top_20_actors['Actor_with_Movie_Count'] = top_20_actors.apply(lambda x: f"{x['Actor']} ({get_actor_number_of_movies(x['Actor'])})", axis=1)

# Tracer un graphique pour visualiser le top 20 des acteurs avec leur revenu moyen par film
plt.figure(figsize=(12, 6))
plt.bar(top_20_actors['Actor_with_Movie_Count'], top_20_actors['Mean_Revenue_Adj'], color='skyblue')
plt.title('Top 20 des Acteurs avec le Revenu Moyen par Film')
plt.xlabel('Acteur (Nombre de Films)')
plt.ylabel('Revenu Moyen par Film (Revenu Ajusté)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.show()
