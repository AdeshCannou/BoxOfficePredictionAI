import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Filtrer les lignes où revenue_adj et budget_adj ne sont pas zéro
filtered_data = data[(data['revenue_adj'] != 0) & (data['budget_adj'] != 0)].copy()  # Utilisez .copy() pour éviter les avertissements

# Ajouter une colonne pour le logarithme du budget
filtered_data.loc[:, 'log_budget_adj'] = np.log1p(filtered_data['budget_adj'])

# Ajouter une colonne pour le logarithme du revenu
filtered_data.loc[:, 'log_revenue_adj'] = np.log1p(filtered_data['revenue_adj'])

# Tracer un histogramme de budget_adj
plt.figure(figsize=(10, 6))
plt.hist(filtered_data['budget_adj'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution du Budget (ajusté)')
plt.xlabel('Budget (ajusté)')
plt.ylabel('Fréquence')
plt.show()

# Tracer un histogramme de log_budget_adj
plt.figure(figsize=(10, 6))
plt.hist(filtered_data['log_budget_adj'], bins=50, color='green', alpha=0.7)
plt.title('Distribution du Logarithme du Budget (ajusté)')
plt.xlabel('Logarithme du Budget (ajusté)')
plt.ylabel('Fréquence')
plt.show()

# Tracer un graphique de dispersion pour visualiser la relation entre budget_adj et revenue_adj
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['budget_adj'], filtered_data['revenue_adj'], alpha=0.5)
plt.title('Relation entre Budget (ajusté) et Revenue (ajusté)')
plt.xlabel('Budget (ajusté)')
plt.ylabel('Revenue (ajusté)')
plt.show()

# Tracer un graphique de dispersion pour visualiser la relation entre log_budget_adj et log_revenue_adj
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['log_budget_adj'], filtered_data['log_revenue_adj'], alpha=0.5)
plt.title('Relation entre Budget (logarithmique) et Revenue (logarithmique)')
plt.xlabel('Logarithme du Budget (ajusté)')
plt.ylabel('Logarithme du Revenue (ajusté)')
plt.show()
