from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Charger le modèle et le scaler
model = joblib.load('ridge_regression_model_alpha_100.joblib')
scaler = joblib.load('scaler.joblib')
mlb = joblib.load('mlb.joblib')

# Extraire les noms de colonnes à partir du MultiLabelBinarizer
mlb_feature_names = mlb.classes_

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données envoyées en POST
    json_data = request.get_json()

    # Créer un DataFrame à partir des données
    input_data = pd.DataFrame(json_data, index=[0])

    # Vérifier que les noms de colonnes sont cohérents avec ceux utilisés lors de l'entraînement
    if not set(input_data.columns) == set(mlb_feature_names):
        missing_features = set(mlb_feature_names) - set(input_data.columns)
        return jsonify({'error': f'Missing features: {missing_features}'}), 400

    # Prétraiter les données avec le MultiLabelBinarizer
    for col in ['cast', 'director', 'genres', 'production_companies']:
        input_data[col] = input_data[col].apply(lambda x: [x])  # Convertir chaque valeur en liste pour correspondre au format attendu par le mlb
        input_data[col] = mlb.transform(input_data[col])

    # Normaliser les données
    input_data_scaled = scaler.transform(input_data)

    # Faire la prédiction
    prediction = model.predict(input_data_scaled)

    # Formater la réponse
    response = {'prediction': prediction[0]}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
