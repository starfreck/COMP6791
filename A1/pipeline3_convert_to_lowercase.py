from pipeline_lib import REUTERS_OUTPUT_FOLDER, load_folders, save

INPUT_FILE_NAME = "Step-2.txt"
OUTPUT_FILE_NAME = "Step-3.txt"

# Read All Folder Names
input_folders = load_folders()


def main():
    for directory in input_folders:
        with open(REUTERS_OUTPUT_FOLDER + "/" + directory + "/" + INPUT_FILE_NAME) as fp:
            # Read Input File
            file_str = fp.read()
            # Make all text lowercase
            lower_tokens = file_str.lower()
            # Split tokens and Strip for Stemming
            tokens = lower_tokens.split(",")
            tokens = [token.strip() for token in tokens]
            # Store tokens in set() to make then unique
            tokens = set(tokens)
            tokens = list(tokens)
            # Convert to string to writing in file
            lower_tokens_str = ""
            for token in tokens:
                lower_tokens_str += token + ", "
            # Write to Output File
            save(directory, OUTPUT_FILE_NAME, lower_tokens_str.rstrip(", "))
            print(lower_tokens_str.rstrip(", "))

if __name__ == '__main__':
    main()
