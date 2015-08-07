from flask import Flask, url_for, request, render_template, jsonify, abort
from apiclient.discovery import build 
import json

DEBUG = True

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('config.txt')
MY_DEVELOPER_KEY = parser.get('KEY','MY_DEVELOPER_KEY')
SERVER = 'https://www.googleapis.com'
DISCOVERY_URL_SUFFIX = '/discovery/v1/apis/trends/v1beta/rest'
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/trends", methods = ['GET','POST'])
def trends():
	results = {}
	terms = request.args.get('terms')
	startDate = request.args.get('startDate')
	endDate = request.args.get('endDate')
	if (terms or startDate or endDate) is None:
		abort(500)
	if DEBUG:
		with open('../trendswidget/dummydata3.json') as data_file:
			json_obj = json.load(data_file)
			results = jsonify(json_obj)
	else:
		service = build('trends', 'v1beta', developerKey=MY_DEVELOPER_KEY, discoveryServiceUrl=DISCOVERY_URL)
		results = service.getGraph(terms=terms, restrictions_startDate=startDate, restrictions_endDate=endDate).execute()
	return results
	
if __name__ == "__main__":
	app.run(debug = True)
