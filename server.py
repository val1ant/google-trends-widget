import os
from flask import Flask, url_for, request, render_template, jsonify, abort
from apiclient.discovery import build 
import json
from ConfigParser import SafeConfigParser

DEBUG = True

basedir = os.path.dirname(os.path.abspath(__file__))
parser = SafeConfigParser()
parser.read(os.path.join(basedir,'config.txt'))

MY_DEVELOPER_KEY = parser.get('KEY','MY_DEVELOPER_KEY')
SERVER = 'https://www.googleapis.com'
DISCOVERY_URL_SUFFIX = '/discovery/v1/apis/trends/v1beta/rest'
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/trends/", methods = ['GET','POST'])
def trends():
	results = {}
	terms = request.args.get('terms')
	startDate = request.args.get('start')
	endDate = request.args.get('end')
	if (terms or startDate or endDate) is None:
		abort(500)
	if DEBUG:
		with open('../google-trends-widget/dummydata3.json') as data_file: 
			results = json.load(data_file)
	else:
		service = build('trends', 'v1beta', developerKey=MY_DEVELOPER_KEY, discoveryServiceUrl=DISCOVERY_URL)
		results = service.getGraph(terms=terms, restrictions_startDate=startDate, restrictions_endDate=endDate).execute()
	return jsonify(results)
	
if __name__ == "__main__":
	app.run(debug = True)
