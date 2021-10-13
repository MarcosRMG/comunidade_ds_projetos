import pandas as pd
import json
import requests
from flask import Flask, request, Response


# Token telegram
token = '2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds'

# Info about the bot
#api.telegram.org/bot2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds/getMe

# Get update
#api.telegram.org/bot2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds/getUpdates

# Webhook
#api.telegram.org/bot2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds/setWebhook?url=https://e2c045b789d17c.lhr.domains 

# Send message
#api.telegram.org/bot2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds/sendMessage?chat_id=766366754&text=Hello!

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
		
		
	def load_dataset(self, test='/home/marcos/Documents/data_science_em_producao/data/rossmann-store-sales/test.csv', 
					store='/home/marcos/Documents/data_science_em_producao/data/rossmann-store-sales/store.csv'):
		'''
		--> Load a dataset refered to store id
		'''
		test = pd.read_csv(test)
		store = pd.read_csv(store)

		# Merge data 
		self._data = pd.merge(test, store, how='left', on='Store')

		# Chose store to prediction
		self._data = self._data[self._data['Store'] == self._store_id]

		if not self._data.empty:
			# Remove closed days
			self._data = self._data[self._data['Open'] != 0]
			self._data = self._data[~self._data['Open'].isnull()]
			self._data.drop('Id', axis=1, inplace=True)

			# Convert to json
			self._data = json.dumps(self._data.to_dict(orient='records'))
		else:
			self._data = 'error'
		
	
	def predict(self):
		'''
		--> Send information to Rossmann API calculate the prediction
		'''
		# API call
		url = 'https://rossmann-stores-sales-pred.herokuapp.com/rossmann/predict'
		header = {'Content-type': 'application/json'}


		r = requests.post(url, data=self._data, headers=header)
		print(f'Status Code {r.status_code}')

		d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())
		
		return d1


def send_message(text, chat_id='766366754', token='2012004284:AAHeN2twKJBBHgHaIb0pu5MNXQUc1R6oeds'):
	'''
	--> Send a messagem to telegram app
	'''
	url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}'.format(token, chat_id)
	
	r = requests.post(url, json={'text': text})
	print(f'Status Code {r.status_code}')


def parse_message(message):
	'''
	--> Took chat id and store id from telegram message
	'''
	chat_id = message['message']['chat']['id']
	store_id = message['message']['text']	

	store_id = store_id.replace('/', '')

	try:
		store_id = int(store_id)
	except ValueError:
		store_id = 'error'

	return chat_id, store_id

# Api initialize
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		message = request.get_json()

		chat_id, store_id = parse_message(message)

		if store_id != 'error':
			data = RossmannBot(store_id)
			data.load_dataset()

			if data != 'error':
				# Prediction
				d1 = data.predict()
				# Calculation
				d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()	
				# Message
				msg = f'''Store: {d2["store"].values[0]}
					      Prediction: ${d2["prediction"].values[0]} (next 6 weeks)'''   

				send_message(msg, chat_id)
				return Response('Ok', status=200)

			else:
				send_message('Store not available', chat_id)
				return Response('Ok', status=200)
		else:
			send_message('Store Id is Wrong', chat_id)
			return Response('Ok', status=200)
	else:
		return '<h1>Rossmann Telegram Bot</h1>'
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
