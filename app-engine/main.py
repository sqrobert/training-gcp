import datetime
from flask import Flask, render_template
from google.cloud import datastore

app = Flask(__name__)
ds = datastore.Client()

def log_visit(dt):
    entity = datastore.Entity(key=ds.key("visit"))
    entity.update({ "timestamp" : dt })

    ds.put(entity)

def fetch_visits(limit):
    query = ds.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

@app.route('/')
def root():
    # Store the current access time in Datastore.
    log_visit(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_visits(10)

    return render_template('index.html', times=times)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)