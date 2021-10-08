from pipeline_lib import REUTERS_OUTPUT_FOLDER, load_folders, save

INPUT_FILE_NAME = "Step-4.txt"
OUTPUT_FILE_NAME = "Step-5.txt"

stop_words = []
# Read All Folder Names
input_folders = load_folders()


def read_stop_words():
    """Read the stop words from user and store them in stop_words list"""
    input_words = input("Enter the Stop words seprated by Space:").strip().split()
    for word in input_words:
        # Convert the word in lowercase
        stop_words.append(word.lower())


def remove_stop_words(tokens):
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(word)
    return filtered


def main():
    for directory in input_folders:
        with open(REUTERS_OUTPUT_FOLDER + "/" + directory + "/" + INPUT_FILE_NAME) as fp:
            # Read Input File
            file_str = fp.read()
            # Convert to list
            tokens = file_str.split(",")
            tokens = [token.strip() for token in tokens]
            # Remove Stop Words from tokens
            filtered_tokens = remove_stop_words(tokens)
            # Convert to string to writing in file
            filtered_tokens_str = ""
            for token in filtered_tokens:
                filtered_tokens_str += token + ", "
            # Write to Output File
            save(directory, OUTPUT_FILE_NAME, filtered_tokens_str.rstrip(", "))


if __name__ == '__main__':
    read_stop_words()
    main()
