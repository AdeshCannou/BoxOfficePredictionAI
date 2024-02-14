import pandas as pd
data = pd.read_csv('data/tmdb_movies_data.csv')
KEYS=['cast','director','runtime','genres','production_companies','budget_adj','revenue_adj']
cleaned = data[KEYS].dropna()
cleaned = cleaned[cleaned['revenue_adj'] > 0]
cleaned = cleaned[cleaned['budget_adj'] > 0]
cleaned.to_csv('data/cleaned.csv',sep=';')

# cleaned = [ [ el.split('|') for el in i[:-1].split(';') ] for i in open('data/cleaned.csv', 'r', encoding='utf-8').readlines() ]

# keys=cleaned.pop(0)
# tab=[]
# for line in cleaned:
#     for cast in line[1]:
#         for director in line[2]:
#             for genre in line[4]:
#                 for companie in line[5]:
#                     tab.append({
#                             KEYS[0]: cast,
#                             KEYS[1]: director,
#                             KEYS[2]: line[3][0],
#                             KEYS[3]: genre,
#                             KEYS[4]: companie,
#                             KEYS[5]: line[6][0],
#                             KEYS[6]: line[7][0]
#                         })
# frame=pd.DataFrame(tab)
# frame.to_csv('data/nested.csv', sep=';')


