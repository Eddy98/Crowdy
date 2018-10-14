from flask import Flask, render_template
import requests
import json
import sys
sys.path.append("/Users/eduardo/Crowdy/server/models")
from theater import theater


app = Flask(__name__, template_folder='../../client/templates')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/place')
def getInfo():
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	params = dict(
		location='29.651634,-82.324829',
		radius='20000',
		type='movie_theater',
		key='AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI'
	)
	# data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=29.651634,-82.324829&radius=20000&type=movie_theater&key=AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI').content
	data = requests.get(url=url, params=params).content
	#data = resp.json()
	parseData = json.loads(data)

	list = []

	for item in parseData["results"]:
		tempT = theater()
		tempT.name = item["name"]
		tempT.address = item["vicinity"]
		tempT.rating = item["rating"]
		list.append(tempT)

	for x in list:
		print x.name
		print x.address
		print x.rating
		print '\n'

	return data

if __name__ == '__main__':
	app.run(debug = True) 



