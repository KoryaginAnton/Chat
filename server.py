from flask import Flask, request, abort
import time
import json
from datetime import datetime

app = Flask(__name__)
base_data = []


@app.route("/")
def hello():
    return "Messager // Koryagin A.A."


@app.route("/status")
def status():
    dt = datetime.now()
    status_server = [{
        'status': True,
        'name': 'Говорилка',
        'time': dt.strftime('%Y/%m/%d %H:%M:%S')
    }]
    return json.dumps(status_server, ensure_ascii=False, indent=4, separators=(". ", " = "), sort_keys=True, )


@app.route("/send", methods=['POST'])
def send():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    name = data['name']
    text = data['text']
    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if not 0 < len(name) <= 64:
        return abort(400)
    if not 0 < len(text) <= 10000:
        return abort(400)
    base_data.append({
        'name': name,
        'text': text,
        'time': time.time()
    })
    return {}


@app.route("/messages")
def messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    filtered_massages = []
    for message in base_data:
        if message['time'] > after:
            filtered_massages.append(message)
    return {'messages': filtered_massages[:50]}


app.run()
