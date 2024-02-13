import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Convertir la colonne release_date en type datetime
data['release_date'] = pd.to_datetime(data['release_date'])

# Créer une colonne pour le mois de sortie
data['release_month'] = data['release_date'].dt.month

# Créer une colonne pour le jour de sortie
data['release_day'] = data['release_date'].dt.day

# Ignorer l'année pour la distribution des sorties par mois
plt.figure(figsize=(10, 6))
data['release_month'].plot(kind='hist', bins=12, color='skyblue', edgecolor='black')
plt.title('Distribution des Sorties par Mois')
plt.xlabel('Mois')
plt.ylabel('Nombre de Films')
plt.xticks(range(1, 13))
plt.grid(True)
plt.show()

# Calculer la moyenne du revenu ajusté par mois de sortie
monthly_revenue = data.groupby('release_month')['revenue_adj'].mean()

# Tracer un graphique de barres pour visualiser la relation entre le mois de sortie et le revenu ajusté moyen
plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind='bar', color='skyblue')
plt.title('Revenu Ajusté Moyen par Mois de Sortie')
plt.xlabel('Mois de Sortie')
plt.ylabel('Revenu Ajusté Moyen')
plt.xticks(rotation=45)
plt.show()

# Calculer la moyenne du revenu ajusté par jour de sortie
daily_revenue = data.groupby('release_day')['revenue_adj'].mean()

# Tracer un graphique de ligne pour visualiser la relation entre le jour de sortie et le revenu ajusté moyen
plt.figure(figsize=(10, 6))
plt.plot(daily_revenue.index, daily_revenue.values, marker='o', color='skyblue')
plt.title('Revenu Ajusté Moyen par Jour de Sortie')
plt.xlabel('Jour de Sortie')
plt.ylabel('Revenu Ajusté Moyen')
plt.xticks(range(1, 32))
plt.grid(True)
plt.show()

# Créer une colonne pour le jour de la semaine
data['day_of_week'] = data['release_date'].dt.day_name()

# Créer une liste ordonnée des jours de la semaine
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Calculer la moyenne du revenu ajusté par jour de la semaine
weekly_revenue = data.groupby('day_of_week')['revenue_adj'].mean()

# Réindexer pour trier les jours de la semaine dans l'ordre
weekly_revenue = weekly_revenue.reindex(ordered_days)

# Créer un graphique avec des points pour visualiser la relation entre le jour de la semaine et le revenu ajusté moyen
plt.figure(figsize=(10, 6))
plt.scatter(weekly_revenue.index, weekly_revenue.values, color='orange')
plt.plot(weekly_revenue.index, weekly_revenue.values, color='blue', linestyle='dashed')
plt.title('Revenu Ajusté Moyen par Jour de la Semaine')
plt.xlabel('Jour de la Semaine')
plt.ylabel('Revenu Ajusté Moyen')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
