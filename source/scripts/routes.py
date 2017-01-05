import sqlite3
import json
import urllib2
import gzip
import time
from StringIO import StringIO

from bottle import route, run, request, static_file

def insert_into(data):
	conn = sqlite3.connect('stackdata.db')
	c = conn.cursor()
	c.execute('INSERT INTO stackdata VALUES (?, ?, ?, ?, ?, ?, ?, ?);', (data["question_id"], data["title"], data["owner_name"], data["score"], data["creation_date"], data["link"], data["is_answered"], data["last_update"]))
	conn.commit()
	c.close()

def prepare_data(data):
	jj = json.loads(data)
	last_update = int(time.time())

	for i in jj["items"]:
		values = dict()
		values["question_id"] = i["question_id"]
		values["title"] = i["title"]
		values["owner_name"] = i["owner"]["display_name"]
		values["score"] = i["score"]
		values["creation_date"] = i["creation_date"]
		values["link"] = i["link"]
		values["is_answered"] = i["is_answered"]
		values["last_update"] = last_update

		insert_into(values)

@route('/getdata',method="GET")
def getdata():
	url = "https://api.stackexchange.com/2.2/questions?page=1&pagesize=100&order=desc&sort=creation&tagged=php&site=stackoverflow"
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()

	prepare_data(data)

@route('/showdata',method="GET")
def showdata():
	conn = sqlite3.connect('stackdata.db')
	c = conn.cursor()
	c.execute("SELECT * FROM stackdata")
	data = c.fetchall()
	c.close()
	print(data)
	return str(data)

@route('/question', method="GET")
def page():
	return static_file("index.html", root="source/html")

@route('/question', method="POST")
def search():
	page = request.forms.get('page')
	rpp = request.forms.get('rpp')
	sort = request.forms.get('sort')
	score = request.forms.get('score')
	return

run(host='localhost', port=8080, debug=True, reloader=True)