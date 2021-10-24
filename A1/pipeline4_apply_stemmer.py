from nltk import PorterStemmer
from pipeline_lib import REUTERS_OUTPUT_FOLDER, load_folders, save

INPUT_FILE_NAME = "Step-3.txt"
OUTPUT_FILE_NAME = "Step-4.txt"

# Read All Folder Names
input_folders = load_folders()


def apply_porter_stemmer(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens


def main():
    for directory in input_folders:
        with open(REUTERS_OUTPUT_FOLDER + "/" + directory + "/" + INPUT_FILE_NAME) as fp:
            # Read Input File
            file_str = fp.read()
            # Split tokens and Strip for Stemming
            tokens = file_str.split(",")
            tokens = [token.strip() for token in tokens]
            # Stemmer tokens
            stemmed_tokens = apply_porter_stemmer(tokens)
            # Convert to string to writing in file
            stemmed_tokens_str = ""
            for token in stemmed_tokens:
                stemmed_tokens_str += token + ", "
            # Write to Output File
            save(directory, OUTPUT_FILE_NAME, stemmed_tokens_str.rstrip(", "))
            print(stemmed_tokens_str.rstrip(", "))

if __name__ == '__main__':
    main()
