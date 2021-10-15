import pandas as pd
import json
import requests
from flask import Flask, request, Response
import os


# Token telegram
with open('token/telegram.txt') as file:
	token = file.read()
file.close()

# Info about the bot
#api.telegram.org/botTelegramToken/getMe

# Get update
#api.telegram.org/botTelegramToken/getUpdates

# Webhook
#api.telegram.org/botTelegramToken/setWebhook?url=https://cb9fb1eab076af.lhr.domains 

# Webhook heroku
#api.telegram.org/botTelegramToken/setWebhook?url=https://bot-rossman.herokuapp.com 

# Send message
#api.telegram.org/botTelegramToken/sendMessage?chat_id=766366754&text=Hello!

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
		
		
	def load_dataset(self, test='test.csv', store='store.csv'):
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
		url = 'https://sales-rossmann-prediction.herokuapp.com/rossmann/predict'
		header = {'Content-type': 'application/json'}


		r = requests.post(url, data=self._data, headers=header)
		print(f'Status Code {r.status_code}')

		df_prediction = pd.DataFrame(r.json(), columns=r.json()[0].keys())
		
		return df_prediction


def send_message(text, chat_id='766366754', token_telegram=token):
	'''
	--> Send a messagem to telegram app
	'''
	url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}'.format(token_telegram, chat_id)
	
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

# Api initialize / receive a message from telegram app bot
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		message = request.get_json()

		chat_id, store_id = parse_message(message)

		if store_id != 'error':
			data = RossmannBot(store_id)
			data.load_dataset()

			if data._data != 'error':
				# Prediction
				df_prediction = data.predict()
				# Calculation
				df_prediction_agg = df_prediction[['store', 'prediction']].groupby('store').sum().reset_index()	
				# Message with sales prediction
				msg = f'Store: {df_prediction_agg["store"].values[0]}\nSales Prediction: ${df_prediction_agg["prediction"].values[0]:,.2f} (next 6 weeks)'   

				send_message(msg, chat_id)
				return Response('Ok', status=200)

			else: # User type a store number that not exist
				send_message('Store not available', chat_id)
				return Response('Ok', status=200)
		else: # User type another information 
			send_message('Store Id is Wrong', chat_id)
			return Response('Ok', status=200)
	else: # Any informaton isn't send
		return '<h1>Rossmann Telegram Bot</h1>'
	
if __name__ == '__main__':
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)
