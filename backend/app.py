from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('model/climate_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    year = data['year']
    state_id = data['state_id']

    # Prepare input
    input_df = pd.DataFrame({'year': [year], 'state_id': [state_id]})
    input_df = pd.get_dummies(input_df)

    # Ensure correct columns
    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model.feature_names_in_]

    prediction = model.predict(input_df)[0]
    return jsonify({'predicted_temp': round(prediction, 2)})

if __name__ == '__main__':
    app.run(debug=True)
