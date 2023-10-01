import pandas as pd
import pickle


class AutoInsurance:
    '''
    --> Clean, transformate and training data to ranking customers
    '''
    def __init__(self, data): 
        '''
        --> Customers information to calculate probabilities
        '''      
        self._data                      = data
        self._target_gender             = pickle.load(open('features/target_gender.pkl', 'rb'))
        self._target_region_code        = pickle.load(open('features/target_region_code.pkl', 'rb'))
        self._age_scaler                = pickle.load(open('features/age_min_max_scaler.pkl', 'rb'))
        self._annual_premium_scaler     = pickle.load(open('features/annual_premium_standard_scaler.pkl', 'rb'))
        self._freq_policy_sales_channel = pickle.load(open('features/freq_policy_sales_channel.pkl', 'rb')) 
        self._vintage_scaler            = pickle.load(open('features/vintage_min_max_scaler.pkl', 'rb'))
        
      
    def data_clean(self):
        '''
        --> Change the format of data in vehicle age and vehicle damage columns
        '''
        self._data['vehicle_age'] = self._data['vehicle_age'].apply(lambda x: 'below_1_year' if x == '< 1 Year' 
                                                                    else 'between_1_2_year' if x == '1-2 Year' 
                                                                    else 'over_2_years')
        self._data['vehicle_damage'] = self._data['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)
        
        
    def data_preparation(self):
        '''
        --> Prepare data to modeling
        '''
        # Gender | Target Encoder
        self._data['gender'] = self._data['gender'].map(self._target_gender)
        
        # vehicle age
        self._data = pd.get_dummies(self._data, columns=['vehicle_age'])
        
        # policy_sales_channel
        self._data.loc[:, 'policy_sales_channel'] = self._data['policy_sales_channel'].map(self._freq_policy_sales_channel)
        
        # Region code
        self._data.loc[:, 'region_code'] = self._data['region_code'].map(self._target_region_code)
        
        # Anual premium
        self._data['annual_premium'] = self._annual_premium_scaler.transform(self._data[['annual_premium']].values)
        
        # Age | MinMaxScale
        self._data['age'] = self._age_scaler.transform(self._data[['age']].values)
        
        # Vintage
        self._data['vintage'] = self._vintage_scaler.transform(self._data[['vintage']].values)
        
        
    def feature_selection(self):
        cols_selected = ['annual_premium', 'previously_insured', 'gender', 'age', 'driving_license', 
                         'region_code', 'vehicle_damage']
        self._data = self._data[cols_selected]
        

    def ranking_model(self, model, original_data):
        # Prediction
        yhat_lr = model.predict_proba(self._data)
        original_data['score'] = yhat_lr[:, 1].tolist()
        original_data.sort_values('score', ascending=False, inplace=True)
        return original_data.to_json(orient='records', date_format='iso')