from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Charger le modèle entraîné depuis le fichier pickle
ridge_model = joblib.load('linear_model.pkl')

# Lire les colonnes depuis le fichier colonnes.txt
with open('columns.txt', 'r') as file:
    expected_columns = file.read().splitlines()

def create_columns(test_data):
    columns = []
    for feature, values in test_data.items():
        if isinstance(values, list):
            for value in values:
                columns.append(f"{feature}_{value}")
        elif feature not in ['runtime', 'budget_adj']:
            columns.append(f"{feature}_{values}")
    return columns

def preprocess_test_data(test_data, expected_columns):
    test_array = []
    generated_columns = create_columns(test_data)
    for col in expected_columns:
        if col in generated_columns:
            test_array.append(1)
        elif col == 'runtime':
            test_array.append(test_data['runtime'])
        elif col == 'budget_adj':
            test_array.append(test_data['budget_adj'])
        else:
            test_array.append(0)
    return test_array

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données envoyées en POST
    json_data = request.get_json()

    # Prétraiter les données de test
    test_array = preprocess_test_data(json_data, expected_columns)

    # Faire des prédictions sur les données de test
    predicted_revenue = ridge_model.predict([test_array])

    # Retourner les prédictions au format JSON
    return jsonify({'predicted_revenue': predicted_revenue[0]})

if __name__ == '__main__':
    app.run(debug=True)
