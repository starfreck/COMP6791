import json
import operator
import os
import re
import glob
import timeit

import _pickle as pickle

from tabulate import tabulate

from lib import save, save_pickle, size, REUTERS_OUTPUT_FOLDER
from nltk import word_tokenize

inverted_index = {}
pairs = []
reuters_files = []
REUTERS_FOLDER = "./reuters21578"

number_of_terms = number_of_postings = 0

counter = START_TIME = STOP_TIME = 0
MAX_TOKEN_NUMBER = 10000


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


def make_pairs(article):
    doc_id, tokens = article
    for token in tokens:
        pairs.append((token, int(doc_id)))


def construct_index():
    """turn the sorted file F into an index by turning the docIDs paired with the same term into a postings list and
    setting the pointer """
    global inverted_index, counter, STOP_TIME

    for pair in pairs:
        term, doc_id = pair
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
            make_pairs(article)

    # All Files are processed
    # sort F
    pairs.sort()

    # Duplicates were already removed during the tokenization process
    # Reason: It is much faster to remove duplicates from same articles
    # than after creating pairs. [see tokenizer() for more.]

    # Construction of Inverted Index
    construct_index()
    # Write to Text File
    save(name="naive_index_unfiltered.txt", content=json.dumps(inverted_index, indent=4))
    # Write to Pickle File
    save_pickle(name="naive_index_unfiltered.pickle", content=inverted_index)


def load_naive_index():
    global inverted_index
    try:
        with open(REUTERS_OUTPUT_FOLDER + "/pickle/naive_index_unfiltered.pickle", 'rb') as handle:
            inverted_index = pickle.load(handle)
    except:
        START_TIME = timeit.default_timer()
        main()
        # Check Size
        print('Time to process', MAX_TOKEN_NUMBER, 'tokens is', round(STOP_TIME - START_TIME, 4), "Seconds")


def search(query):
    if 'and' in query or 'AND' in query:
        query_keywords = re.split("and", query, flags=re.IGNORECASE)
        return and_query(query_keywords=[s.strip() for s in query_keywords])
    elif 'or' in query or 'OR' in query:
        query_keywords = re.split("or", query, flags=re.IGNORECASE)
        return or_query(query_keywords=[s.strip() for s in query_keywords])
    else:
        return or_query(query_keywords=[query])


def and_query(query_keywords):
    results = []
    final_result = []
    for keyword in query_keywords:
        if keyword in inverted_index:
            results.append(inverted_index[keyword])
    # Take out the minimum to perform AND
    final_result = min(results, key=len)
    results.remove(final_result)
    while results:
        min_list = min(results, key=len)
        results.remove(min_list)
        final_result = list(set(final_result) & set(min_list))
    return final_result


def or_query(query_keywords):
    results = {}
    for keyword in query_keywords:
        if keyword in inverted_index:
            for doc_id in inverted_index[keyword]:
                if doc_id in results:
                    results[doc_id] = results[doc_id] + 1
                else:
                    results[doc_id] = 1
    # Merge all lists and take Union to perform OR operation
    return sorted(results.items(), key=operator.itemgetter(1), reverse=True)


if __name__ == '__main__':
    print("""
    █▀▀▄ █▀▀█ ─▀─ ▀█─█▀ █▀▀ 　 ─▀─ █▀▀▄ █▀▀▄ █▀▀ █─█ █▀▀ █▀▀█ 
    █──█ █▄▄█ ▀█▀ ─█▄█─ █▀▀ 　 ▀█▀ █──█ █──█ █▀▀ ▄▀▄ █▀▀ █▄▄▀ 
    ▀──▀ ▀──▀ ▀▀▀ ──▀── ▀▀▀ 　 ▀▀▀ ▀──▀ ▀▀▀─ ▀▀▀ ▀─▀ ▀▀▀ ▀─▀▀
    """)
    print("_____________________________________________________________")
    load_naive_index()
    number_of_terms, number_of_postings = size(inverted_index)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    print("System is Ready for querying...")
    query = input("Enter 'exit..' to stop\n> ")

    while query != 'exit..':
        result = search(query)
        if result:
            print("No. of Docs:", len(result))
            table = []
            headers = ['#', 'No. of Keywords', 'Doc ID']
            if type(result[0]) == tuple:
                for i, pair in enumerate(result):
                    table.append([i + 1, pair[1], pair[0]])
            else:
                for i, pair in enumerate(result):
                    table.append([i + 1, 1, pair])
            print(tabulate(tabular_data=table, headers=headers, tablefmt='pretty'))
        else:
            print("Sorry, No Match found... :(")
        query = input("> ")
