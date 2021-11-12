from BM25 import BM25
import _pickle as pickle
from tabulate import tabulate
from lib import REUTERS_OUTPUT_FOLDER, save_pickle, measured_run


def main():
    N = None
    try:
        N = int(input("How many documents you want to index? (N):"))
    except:
        print("Indexing all documents...")

    # Create Object of BM25
    if N is not None:
        okapi_bm25 = BM25(N)
    else:
        okapi_bm25 = load_okapi_bm25_21578()

    okapi_bm25.parser_collection()

    print("System is Ready for querying...")
    query = input("Enter 'exit..' to stop\n> ")

    while query != 'exit..':
        result = okapi_bm25.search(query)
        if result:
            print("No. of Docs:", len(result))
            table = []
            headers = ['Doc ID', 'Rank Score']
            for k, v in result.items():
                table.append([v, round(k, 6)])
            print(tabulate(tabular_data=table, headers=headers, tablefmt='pretty'))
        else:
            print("Sorry, No Match found... :(")
        query = input("> ")


def load_okapi_bm25_21578():
    try:
        with open(REUTERS_OUTPUT_FOLDER + "/pickle/okapi_bm25_21578.pickle", 'rb') as handle:
            okapi_bm25_21578 = pickle.load(handle)
    except:
        okapi_bm25_21578 = BM25()
        save_pickle(name="okapi_bm25_21578.pickle", content=okapi_bm25_21578)
    return okapi_bm25_21578



if __name__ == '__main__':
    main()
