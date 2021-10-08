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
            # Write to Output File
            save(directory, OUTPUT_FILE_NAME, lower_tokens)


if __name__ == '__main__':
    main()