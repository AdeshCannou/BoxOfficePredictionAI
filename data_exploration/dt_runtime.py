import pandas as pd
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Supprimer les lignes où runtime est nul
data = data[data['runtime'].notna()]

# Tracer un histogramme de la distribution de runtime
plt.figure(figsize=(10, 6))
plt.hist(data['runtime'], bins=30, color='skyblue', alpha=0.7)
plt.title('Distribution de Runtime')
plt.xlabel('Runtime (minutes)')
plt.ylabel('Fréquence')
plt.xlim(0, 300)  # Ajustez les limites selon votre préférence

plt.show()

# Tracer un graphique de dispersion pour visualiser la relation entre runtime et revenue_adj
plt.figure(figsize=(10, 6))
plt.scatter(data['runtime'], data['revenue_adj'], alpha=0.5)
plt.title('Relation entre Runtime et Revenue (ajusté)')
plt.xlabel('Runtime (minutes)')
plt.ylabel('Revenue (ajusté)')
plt.show()
