from flask import Flask, request, send_file, render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse

from conversation import *
from helper import *
from pprint import pprint
from collections import defaultdict
import pandas

app = Flask(__name__)

replies=[hello, giveOrTake, give, take, give_name, take_name, give_image]
context=defaultdict(dict)
conversations=defaultdict(str)

@app.route('/contacts', methods=['GET'])
def contacts():
	return pandas.read_csv('contacts.csv').to_html(escape=False)

@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
	if request.method == 'POST': #probably a button press (not necessarily though)
		print(request.form.getlist('number'))
	return render_template('table.html', data_list=csv_to_list('conversations.csv'))

@app.route('/bot', methods=['POST'])
def bot():
	global replies, context, conversations
	msg_dict = request.values
	
	incoming_msg = msg_dict['Body']
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	
	if 'conv_status' not in context[msg_dict['From']]:
		context[msg_dict['From']]['conv_status']=0
	known=saveContact(msg_dict['From'])
	pprint(context[msg_dict['From']])
	context[msg_dict['From']]['conv_status'], reply = replies[context[msg_dict['From']]['conv_status']](msg_dict, context[msg_dict['From']])
	
	conversations[msg_dict['From']]+='שולח:{}\n\n"{}"\n\nשולח:בוט\n\n"{}"\n'.format(msg_dict['From'], msg_dict['Body'], reply)
	
	if context[msg_dict['From']]['conv_status'] == -1:
		saveConversation(conversations[msg_dict['From']], msg_dict['From'])
		del conversations[msg_dict['From']]
		del context[msg_dict['From']]['conv_status']
		save_details({'number': msg_dict['From'], **context[msg_dict['From']]})
		del context[msg_dict['From']]
	msg.body(reply)
	return str(resp)


if __name__ == '__main__':
	app.run()
