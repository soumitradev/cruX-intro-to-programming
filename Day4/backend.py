import flask

app = flask.Flask("backend")

records = {}


@app.route("/get/<id>", methods=["GET"])
def get(id):
    try:
        id = int(id)
    except:
        flask.abort(400)

    record = records.get(id, None)
    if not record:
        flask.abort(404)
    return record


@app.route("/create", methods=["POST"])
def create():
    data = flask.request.json
    id = len(records)
    name = data.get("name", None)
    authors = data.get("authors", None)
    if (not name) and (not authors):
        flask.abort(400)

    issued = bool(data.get("issued", None))
    if not issued:
        issued = False
    date_of_issue = data.get("date_of_issue", None)
    try:
        date_of_issue = int(date_of_issue)
    except:
        flask.abort(400)
    if not date_of_issue:
        date_of_issue = 0
    issue_duration = data.get("issue_duration", None)
    if not issue_duration:
        issue_duration = 0
    record = {
        "id": id,
        "name": name,
        "authors": authors,
        "issued": issued,
        "date_of_issue": date_of_issue,
        "issue_duration": issue_duration,
    }
    records[id] = record
    return record


app.run()
