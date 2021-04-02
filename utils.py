from datetime import datetime
from notion.client import NotionClient

def fix_title(title):
    title_length = len(title.split())
    if title_length > 1
        first, rest = title.split(None, 1)
        if first in {'A', 'An', 'The'}:
            return rest + ', ' + first
    return title

def getBook(token, collectionURLBook, title):
    client = NotionClient(token)
    cvBook = client.get_collection_view(collectionURLBook)
    for row in cvBook.collection.get_rows(search=title):
        if row.title == fix_title(title):
            authorId = row.id
            return authorId

def addGoodReadsPercent(token, collectionURL, collectionURLBook, title, percent):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    date = datetime.now()
    row.date = date
    percent = int(percent)
    percent = float(percent/100)
    row.percent = percent
    titleDate = datetime.strftime(date, "%m/%d/%Y")
    titleBook = title + " | " + titleDate
    row.title = titleBook
    row.book = getBook(token, collectionURLBook, title)
    return