import csv

def save_details(details):
	with open('contacts.csv', 'a', newline='') as csvfile:
		fieldnames = ['status', 'number', 'name', 'item', 'images']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writerow(details)

