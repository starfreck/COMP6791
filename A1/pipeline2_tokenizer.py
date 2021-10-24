import re
from nltk import word_tokenize
from pipeline_lib import REUTERS_OUTPUT_FOLDER, load_folders, save

INPUT_FILE_NAME = "Step-1.txt"
OUTPUT_FILE_NAME = "Step-2.txt"

# Read All Folder Names
input_folders = load_folders()


def text_cleaner(string):
    string = string.replace("&lt;", "").replace(".", "")
    string = re.sub('[^a-zA-Z \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    return string

def tokenizer(text):
    tokens = word_tokenize(text_cleaner(text))
    tokens = set(tokens)  # Using set() here to remove duplicate tokens
    tokens = list(tokens)  # Using list() here to convert unique tokens to list
    return tokens


def main():
    for directory in input_folders:
        with open(REUTERS_OUTPUT_FOLDER + "/" + directory + "/" + INPUT_FILE_NAME) as fp:
            # Read Input File
            file_str = fp.read()
            # Clean all files and generate tokens' list
            tokens = tokenizer(file_str)
            # Convert to string to writing in file
            tokens_str = ""
            for token in tokens:
                tokens_str += token + ", "
            # Write to Output File
            save(directory, OUTPUT_FILE_NAME, tokens_str.rstrip(", "))
            print(tokens_str.rstrip(", "))


if __name__ == '__main__':
    main()
