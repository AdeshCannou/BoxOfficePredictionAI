import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Supprimer les lignes avec des valeurs nulles dans la colonne 'genres'
data = data.dropna(subset=['genres'])

# Séparer les genres et compter le nombre total de genres différents
unique_genres = set()
for genres in data['genres'].str.split('|'):
    unique_genres.update(genres)
total_unique_genres = len(unique_genres)
print("Nombre total de genres différents :", total_unique_genres)

# Compter le nombre de genres par film
data['num_genres'] = data['genres'].apply(lambda x: len(x.split('|')))
genres_counts = data['num_genres'].value_counts()

# Tracer un graphique pour visualiser le nombre de films en fonction du nombre de genres qu'ils possèdent
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
genres_counts.sort_index().plot(kind='bar', color='skyblue')
plt.title('Nombre de Films en Fonction du Nombre de Genres')
plt.xlabel('Nombre de Genres')
plt.ylabel('Nombre de Films')
plt.xticks(rotation=0)
plt.grid(True)

# Créer une colonne pour chaque genre
genres = list(unique_genres)
for genre in genres:
    data[genre] = data['genres'].str.contains(genre)

# Tracer un graphique pour visualiser le classement des genres les plus utilisés
plt.subplot(1, 2, 2)
genre_counts = data[genres].sum().sort_values(ascending=False)
genre_counts.plot(kind='bar', color='skyblue')
plt.title('Classement des Genres les Plus Utilisés dans les Films')
plt.xlabel('Genre')
plt.ylabel('Nombre de Films')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# Calculer le total des revenus ajustés pour chaque genre
genre_revenue_sum = {}
for genre in genres:
    genre_revenue_sum[genre] = data[data[genre]]['revenue_adj'].sum()

# Tracer un graphique pour visualiser le total des revenus ajustés par genre
plt.figure(figsize=(12, 6))
plt.bar(genre_revenue_sum.keys(), genre_revenue_sum.values(), color='skyblue')
plt.title('Total des Revenus Ajustés par Genre')
plt.xlabel('Genre')
plt.ylabel('Total des Revenus Ajustés')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

plt.tight_layout()
plt.show()
