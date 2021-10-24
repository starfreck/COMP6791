import json
import os
import re
import glob
import timeit

from lib import save, save_pickle
from nltk import word_tokenize

inverted_index = {}
pairs = []
reuters_files = []
REUTERS_FOLDER = "./reuters21578"

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
    tokens = set(tokens)  # Using set() here to remove duplicate tokens
    tokens = list(tokens)  # Using list() here to convert unique tokens to list
    return tokens


def make_pairs(article):
    doc_id = article[0]
    tokens = article[1]
    for token in tokens:
        pairs.append([token, int(doc_id)])


def construct_index():
    """turn the sorted file F into an index by turning the docIDs paired with the same term into a postings list and
    setting the pointer """
    global inverted_index

    while pairs:
        term, doc_id = pairs.pop(0)
        if term not in inverted_index:
            inverted_index[term] = [doc_id]
        else:
            if doc_id not in inverted_index[term]:
                inverted_index[term].append(doc_id)
                inverted_index[term].sort()


def main():
    global inverted_index
    # Read All Reuters File Names
    trace_files()

    # Process All files one by one
    for reuters_file in reuters_files:
        # Parse Article in 1 file
        articles = parser(reuters_file)
        for article in articles:
            # Process Each Article One by One
            make_pairs(article)
            # sort F
            pairs.sort()
            # Duplicates were already removed during the tokenization process
            # Construction of Inverted Index
            construct_index()

    # All Files are processed
    # Write to Text File
    save(name="inverted_index_unfiltered.txt", content=json.dumps(inverted_index, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_unfiltered.pickle", content=inverted_index)


def size():
    global number_of_terms, number_of_postings
    number_of_terms = len(inverted_index)
    for k, v in inverted_index.items():
        number_of_postings += len(v)


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Run Time: ', stop - start, "Seconds")
    # Check Size
    size()
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
