from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Charger le modèle
model = joblib.load('ridge_regression_model_alpha_100.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = ['cast', 'director', 'runtime', 'genres', 'production_companies', 'budget_adj']
    df = pd.DataFrame(data, index=[0])[features]
    
    # Prétraiter les données
    mlb = MultiLabelBinarizer()
    df_cast = pd.DataFrame(mlb.fit_transform(df.pop('cast')), columns=mlb.classes_, index=df.index)
    df_director = pd.DataFrame(mlb.fit_transform(df.pop('director')), columns=mlb.classes_, index=df.index)
    df_genres = pd.DataFrame(mlb.fit_transform(df.pop('genres')), columns=mlb.classes_, index=df.index)
    df_production_companies = pd.DataFrame(mlb.fit_transform(df.pop('production_companies')), columns=mlb.classes_, index=df.index)
    df = df.join(df_cast).join(df_director).join(df_genres).join(df_production_companies)
    
    # Normaliser les caractéristiques
    scaled_features = scaler.transform(df)
    
    # Faire la prédiction
    prediction = model.predict(scaled_features)
    
    # Retourner la prédiction
    return jsonify({'prediction': prediction.tolist()})

@app.route('/test', methods=['GET'])
def test():
    return 'API is working.'

if __name__ == '__main__':
    app.run(port=5000)
