import pickle
import timeit
from lib import REUTERS_OUTPUT_FOLDER

inverted_index = {}


def load_inverted_index(choice):
    global inverted_index
    try:
        with open(REUTERS_OUTPUT_FOLDER + "/pickle/" + choice + '.pickle', 'rb') as handle:
            inverted_index = pickle.load(handle)
    except:
        print("Pickle file not found...")
        print("Please run the subproject_1_naive_indexer.py first")
        print("And re-run the subproject_2_query_processor.py")
        exit(0)


def query_processor(query):
    if query in inverted_index:
        print("No. of Docs:", len(inverted_index[query]))
        print("Doc IDs:", inverted_index[query])
    else:
        print("Sorry, No match found! :(")


def menu():
    print("1. unfiltered")
    print("2. no numbers")
    print("3. case folding")
    print("4. 30 stop words")
    print("5. 150 stop words")
    print("6. stemming")
    return input("Select Inverted index:")


def select_choice():
    choice = ""
    while True:
        option = menu()
        if option == "1":
            return "inverted_index_unfiltered"
        elif option == "2":
            return "inverted_index_no_numbers"
        elif option == "3":
            return "inverted_index_case_folding"
        elif option == "4":
            return "inverted_index_30_stop_words"
        elif option == "5":
            return "inverted_index_150_stop_words"
        elif option == "5":
            return "inverted_index_stemming"
        else:
            print("Invalid choice! Please try again!")
            continue


def main():
    print("--------Welcome--------")
    choice = select_choice()
    load_inverted_index(choice)
    query = input("Enter 'exit..' to stop\n> ")
    while query != 'exit..':
        query_processor(query)
        query = input("> ")


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Run Time: ', stop - start)
