import os, sys
from utils import wit_response, get_news_elements
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAbBcP1HPzUBAHQwUHAk3SlaizTdPyUclMVrMaRdY3uRJBItnmH6PCZCSlmEOAUzWTwZBZANfYX9RPgV1YwR2TF63f6xOImZBLt0ra1KXAG5W3K5yoOP5UYyeDmfJ3vxz3RtaOWEvjOWMWDFyEP76DC8vQPRX3UhRreNFWHXKAZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	#webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Verification token verify", 200



@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					# Echo
					categories = wit_response(messaging_text)
					elements = get_news_elements(categories)
					bot.send_generic_message(sender_id, elements)

	return "ok",200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)
