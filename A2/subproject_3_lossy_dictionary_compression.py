import json
import pickle
from nltk.stem.porter import PorterStemmer
from tabulate import tabulate
from nltk.corpus import stopwords as stw

from lib import REUTERS_OUTPUT_FOLDER, measured_run, save, save_pickle, size

inverted_index = {}
inverted_index_no_numbers = {}
inverted_index_case_folding = {}
inverted_index_30_stop_words = {}
inverted_index_150_stop_words = {}
inverted_index_stemming = {}

stopwords = stw.words('english')
data = {'unfiltered': [67961, 1775388]}


def load_inverted_index():
    global inverted_index
    try:
        with open(REUTERS_OUTPUT_FOLDER + "/pickle/inverted_index_unfiltered.pickle", 'rb') as handle:
            inverted_index = pickle.load(handle)
    except:
        print("Pickle file not found...")
        print("Please run the subproject_1_naive_indexer.py first")
        print("And re-run the subproject_3_lossy_dictionary_compression.py")
        exit(0)


def remove_numbers():
    for k, v in inverted_index.items():
        if not k.isnumeric():
            inverted_index_no_numbers[k] = v
    # Write to Text File
    save(name="inverted_index_no_numbers.txt", content=json.dumps(inverted_index_no_numbers, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_no_numbers.pickle", content=inverted_index_no_numbers)
    number_of_terms, number_of_postings = size(inverted_index_no_numbers)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    data['no_numbers'] = [number_of_terms, number_of_postings]


def remove_case_folding():
    for k, v in inverted_index_no_numbers.items():
        key = k.lower()
        if key in inverted_index_case_folding:
            inverted_index_case_folding[key] += v
            inverted_index_case_folding[key] = list(set(inverted_index_case_folding[key]))
            inverted_index_case_folding[key].sort()
        else:
            inverted_index_case_folding[key] = v

    # Write to Text File
    save(name="inverted_index_case_folding.txt", content=json.dumps(inverted_index_case_folding, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_case_folding.pickle", content=inverted_index_case_folding)
    number_of_terms, number_of_postings = size(inverted_index_case_folding)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    data['case_folding'] = [number_of_terms, number_of_postings]


def remove_30_stop_words():
    stop_words_30 = stopwords[:30]

    for k, v in inverted_index_case_folding.items():
        if k not in stop_words_30:
            inverted_index_30_stop_words[k] = v

    # Write to Text File
    save(name="inverted_index_30_stop_words.txt", content=json.dumps(inverted_index_30_stop_words, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_30_stop_words.pickle", content=inverted_index_30_stop_words)
    number_of_terms, number_of_postings = size(inverted_index_30_stop_words)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    data['30_stop_words'] = [number_of_terms, number_of_postings]


def remove_150_stop_words():
    stop_words_150 = stopwords[:150]

    for k, v in inverted_index_case_folding.items():
        if k not in stop_words_150:
            inverted_index_150_stop_words[k] = v

    # Write to Text File
    save(name="inverted_index_150_stop_words.txt", content=json.dumps(inverted_index_150_stop_words, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_150_stop_words.pickle", content=inverted_index_150_stop_words)
    number_of_terms, number_of_postings = size(inverted_index_150_stop_words)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    data['150_stop_words'] = [number_of_terms, number_of_postings]


def remove_stemmed_words():
    stemmer = PorterStemmer()
    for k, v in inverted_index_150_stop_words.items():
        # Stem Key
        key = stemmer.stem(k)
        if key in inverted_index_stemming:
            inverted_index_stemming[key] += v
            inverted_index_stemming[key] = list(set(inverted_index_stemming[key]))
            inverted_index_stemming[key].sort()
        else:
            inverted_index_stemming[key] = v

    # Write to Text File
    save(name="inverted_index_stemming.txt", content=json.dumps(inverted_index_stemming, indent=4))
    # Write to Pickle File
    save_pickle(name="inverted_index_stemming.pickle", content=inverted_index_stemming)
    number_of_terms, number_of_postings = size(inverted_index_stemming)
    print('Number of Terms: ', number_of_terms)
    print('Number of Postings: ', number_of_postings)
    data['stemming'] = [number_of_terms, number_of_postings]


def table():
    # unfiltered
    t_d0 = ""
    t_t0 = ""
    p_d0 = ""
    p_t0 = ""
    # no numbers
    t_d1 = delta(data['no_numbers'][0], data['unfiltered'][0])
    t_t1 = delta(data['no_numbers'][0], data['unfiltered'][0])
    p_d1 = delta(data['no_numbers'][1], data['unfiltered'][1])
    p_t1 = delta(data['no_numbers'][1], data['unfiltered'][1])
    # case folding
    t_d2 = delta(data['case_folding'][0], data['no_numbers'][0])
    t_t2 = delta(data['case_folding'][0], data['unfiltered'][0])
    p_d2 = delta(data['case_folding'][1], data['no_numbers'][1])
    p_t2 = delta(data['case_folding'][1], data['unfiltered'][1])
    # 30 stop words
    t_d3 = -0
    t_t3 = delta(data['30_stop_words'][0], data['unfiltered'][0])
    p_d3 = delta(data['30_stop_words'][1], data['case_folding'][1])
    p_t3 = delta(data['30_stop_words'][1], data['unfiltered'][1])

    # 150 stop words
    t_d4 = -0
    t_t4 = delta(data['150_stop_words'][0], data['unfiltered'][0])
    p_d4 = delta(data['150_stop_words'][1], data['case_folding'][1])
    p_t4 = delta(data['150_stop_words'][1], data['unfiltered'][1])

    # stemming
    t_d5 = delta(data['stemming'][0], data['150_stop_words'][0])
    t_t5 = delta(data['stemming'][0], data['unfiltered'][0])
    p_d5 = delta(data['stemming'][1], data['150_stop_words'][1])
    p_t5 = delta(data['stemming'][1], data['unfiltered'][1])

    headers = ["", "number of terms", "D%", "T%",
               "number of nonpositional postings", "D%", "T%"]
    table = [
        ["unfiltered",
         data['unfiltered'][0], t_d0, t_t0,
         data['unfiltered'][1], p_d0, p_t0
         ],
        ["no numbers",
         data['no_numbers'][0], t_d1, t_t1,
         data['no_numbers'][1], p_d1, p_t1
         ],
        ["case folding",
         data['case_folding'][0], t_d2, t_t2,
         data['case_folding'][1], p_d2, p_t2
         ],
        ["30 stop words",
         data['30_stop_words'][0], t_d3, t_t3,
         data['30_stop_words'][1], p_d3, p_t3
         ],
        ["150 stop words",
         data['150_stop_words'][0], t_d4, t_t4,
         data['150_stop_words'][1], p_d4, p_t4
         ],
        ["stemming",
         data['stemming'][0], t_d5, t_t5,
         data['stemming'][1], p_d5, p_t5
         ]
    ]
    print(tabulate(table, headers, tablefmt="psql"))


def delta(v1, v2):
    return int(((v1 - v2) / v2) * 100)


def main():
    load_inverted_index()
    measured_run(function=remove_numbers, name="remove_numbers")
    measured_run(function=remove_case_folding, name="remove_case_folding")
    measured_run(function=remove_30_stop_words, name="remove_30_stop_words")
    measured_run(function=remove_150_stop_words, name="remove_150_stop_words")
    measured_run(function=remove_stemmed_words, name="remove_stemmed_words")
    table()


if __name__ == '__main__':
    main()
