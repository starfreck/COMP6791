import pickle
from lib import REUTERS_OUTPUT_FOLDER, measured_run

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


def query_processor(query, choice):
    # Convert to lower case if it's not for unfiltered or no numbers
    if not (choice == "inverted_index_unfiltered" or choice == "inverted_index_no_numbers"):
        query = query.lower()
    # We have to use Stammer on query
    if choice == "inverted_index_stemming":
        from nltk.stem.porter import PorterStemmer
        stemmer = PorterStemmer()
        query = stemmer.stem(query)

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
        elif option == "6":
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
        query_processor(query,choice)
        query = input("> ")


if __name__ == '__main__':
    measured_run(function=main,name="Main")
