import json
import os
import re
import glob
import timeit
import time

from lib import save, save_pickle, measured_run, size
from nltk import word_tokenize

counter = 0
inverted_index = {}
reuters_files = []
REUTERS_FOLDER = "./reuters21578"

MAX_TOKEN_NUMBER = 10000
counter = START_TIME = STOP_TIME = 0
number_of_terms = number_of_postings = 0


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
                yield [new_id, tokenizer(str(title) + " " + str(body))]


def text_cleaner(string):
    string = string.replace("&lt;", "").replace(".", "")
    string = re.sub('[^a-zA-Z0-9 \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    return string


def tokenizer(text):
    tokens = word_tokenize(text_cleaner(text))
    return list(set(tokens))  # Using set() here to remove duplicate tokens


def process_article(article):
    doc_id, tokens = article
    for token in tokens:
        # Hash the token and ID
        hash(int(doc_id), token)


def hash(doc_id, term):
    """turn the sorted file F into an index by turning the docIDs paired with the same term into a postings list and
    setting the pointer """
    global inverted_index, counter, STOP_TIME
    if term not in inverted_index:
        inverted_index[term] = [doc_id]
    else:
        if doc_id not in inverted_index[term]:
            inverted_index[term].append(doc_id)

    if counter == MAX_TOKEN_NUMBER:
        STOP_TIME = timeit.default_timer()
    counter += 1


def main():
    global inverted_index, pairs
    # Read All Reuters File Names
    trace_files()

    # Process All files one by one
    for reuters_file in reuters_files:
        # Parse Article in 1 file
        articles = parser(reuters_file)
        for article in articles:
            # Process Each Article One by One
            process_article(article)

    # Write to Text File
    save(name="inverted_index_SPIMI.txt", content=json.dumps(inverted_index, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_SPIMI.pickle", content=inverted_index)


if __name__ == '__main__':
    START_TIME = timeit.default_timer()
    main()
    # Check Size
    print('Time to process', MAX_TOKEN_NUMBER, 'tokens is', round(STOP_TIME - START_TIME, 4), "Seconds")
    number_of_terms, number_of_postings = size(inverted_index)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
