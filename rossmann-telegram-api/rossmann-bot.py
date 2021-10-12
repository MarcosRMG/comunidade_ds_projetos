import pandas as pd
import json
import requests


# Load data
class RossmannBot:
	'''
	--> Respond a requisition from telegram
	'''
	def __init__(self, store_id=None, data=None):
		'''
		:param store_id: Store id to respond a sales prediction
		:param data: Pandas DataFrame with result of prediction
		'''
		self._store_id = store_id
		self._data = data
		
		
	def load_dataset():
		'''
		--> Load a dataset refered to store id
		'''
		df10 = pd.read_csv('../data/rossmann-store-sales/test.csv')
		df_store_raw = pd.read_csv('../data/rossmann-store-sales/store.csv')

		# Merge data 
		df_test = pd.merge(df10, df_store_raw, how='left', on='Store')

		# Chose store to prediction
		df_test = df_test[df_test['Store'] == store_id]

# Remove closed days
df_test = df_test[df_test['Open'] != 0]
df_test = df_test[~df_test['Open'].isnull()]
df_test.drop('Id', axis=1, inplace=True)

# Convert to json
data = json.dumps(df_test.to_dict(orient='records'))

# API call
#url = 'http://0.0.0.0:5000/rossmann/predict'
url = 'https://rossmann-stores-sales-pred.herokuapp.com/rossmann/predict'
header = {'Content-type': 'application/json'}


r = requests.post(url, data=data, headers=header)
print(f'Status Code {r.status_code}')

d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())
d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()
d2

for i in range(len(d2)):
    print(f'Store: {d2.loc[i, "store"]}')
    print(f'Prediction: ${d2.loc[i, "prediction"]:,.2f} (next 6 weeks)\n')    
