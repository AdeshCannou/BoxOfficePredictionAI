import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Charger le dataset
data = pd.read_csv('data/tmdb_movies_data.csv', sep=',')

# Nettoyage des données (par exemple, mettre en minuscule)
data['overview_cleaned'] = data['overview'].str.lower().fillna('')  # Remplacer les valeurs NaN par des chaînes vides

# Tokenization
words = ' '.join(data['overview_cleaned']).split()

# Analyse de la fréquence des mots
word_freq = pd.Series(words).value_counts().head(20)

# Visualisation de la fréquence des mots
plt.figure(figsize=(10, 6))
word_freq.plot(kind='bar', color='skyblue')
plt.title('20 mots les plus fréquents dans les résumés des films')
plt.xlabel('Mots')
plt.ylabel('Fréquence')
plt.xticks(rotation=45)
plt.show()

# Nuage de mots (Word Cloud)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des résumés des films')
plt.show()

# Filtrer les données pour les 100 films avec le plus de revenu ajusté
top_100_revenue = data.nlargest(100, 'revenue_adj')

# Concaténer les résumés de ces films
overviews_top_100 = ' '.join(top_100_revenue['overview'].str.lower().fillna(''))

# Tokenization
words_top_100 = overviews_top_100.split()

# Analyse de la fréquence des mots
word_freq_top_100 = pd.Series(words_top_100).value_counts().head(20)

# Visualisation de la fréquence des mots des résumés des 100 films avec le plus de revenu ajusté
plt.figure(figsize=(10, 6))
word_freq_top_100.plot(kind='bar', color='skyblue')
plt.title('20 mots les plus présents dans les 100 résumés des films avec le plus de revenu ajusté')
plt.xlabel('Mots')
plt.ylabel('Fréquence')
plt.xticks(rotation=45)
plt.show()

# Nuage de mots (Word Cloud) pour les 100 résumés des films avec le plus de revenu ajusté
wordcloud_top_100 = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words_top_100))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_top_100, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des résumés des 100 films avec le plus de revenu ajusté')
plt.show()

# Filtrer les données pour les 20 mots les plus fréquents
top_20_words = word_freq.index
filtered_data = data[data['overview_cleaned'].str.contains('|'.join(top_20_words))]

# Visualisation de la relation avec "revenue_adj" pour chaque mot
plt.figure(figsize=(12, 8))
for word in top_20_words:
    word_data = filtered_data[filtered_data['overview_cleaned'].str.contains(word)]
    plt.scatter(word_data['revenue_adj'], word_data['overview_cleaned'], label=word, alpha=0.5)

plt.title('Relation entre les mots les plus fréquents dans les résumés et le revenu ajusté')
plt.xlabel('Revenu Ajusté')
plt.ylabel('Résumé de Film')
plt.legend()
plt.show()
