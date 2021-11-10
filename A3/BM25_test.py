import json
import math
import os
import re
import glob
import timeit

from BM25 import BM25
from lib import save, save_pickle, size
from nltk import word_tokenize

corpus = []
reuters_files = []
REUTERS_FOLDER = "./reuters21578"


def trace_files():
    """Get all files and make a list to process each files."""
    os.chdir(REUTERS_FOLDER)
    for file in glob.glob("*.sgm"):
        reuters_files.append(REUTERS_FOLDER + "/" + file)
    os.chdir("..")


def parser(reuters_file):
    """Extract the raw text of each article from the corpus"""

    new_id_pattern = "NEWID=\"([\s\S]*?)\""
    title_pattern = "<TITLE>([\s\S]*?)</TITLE>"
    body_pattern = "<BODY>([\s\S]*?)</BODY>"

    with open(reuters_file) as fp:
        file_str = fp.read()
        articles = file_str.split("</REUTERS>")

        for article in articles:

            new_id = title = body = None

            if re.search(title_pattern, article) is not None:
                new_id = re.search(new_id_pattern, article).group(1)

            if re.search(title_pattern, article) is not None:
                title = re.search(title_pattern, article).group(1)

            if re.search(body_pattern, article) is not None:
                body = re.search(body_pattern, article).group(1)

            if new_id is None and title is None and body is None:
                pass  # Everything is Empty
            elif new_id is None:
                pass  # If can't fine ID then skip article
            else:
                # Process the Article
                yield new_id, str(title) + " " + str(body)


def text_cleaner(string):
    string = string.replace("&lt;", "").replace(".", "")
    string = re.sub('[^a-zA-Z0-9 \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    string = string.lower()
    return string


def tokenizer(text):
    return word_tokenize(text_cleaner(text))


def main():
    # Read All Reuters File Names
    trace_files()

    # Process All files one by one
    for reuters_file in reuters_files:
        # Parse Article in 1 file
        articles = parser(reuters_file)

        for new_id, article in articles:
            # Process Each Article One by One
            corpus.append(article)

        # corpus = [
        #     'Human machine interface for lab abc computer applications',
        #     'A survey of user opinion of computer system response time',
        #     'The EPS user interface management system',
        #     'System and human system engineering testing of EPS',
        #     'Relation of user perceived response time to error measurement',
        #     'The generation of random binary unordered trees',
        #     'The intersection graph of paths in trees',
        #     'Graph minors IV Widths of trees and well quasi ordering',
        #     'Graph minors A survey'
        # ]

        # remove stop words and tokenize them (we probably want to do some more
        # preprocessing with our text in a real world setting, but we'll keep
        # it simple here)
        stopwords = set(['for', 'a', 'of', 'the', 'and', 'to', 'in'])
        texts = [
            [word for word in document.lower().split() if word not in stopwords]
            for document in corpus
        ]

        # build a word count dictionary so we can remove words that appear only once
        word_count_dict = {}
        for text in texts:
            for token in text:
                word_count = word_count_dict.get(token, 0) + 1
                word_count_dict[token] = word_count

        texts = [[token for token in text if word_count_dict[token] > 1] for text in texts]

        # query our corpus to see which document is more relevant
        query = 'The intersection of graph survey and trees'
        query = [word for word in query.lower().split() if word not in stopwords]

        bm25 = BM25()
        bm25.fit(texts)
        scores = bm25.search(query)

        for score, doc in zip(scores, corpus):
            score = round(score, 3)
            print(str(score) + '\t' + doc)


if __name__ == '__main__':
    main()
