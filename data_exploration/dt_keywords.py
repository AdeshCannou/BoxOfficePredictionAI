import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Nettoyage des données (par exemple, mettre en minuscule)
data['keywords_cleaned'] = data['keywords'].str.lower().fillna('')  # Remplacer les valeurs NaN par des chaînes vides

# Tokenization
words = ' '.join(data['keywords_cleaned']).split()

# Analyse de la fréquence des mots
word_freq = pd.Series(words).value_counts().head(20)

# Visualisation de la fréquence des mots
plt.figure(figsize=(10, 6))
word_freq.plot(kind='bar', color='skyblue')
plt.title('20 mots clés les plus fréquents dans les films')
plt.xlabel('Mots clés')
plt.ylabel('Fréquence')
plt.xticks(rotation=45)
plt.show()

# Nuage de mots (Word Cloud)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des mots clés des films')
plt.show()

# Filtrer les données pour les 100 films avec le plus de revenu ajusté
top_100_revenue = data.nlargest(100, 'revenue_adj')

# Concaténer les mots clés de ces films
keywords_top_100 = ' '.join(top_100_revenue['keywords'].str.lower().fillna(''))

# Tokenization
words_top_100 = keywords_top_100.split()

# Analyse de la fréquence des mots clés
word_freq_top_100 = pd.Series(words_top_100).value_counts().head(20)

# Visualisation de la fréquence des mots clés des 100 films avec le plus de revenu ajusté
plt.figure(figsize=(10, 6))
word_freq_top_100.plot(kind='bar', color='skyblue')
plt.title('20 mots clés les plus présents dans les 100 films avec le plus de revenu ajusté')
plt.xlabel('Mots clés')
plt.ylabel('Fréquence')
plt.xticks(rotation=45)
plt.show()

# Nuage de mots (Word Cloud) pour les 100 films avec le plus de revenu ajusté
wordcloud_top_100 = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words_top_100))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_top_100, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des mots clés des 100 films avec le plus de revenu ajusté')
plt.show()

# Filtrer les données pour les 20 mots clés les plus fréquents
top_20_words = word_freq.index
filtered_data = data[data['keywords_cleaned'].str.contains('|'.join(top_20_words))]

# Visualisation de la relation avec "revenue_adj" pour chaque mot clé
plt.figure(figsize=(12, 8))
for word in top_20_words:
    word_data = filtered_data[filtered_data['keywords_cleaned'].str.contains(word)]
    plt.scatter(word_data['revenue_adj'], word_data['keywords_cleaned'], label=word, alpha=0.5)

plt.title('Relation entre les mots clés les plus fréquents et le revenu ajusté')
plt.xlabel('Revenu Ajusté')
plt.ylabel('Mots clés')
plt.legend()
plt.show()
