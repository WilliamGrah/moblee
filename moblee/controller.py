import data
import json
import helper


def get_data(request):
    filter = helper.get_params(request)
    result = data.get(filter)
    
    if not result:
        json = {}
    else:
        json = helper.parse_data(result)
    return json


def clean_table():
    data.clean()


