import pickle

from flask import Flask, render_template, request, flash, url_for, redirect

from BM25 import BM25
from lib import REUTERS_OUTPUT_FOLDER, measured_run, save_pickle

app = Flask(__name__)


# Custom Functions
def load_okapi_bm25_21578():
    try:
        with open(REUTERS_OUTPUT_FOLDER + "/pickle/okapi_bm25_21578.pickle", 'rb') as handle:
            okapi_bm25_21578 = pickle.load(handle)
    except:
        okapi_bm25_21578 = BM25()
        measured_run(okapi_bm25_21578.parser_collection, "Creation of Ranked Index for 21578")
        save_pickle(name="okapi_bm25_21578.pickle", content=okapi_bm25_21578)
    return okapi_bm25_21578


okapi_bm25 = load_okapi_bm25_21578()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return render_template('index.html', query="", result="Sorry, Query is required! :(", found=False)
    else:
        result = okapi_bm25.search(query)
        if result:
            table = []
            for pair in result:
                title = okapi_bm25.get_document_title(pair[0])
                table.append([pair[0], round(pair[1], 3), title])
            return render_template('index.html', query=query, result=table, found=True)
        else:
            return render_template('index.html', query=query, result="Sorry, No Match found :(", found=False)


@app.route('/article', methods=['GET'])
def article():
    new_id = request.args.get('id')
    if not new_id:
        return render_template('article.html', id=new_id, title="Sorry, ID is required! :(", found=False)
    else:
        new_id = int(new_id)
        if 1 <= new_id <= 21578:
            title = okapi_bm25.get_document_title(new_id)
            body = okapi_bm25.get_document_body(new_id)
            return render_template('article.html', id=new_id, title=title, body=body,found=True)
        else:
            return render_template('article.html', id=new_id, title="Sorry, Invalid ID :(", found=False)
