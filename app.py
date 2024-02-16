from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

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

def preprocess_test_data(test_data, expected_columns):
    test_array = []
    required_features = ['cast', 'director', 'genres', 'production_companies', 'runtime', 'budget_adj']
    
    # Vérifier la présence des fonctionnalités requises
    for feature in required_features:
        if feature not in test_data:
            return None, f"Missing feature: {feature}"
    
    generated_columns = create_columns(test_data)
    for col in expected_columns:
        if col in generated_columns:
            test_array.append(1)
        elif col == 'runtime':
            test_array.append(float(test_data['runtime']))
        elif col == 'budget_adj':
            test_array.append(float(test_data['budget_adj']))  
        else:
            test_array.append(0)

    return test_array, None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()

        if not json_data:
            return jsonify({'error': 'No data provided'}), 400
        
        test_array, error_message = preprocess_test_data(json_data, expected_columns)
        if error_message:
            return jsonify({'error': error_message}), 400
        
        predicted_revenue = ridge_model.predict([test_array])

        return jsonify({'predicted_revenue': predicted_revenue[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)
