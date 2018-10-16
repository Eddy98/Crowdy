from flask import Flask, render_template, request
import requests
import json
import sys
sys.path.append("..")
from theater import theater

app = Flask(__name__, template_folder='../../client/templates')

#Homepage - takes in location and radius input from user
@app.route('/')
def index():
	return render_template('index.html')

#Retrieves all theaters by location and radius
@app.route('/theaters', methods = ['POST', 'GET'])
def get_all_theaters():
	#Retrieves location and radius from the form data
	if request.method == 'POST':
      		locationString = request.form['Location']
		radiusString = request.form['Radius']

	#Converts location string to longitude and latitude radiusString
	geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json"
	paramsGeocode = dict(
		address=locationString,
		key='AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI'
	)
	resp = requests.get(url=geocodeUrl, params=paramsGeocode).content
	respParse = json.loads(resp)
	lng = str(respParse["results"][0]["geometry"]["location"]["lng"])
	lat = str(respParse["results"][0]["geometry"]["location"]["lat"])

	#Finds movie theaters based on longitude and latitude and radius
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	params = dict(
		location=lat + ',' + lng,
		radius=radiusString,
		type='movie_theater',
		key='AIzaSyBBABVNXk90RVdvQqgDanDifw-bgMGeONI'
	)
	data = requests.get(url=url, params=params).content
	parseData = json.loads(data)
	list = []

	for item in parseData["results"]:
		tempT = theater()
		tempT.name = item["name"]
		tempT.address = item["vicinity"]
		#tempT.rating = item["rating"]
		list.append(tempT)

	return render_template('display_theaters.html', list=list)

if __name__ == '__main__':
	app.run(debug = True)
