from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from itertools import product

app = Flask(__name__)
cors = CORS(app)

ridge_model = joblib.load('linear_model.pkl')

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

def predict_revenue(test_data):
    # Récupérer toutes les colonnes attendues pour chaque combinaison
    generated_columns = create_columns(test_data)
    
    # Créer un tableau de test pour chaque combinaison
    test_array = []
    for col in expected_columns:
        if col in generated_columns:
            test_array.append(1)
        elif col == 'runtime':
            test_array.append(float(test_data['runtime']))
        elif col == 'budget_adj':
            test_array.append(float(test_data['budget_adj']))  
        else:
            test_array.append(0)
    
    # Prédire le revenu pour la combinaison actuelle
    predicted_revenue = ridge_model.predict([test_array])[0]
    
    return predicted_revenue

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()

        if not json_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Générer toutes les combinaisons possibles des caractéristiques spécifiées
        combinations = list(product(json_data["cast"], json_data["director"], json_data["genres"], json_data["production_companies"]))
        
        print(combinations)
        # Prédire et stocker les revenus pour chaque combinaison
        predicted_revenues = []
        for combination in combinations:
            test_data = {
                'cast': combination[0],
                'director': combination[1],
                'genres': combination[2],
                'production_companies': combination[3],
                'runtime': json_data['runtime'],
                'budget_adj': json_data['budget_adj']
            }
            predicted_revenues.append(predict_revenue(test_data))    

        # print(predicted_revenues)   
        
        # Calculer la prédiction moyenne
        average_predicted_revenue = sum(predicted_revenues) / len(predicted_revenues)

        return jsonify({'predicted_revenue': average_predicted_revenue}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)
