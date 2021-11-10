import json
import math
import os
import re
import glob
import timeit

from lib import save, save_pickle, size
from nltk import word_tokenize

tfDict = {}
corpus = {}
bag_of_words_in_corpus = {}
unique_words = set()
num_of_words_in_docs = {}
inverted_index = {}
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
                yield new_id, str(title) + " " + str(body)


def text_cleaner(string):
    string = string.replace("&lt;", "").replace(".", "")
    string = re.sub('[^a-zA-Z0-9 \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    string = string.lower()
    return string


def tokenizer(text):
    return word_tokenize(text_cleaner(text))


def compute_tf(word_dict, bag_of_words):
    tf = {}
    bag_of_words_count = len(bag_of_words)
    for word, count in word_dict.items():
        tf[word] = count / float(bag_of_words_count)
    return tf


def get_unique_words():
    global unique_words
    for new_id, document in corpus.items():
        bag_of_words_in_corpus[new_id] = tokenizer(document)
        unique_words = unique_words.union(set(bag_of_words_in_corpus[new_id]))
        unique_words.discard('')


def generate_dictionary_of_words():
    for new_id, bag_of_words in bag_of_words_in_corpus.items():
        num_of_words = dict.fromkeys(unique_words, 0)
        for word in bag_of_words:
            try:
                num_of_words[word] += 1
            except:
                print(word, "is not in unique_words")
        num_of_words_in_docs[new_id] = num_of_words


def main():
    global inverted_index, pairs
    # Read All Reuters File Names
    trace_files()

    # Process All files one by one
    for reuters_file in reuters_files:
        # Parse Article in 1 file
        articles = parser(reuters_file)

        for new_id, article in articles:
            # Process Each Article One by One
            corpus[new_id] = article

    get_unique_words()
    generate_dictionary_of_words()
    # compute the term frequency for each of documents
    for new_id, num_of_words in num_of_words_in_docs.items():
        tfDict[new_id] = compute_tf(num_of_words, bag_of_words_in_corpus[new_id])

    print(tfDict)
    # Construction of Inverted Index
    # Write to Text File
    # save(name="inverted_index_BM25.txt", content=json.dumps(inverted_index, indent=4))
    # Write to Pickle File
    # save_pickle(name="inverted_index_BM25.pickle", content=inverted_index)


if __name__ == '__main__':
    START_TIME = timeit.default_timer()
    main()
    # Check Size
    number_of_terms, number_of_postings = size(inverted_index)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
