import pandas as pd
import pickle
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import os


model = pickle.load(open('models/xgb_model_tuned.pickle', 'rb'))

app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: # there is data
        if isinstance(test_json, dict): # unique example
            test_raw = pd.DataFrame(test_json, index=[0])
        else: # multiple example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
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
