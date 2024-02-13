import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Supprimer les lignes avec des valeurs nulles dans la colonne 'production_companies'
data = data.dropna(subset=['production_companies'])

# Séparer les noms des sociétés de production et compter le nombre total de sociétés différentes
unique_production_companies = set()
for companies in data['production_companies'].str.split('|'):
    unique_production_companies.update(companies)
total_unique_companies = len(unique_production_companies)
print("Nombre total de sociétés de production différentes :", total_unique_companies)

# Compter le nombre de sociétés de production par film
data['num_production_companies'] = data['production_companies'].apply(lambda x: len(x.split('|')))
production_companies_counts = data['num_production_companies'].value_counts()

# Créer un DataFrame pour les sociétés de production et leurs revenus ajustés
production_revenue = pd.DataFrame(columns=['production_company', 'revenue_adj'])

# Remplir le DataFrame avec les données de chaque société de production et son revenu ajusté
for _, row in data.iterrows():
    for company in row['production_companies'].split('|'):
        production_revenue = production_revenue._append({'production_company': company,
                                                        'revenue_adj': row['revenue_adj']},
                                                       ignore_index=True)

# Agréger les revenus ajustés par société de production
top_production_revenue = production_revenue.groupby('production_company')['revenue_adj'].sum()

# Sélectionner les 20 sociétés de production avec les revenus ajustés les plus élevés
top_20_production_revenue = top_production_revenue.nlargest(20)

# Compter le nombre de films pour chaque société de production dans le top 20
num_films_per_company = {}
for company in top_20_production_revenue.index:
    num_films = len(data[data['production_companies'].str.contains(company)])
    num_films_per_company[company] = num_films

# Tracer un graphique de barres pour visualiser la distribution du nombre de sociétés de production par film
plt.figure(figsize=(10, 6))
plt.bar(production_companies_counts.index, production_companies_counts.values, color='skyblue')
plt.title('Distribution du Nombre de Sociétés de Production par Film')
plt.xlabel('Nombre de Sociétés de Production')
plt.ylabel('Nombre de Films')
plt.xticks(rotation=0)
plt.grid(True)
plt.show()

# Tracer un graphique de barres pour visualiser le nombre de films par société de production dans le top 20
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(num_films_per_company.keys(), num_films_per_company.values(), color='skyblue')
plt.title('Nombre de Films par Société de Production dans le Top 20')
plt.xlabel('Société de Production')
plt.ylabel('Nombre de Films')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Tracer un graphique de barres pour visualiser les revenus ajustés par société de production dans le top 20
plt.subplot(1, 2, 2)
plt.bar(top_20_production_revenue.index, top_20_production_revenue.values, color='skyblue')
plt.title('Revenus Ajustés par Société de Production dans le Top 20')
plt.xlabel('Société de Production')
plt.ylabel('Revenus Ajustés')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

plt.tight_layout()
plt.show()
