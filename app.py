
import os
from dateutil import parser
from dateutil import tz
from datetime import datetime
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)


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

def addGoodReadsPercent(token, collectionURL, title, percent, date):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    #row.title = title
    #CST = tz.gettz('America/Chicago')
    #dateTest = "2020-11-05 10:49:18"
    date = parser.parse(date)
    row.date = date
    percent = int(percent)
    percent = float(percent/100)
    row.percent = percent
    titleDate = datetime.strftime(date, "%M %d %Y")
    title = title + " | " + titleDate
    row.title = title


@app.route('/add_percent', methods=['GET'])
def add_percent():

    title = request.args.get('title')
    percent = request.args.get('percent')
    date = str(request.args.get('date'))
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    addGoodReadsPercent(token_v2, url, title, percent, date)
    return f'added {percent} to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
