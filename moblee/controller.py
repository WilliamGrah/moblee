import data
import helper
import urllib2
import gzip
from StringIO import StringIO


def get_data(request):
    filter = helper.get_params(request)
    result = data.get(filter)

    if not result:
        json = {}
    else:
        json = helper.parse_data(result)
    return json


def prepare_data():
    data.clean()

    url = (
            "https://api.stackexchange.com/2.2/questions?page=1&pagesize=99"
            "&order=desc&sort=creation&tagged=php&site=stackoverflow"
            )

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        result = f.read()

    helper.prepare_data(result)
