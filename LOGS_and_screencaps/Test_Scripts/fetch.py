
import requests
import time
import threading

def gibe():
	
	
	page = requests.get('http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSms%3E%28+%CD%A1%C2%B0+%CD%9C%CA%96+%CD%A1%C2%B0%29%3C%2FSms%3E%3C%2FResponse%3E')
	page = str(page.text)

	page=page.split("Sms>")
	page = page[1]
	page = page[:-2]

	

	threading.Timer(10, gibe).start()

	print(page)

gibe()
