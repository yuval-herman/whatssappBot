from flask import Flask, request, send_file
import requests
from twilio.twiml.messaging_response import MessagingResponse

from conversation import *
from helper import *
from pprint import pprint
from collections import defaultdict

app = Flask(__name__)

replies=[hello, giveOrTake, give, take, give_name, take_name]
context=defaultdict(dict)

#TODO: load conversations from file
convs=[]

def saveContact(contact):
	with open('contacts.txt', 'r+') as doc:
		if contact not in doc.read():
			doc.write(contact) #read() made pointer go to the end of the file so now we can append safely
			return False #if not already known
	return True

@app.route('/data', methods=['GET'])
def data():
	return send_file('contacts.csv')

@app.route('/bot', methods=['POST'])
def bot():
	global replies, context
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
	if context[msg_dict['From']]['conv_status'] == -1:
		del context[msg_dict['From']]['conv_status']
		save_details({'number': msg_dict['From'], **context[msg_dict['From']]})
		context[msg_dict['From']]['conv_status']=0
	msg.body(reply)
	return str(resp)


if __name__ == '__main__':
	app.run()
