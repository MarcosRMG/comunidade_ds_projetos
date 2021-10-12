import pandas as pd
import inflection
from sklearn.preprocessing import MinMaxScaler, RobustScaler, LabelEncoder
import math
from datetime import datetime, timedelta
import numpy as np


class Rossmann:
    '''
    --> Deploy Rossmann prediction model
    '''
    def __init__(self, data=None):
        '''
        :param data: Pandas DataFrame to make a sales predictions
        '''
        self._data = data
        
        
    def data_cleaning(self):
        '''
        --> Cleaning data to properly data types and appropriate format
        '''
        ## Rename Columns
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment', 
                    'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 
                    'Promo2SinceYear', 'PromoInterval']

        # Renomeando as colunas para o padrão snacke case
        snackecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snackecase, cols_old))
        self._data.columns = cols_new

        # Types
        self._data['date'] = pd.to_datetime(self._data['date'])

        # Fill NaN            
        self._data['competition_distance'] = self._data['competition_distance'].apply(lambda x: 200000.0 if math.isnan(x) else x)
        self._data['competition_open_since_month'] = self._data.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)
        self._data['competition_open_since_year'] = self._data.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)
        self._data['promo2_since_week'] = self._data.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)
        self._data['promo2_since_year'] = self._data.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)


        # promo_interval

        month_map = {1: 'Jan',
                    2: 'Feb',
                    3: 'Mar',
                    4: 'Apr',
                    5: 'May',
                    6: 'Jun',
                    7: 'Jul',
                    8: 'Aug',
                    9: 'Sep',
                    10: 'Oct',
                    11: 'Nov',
                    12: 'Dec'}

        self._data['promo_interval'].fillna(0, inplace=True)
        self._data['month_map'] = self._data['date'].dt.month.map(month_map)

        self._data['is_promo'] = self._data[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1)

        ## Change Data Types
        self._data['competition_open_since_month'] = self._data['competition_open_since_month'].astype(int)
        self._data['competition_open_since_year'] = self._data['competition_open_since_year'].astype(int)
        self._data['promo2_since_week'] = self._data['promo2_since_week'].astype(int)
        self._data['promo2_since_year'] = self._data['promo2_since_year'].astype(int)
    
    
    def feature_engenering(self):
        '''
        --> Create news features to model performance
        '''
        ### Feature Engineering
        # year
        self._data['year'] = self._data['date'].dt.year

        # month
        self._data['month'] = self._data['date'].dt.month

        # day
        self._data['day'] = self._data['date'].dt.day

        # week of year
        self._data['week_of_year'] = self._data['date'].dt.isocalendar().week

        # year week
        self._data['year_week'] = self._data['date'].dt.strftime('%Y-%W')

        # competition since
        self._data['competition_since'] = self._data.apply(lambda x: datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1)
        self._data['competition_time_month'] = ((self._data['date'] - self._data['competition_since']) / 30).apply(lambda x: x.days).astype(int)

        # promo since
        self._data['promo_since'] = self._data['promo2_since_year'].astype(str) + '-' + self._data['promo2_since_week'].astype(str)
        self._data['promo_since'] = self._data['promo_since'].apply(lambda x: datetime.strptime(x + '-1', '%Y-%W-%w') - timedelta(days=7))
        self._data['promo_time_week'] = ((self._data['date'] - self._data['promo_since']) / 7).apply(lambda x: x.days).astype(int)

        # Assortment
        self._data['assortment'] = self._data['assortment'].apply(lambda x: 'basic' if x == 'a' else 'extra' if x == 'b'else 'extended')

        # state holiday
        self._data['state_holiday'] = self._data['state_holiday'].apply(lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day')

        ## Data Filter
        ### Row Filter
        #self._data = self._data[(self._data['open'] != 0) & (self._data['sales'] > 0)]

        ### Columns Filter
        self._data.drop(['open', 'promo_interval', 'month_map'], axis=1, inplace=True)
    
    
    def data_preparation(self):
        '''
        --> Data preparation to Machine Learning model
        '''
        ## Rescaling
        mms = MinMaxScaler()
        rs = RobustScaler()

        # Robust Scaler
        # competition_distance
        self._data['competition_distance'] = rs.fit_transform(self._data[['competition_distance']].values)

        # competition_time_month
        self._data['competition_time_month'] = rs.fit_transform(self._data[['competition_time_month']].values)

        # Min Max Scaler
        # promo_time_week
        self._data['promo_time_week'] = mms.fit_transform(self._data[['promo_time_week']].values)

        # year
        self._data['year'] = mms.fit_transform(self._data[['year']].values)

        ### Encoding
        # State Holiday - OheHotEncoding
        self._data = pd.get_dummies(self._data, prefix=['state_holiday'], columns=['state_holiday'])

        # Store Type - Label Encoding
        le = LabelEncoder()
        self._data['store_type'] = le.fit_transform(self._data['store_type'])

        # Assortment - Ordina encoding
        store_type = {'basic': 1, 'extra': 2, 'extended': 3}
        self._data['assortment'] = self._data['assortment'].map(store_type)

        ### Response Variable Transformation
        # response variable normalization
        #self._data['sales'] = np.log1p(self._data['sales'])

        ### Nature Transformation 
        # day_of_week
        self._data['day_of_week_sin'] = self._data['day_of_week'].apply(lambda x: np.sin(x * (2 * np.pi / 7)))
        self._data['day_of_week_cos'] = self._data['day_of_week'].apply(lambda x: np.cos(x * (2 * np.pi / 7)))

        # month
        self._data['month_sin'] = self._data['month'].apply(lambda x: np.sin(x * (2 * np.pi / 12)))
        self._data['month_cos'] = self._data['month'].apply(lambda x: np.cos(x * (2 * np.pi / 12)))

        #day
        self._data['day_sin'] = self._data['day'].apply(lambda x: np.sin(x * (2 * np.pi / 30)))
        self._data['day_cos'] = self._data['day'].apply(lambda x: np.cos(x * (2 * np.pi / 30)))

        # week_of_year
        self._data['week_of_year_sin'] = self._data['week_of_year'].apply(lambda x: np.sin(x * (2 * np.pi / 52)))
        self._data['week_of_year_cos'] = self._data['week_of_year'].apply(lambda x: np.cos(x * (2 * np.pi / 52)))

        cols_selected_boruta = [
         'store',
         'promo',
         'store_type',
         'assortment',
         'competition_distance',
         'competition_open_since_month',
         'competition_open_since_year',
         'promo2',
         'promo2_since_week',
         'promo2_since_year',
         'competition_time_month',
         'promo_time_week',
         'day_of_week_sin',
         'day_of_week_cos',
         'month_cos',
         'day_sin',
         'day_cos',
         'week_of_year_cos'
        ]

        self._data = self._data[cols_selected_boruta] 
    
    
    def get_prediction(self, model, readable_data):
        '''
        --> Realize the prediction of sales
        
        :param model: Machine Learning model to be use
        :param readable_data: DataFrame Pandas with raw data to be predict in readable
        '''
        # prediction
        pred = model.predict(self._data)
        
        # join prediction to original data
        readable_data['prediction'] = np.expm1(pred)
        
        return readable_data.to_json(orient='records', date_format='iso')
