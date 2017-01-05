from bottle import route, run, request

@route('/question', method="POST")
def search():
	page = request.forms.get('page')
	rpp = request.forms.get('rpp')
	sort = request.forms.get('sort')
	score = request.forms.get('score')
	return

run(host='localhost', port=8000, debug=True)