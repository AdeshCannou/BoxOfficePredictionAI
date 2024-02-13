import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Créer une nouvelle colonne 'has_homepage' pour indiquer si un film a une page d'accueil ou non
data['has_homepage'] = 0
data.loc[data['homepage'].notnull(), 'has_homepage'] = 1

# Tracer un graphique pour visualiser les revenus des films avec et sans page d'accueil
sns.catplot(x='has_homepage', y='revenue_adj', data=data)
plt.title('Revenu pour les films avec et sans page d\'accueil')
plt.xlabel('A une Page d\'Accueil')
plt.ylabel('Revenu Ajusté')
plt.show()
