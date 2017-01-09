
def get_params(request):
    query = ""

    if request.GET['score']:
        query = query + " WHERE score > "+request.GET['score']

    if request.GET['sort']:
        query = query + " ORDER BY "+request.GET['sort']+" DESC"

    if request.GET['page'] and request.GET['rpp']:
        page = int(request.GET['page'])-1
        rpp = request.GET['rpp']
        offset = int(page) * int(rpp)
        query += " LIMIT " + str(rpp) + " OFFSET " + str(offset)

    return query


def parse_data(data):
    response = {"last_update": data[0][7], "content": []}
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