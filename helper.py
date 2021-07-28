import csv
from datetime import date
from os import stat

def save_details(details):
	with open('contacts.csv', 'a', newline='') as csvfile:
		fieldnames = ['status', 'number', 'name', 'item', 'images']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow(details)

def saveContact(contact):
	with open('contacts.txt', 'r+', newline='') as doc:
		if contact not in doc.read():
			doc.write(contact) #read() made pointer go to the end of the file so now we can append safely
			return False #if not already known
	return True

def change_csv_header(path, newHeader):
	with open(path, 'r', newline='') as doc:
		old=[row for row in csv.reader(doc)]
	old[0]=newHeader
	with open(path, 'w', newline='') as doc:
		writer=csv.writer(doc)
		for row in old:
			writer.writerow(row)

def saveConversation(conv, number): #number+convNumber, date
	today=date.today().strftime("%d/%m/%Y")
	empty=False
	header=[]
	with open('conversations.csv', 'r', newline='') as doc:
		try: header = next(csv.reader(doc))
		except StopIteration: empty=True
	
	if len(header)==0:
		empty=True
		header=['number', today]
		
	if header[-1]!=today:
		header.append(today)
		if not empty:
			change_csv_header('conversations.csv', header)
	
	with open('conversations.csv', 'a', newline='') as doc:
		writer = csv.DictWriter(doc, fieldnames=header)
		if empty:
			 writer.writeheader()
		writer.writerow({'number': number, today: conv})

def csv_to_list(path):
	with open(path, 'r', newline='') as doc:
		return [row for row in csv.reader(doc)]

