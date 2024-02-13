import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Supprimer les lignes avec des valeurs nulles dans la colonne 'director'
data = data.dropna(subset=['director'])

# Nombre distinct de réalisateurs dans le dataset
distinct_directors_count = data['director'].nunique()
print("Nombre distinct de réalisateurs dans le dataset :", distinct_directors_count)

# Créer un DataFrame pour stocker le nombre de réalisateurs par film et leur revenu ajusté
director_count_revenue_df = data.groupby('director')['revenue_adj'].agg(['count', 'mean']).reset_index()
director_count_revenue_df.columns = ['Director', 'Film_Count', 'Mean_Revenue_Adj']

# Tracer un graphique du nombre de réalisateurs par film en relation avec le revenu ajusté
plt.figure(figsize=(10, 6))
plt.scatter(director_count_revenue_df['Film_Count'], director_count_revenue_df['Mean_Revenue_Adj'], alpha=0.5)
plt.title('Nombre de Réalisateurs par Film en Relation avec le Revenu Ajusté')
plt.xlabel('Nombre de Réalisateurs par Film')
plt.ylabel('Revenu Moyen Ajusté par Film')
plt.grid(True)
plt.tight_layout()
plt.show()

# Créer un DataFrame pour stocker les réalisateurs et leur revenu moyen par film
director_revenue_df = pd.DataFrame(columns=['Director', 'Mean_Revenue_Adj'])

# Itérer sur la colonne 'director'
for index, row in data.iterrows():
    directors = row['director'].split('|')
    revenue_adj = row['revenue_adj']
    
    # Calculer le revenu moyen par film pour chaque réalisateur dans la liste des réalisateurs
    for director in directors:
        # Vérifier si le réalisateur est déjà dans le DataFrame
        if director in director_revenue_df['Director'].values:
            director_revenue_df.loc[director_revenue_df['Director'] == director, 'Mean_Revenue_Adj'] += revenue_adj
        else:
            director_revenue_df = director_revenue_df._append({'Director': director, 'Mean_Revenue_Adj': revenue_adj}, ignore_index=True)

# Diviser le revenu total par le nombre de films pour chaque réalisateur
director_revenue_df['Mean_Revenue_Adj'] /= director_revenue_df.groupby('Director').cumcount() + 1

# Trier le DataFrame par revenu moyen par film en ordre décroissant
director_revenue_df = director_revenue_df.sort_values(by='Mean_Revenue_Adj', ascending=False)

# Sélectionner les 20 premiers réalisateurs avec le revenu moyen par film le plus élevé
top_20_directors = director_revenue_df.head(20)

def get_director_number_of_movies(director_name):
    return director_count_revenue_df[director_count_revenue_df['Director'] == director_name]['Film_Count'].values[0]

# Ajouter le nombre de films dans l'abscisse à côté du nom de chaque réalisateur
top_20_directors['Director_with_Movie_Count'] = top_20_directors.apply(lambda x: f"{x['Director']} ({get_director_number_of_movies(x['Director'])})", axis=1)

# Tracer un graphique pour visualiser le top 20 des réalisateurs avec leur revenu moyen par film
plt.figure(figsize=(12, 6))
plt.bar(top_20_directors['Director_with_Movie_Count'], top_20_directors['Mean_Revenue_Adj'], color='skyblue')
plt.title('Top 20 des Réalisateurs avec le Revenu Moyen par Film')
plt.xlabel('Réalisateur (Nombre de Films)')
plt.ylabel('Revenu Moyen par Film (Revenu Ajusté)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.show()
