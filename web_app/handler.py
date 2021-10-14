import pandas as pd
import pickle
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import os


model = pickle.load(open('model/xgb_model_tuned.pickle', 'rb'))

app = Flask(__name__)
# Receive a request an return a prediction
@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    json = request.get_json()
    
    if json: # there is data
        if isinstance(json, dict): # unique example
            test_raw = pd.DataFrame(json, index=[0])
        else: # multiple example
            test_raw = pd.DataFrame(json, columns=json[0].keys())
            
        # Instantiate Rossman Class
        pipeline = Rossmann(test_raw)
        pipeline.data_cleaning()
        pipeline.feature_engenering()
        pipeline.data_preparation()
        return pipeline.get_prediction(model, test_raw)
    else:
        return Response('{}', status=200, mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
