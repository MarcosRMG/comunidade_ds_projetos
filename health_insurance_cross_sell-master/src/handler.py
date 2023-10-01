import pickle
from auto_insurance.auto_insurance import AutoInsurance
from flask import Flask, request, Response
import pandas as pd
import os


model = pickle.load(open('model/logistic_regression.pkl', 'rb'))

# Initialize API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def health_insurance_predict():
    test_json = request.get_json()
    
    if test_json: # There is data
        if isinstance(test_json, dict): # Unique example
            test_raw = pd.DataFrame(test_json, index=[0])
        else: # Multiple example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Health Insurance Class
        pipeline = AutoInsurance(test_raw)
        pipeline.data_clean()
        pipeline.data_preparation()
        pipeline.feature_selection()
        df_response = pipeline.ranking_model(model=model, original_data=test_raw)
        return df_response
    else:
        return Response('{}', status=200, mimetype='application/json')
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)