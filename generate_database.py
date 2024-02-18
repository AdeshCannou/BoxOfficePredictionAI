import pandas as pd
data = pd.read_csv('data/nested.csv', delimiter=';', encoding='utf-8')
KEYS=['cast','director','genres','production_companies']

json={}
for key in KEYS:
    json[key] = [m for m in set(data[key])]

print(pd.DataFrame(json))

#pd.DataFrame()
#file=open('FRONTEND/my-movie-will-go-on/db.json', 'w')
#file.write(str(json))
#file.close()