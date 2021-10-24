import os
import re
import glob
from pipeline_lib import save, remove_old_outputs

ARTICLE_COUNT = 5

REUTERS_FOLDER = "./reuters21578"
OUTPUT_FILE_NAME = "Step-1.txt"

reuters_files = []


def trace_files():
    """Get all files and make a list to process each files."""
    os.chdir(REUTERS_FOLDER)
    for file in glob.glob("*.sgm"):
        reuters_files.append(REUTERS_FOLDER + "/" + file)
    os.chdir("..")


def main(reuters_file, number_of_articles=None):
    """Extract the raw text of each article from the corpus"""

    new_id_pattern = "NEWID=\"([\s\S]*?)\""
    title_pattern = "<TITLE>([\s\S]*?)</TITLE>"
    body_pattern = "<BODY>([\s\S]*?)</BODY>"

    with open(reuters_file) as fp:
        file_str = fp.read()
        articles = file_str.split("</REUTERS>")

        count = 1

        for article in articles:

            if number_of_articles is not None:
                if count > number_of_articles:
                    break

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
                count += 1
                # Write Article to File
                save(new_id, OUTPUT_FILE_NAME, str(title) + " " + str(body))
                print(str(title) + " " + str(body))


"""
       NOTE: If you want to process all Reuters Files then
       loop over the reuters_files one by one and pass the
       each file in main() (i.e. main(reuters_file,ARTICLE_COUNT)).

       If you want to change the number of articles to process
       in one file then update "ARTICLE_COUNT" on top of the
       file. If you want to process all articles in file then 
       call main() with only one argument (i.e. main(reuters_file)).

   """
if __name__ == '__main__':
    # Remove Old Output Files
    remove_old_outputs()
    # Read All Reuters File Names
    trace_files()
    # Get 1st File Only
    file_name = reuters_files[0]

    # Process One file
    # main(file_name, ARTICLE_COUNT)

    # Process All files
    for reuters_file in reuters_files:
        main(reuters_file)
