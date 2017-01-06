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

def clean_db():
	conn = sqlite3.connect('stackdata.db')
	c = conn.cursor()
	c.execute('DELETE FROM stackdata')
	conn.commit()
	c.close()


@route('/getdata',method="GET")
def getdata():
	clean_db()
	url = "https://api.stackexchange.com/2.2/questions?page=1&pagesize=100&order=desc&sort=creation&tagged=php&site=stackoverflow"
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()

	prepare_data(data)


def parse_data(data):
	response = {"last_update":data[0][7], "content":[]}
	for i in data:
		json = {}
		json["question_id"] = i[0]
		json["title"] = i[1]
		json["owner_name"] = i[2]
		json["score"] = i[3]
		json["creation_date"] = i[4]
		json["link"] = i[5]
		json["is_answered"] = i[6]
		response["content"].append(json)
	return response

@route('/', method="GET")
def page():
	return static_file("index.html", root="source/html")


def showdata(filter):
	conn = sqlite3.connect('stackdata.db')
	c = conn.cursor()
	c.execute("SELECT * FROM stackdata {filter}".format(filter=filter))
	data = c.fetchall()
	c.close()
	if not data:
		json = {}
	else:
		json = parse_data(data)
	return json

@route('/stack_moblee/v1/question', method="GET")
def search():
	query = ""

	if request.GET['score']:
		query = query + " WHERE score > "+request.GET['score']

	if request.GET['sort']:
		query = query + " ORDER BY "+request.GET['sort']+" DESC"

	if request.GET['page'] and request.GET['rpp']:
		page = int(request.GET['page'])-1
		offset = int(page) * int(request.GET['rpp'])
		query = query + " LIMIT "+str(request.GET['rpp'])+" OFFSET "+str(offset)
	
	return showdata(query)

run(host='localhost', port=8080, debug=True, reloader=True)