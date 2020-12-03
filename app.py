import os
from dateutil import parser
from dateutil import tz
from datetime import datetime
from notion.client import NotionClient
from flask import Flask
from flask import request
from rq import Queue
from worker import conn
from utils import addGoodReadsPercent

app = Flask(__name__)

q = Queue(connection=conn)

def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content


@app.route('/create_todo', methods=['GET'])
def create_todo():

    todo = request.args.get('todo')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo)
    return f'added {todo} to Notion'


@app.route('/add_percent', methods=['GET'])
def add_percent():

    title = str(os.environ.get('TITLE'))
    percent = request.args.get('percent')
    #date = str(request.args.get('date'))
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    urlb = os.environ.get("URLB")
    q.enqueue(addGoodReadsPercent, 
        args=(token_v2, url, urlb, title, percent,)
    )
    return f'Added {percent} for {title} to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
