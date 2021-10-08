import glob, os, re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize

# Variables

sgm_count = 1
article_count = 5
REUTERS_EXT = "*.sgm"
REUTERS_FOLDER = "./reuters21578"

stop_words = []
reuters_files = []
db = dict()


def read_stop_words():
    """Read the stop words from user and store them in stop_words list"""
    input_words = input("Enter the Stop words seprated by Space:").strip().split()
    for word in input_words:
        # Convert the word in lowercase
        stop_words.append(word.lower())


def trace_files():
    """Get all files and make a list to process each files."""
    os.chdir(REUTERS_FOLDER)
    for file in glob.glob("*.sgm"):
        reuters_files.append(file)


def extract_raw_text(reuters_file, number_of_articals=None):
    """Extract the raw text of each article from the corpus"""

    new_id_pattern = "NEWID=\"([\s\S]*?)\""
    title_pattern = "<TITLE>([\s\S]*?)</TITLE>"
    body_pattern = "<BODY>([\s\S]*?)</BODY>"

    with open(reuters_file) as fp:
        file_str = fp.read()
        articals = file_str.split("</REUTERS>")

        count = 1

        for artical in articals:

            if number_of_articals is not None:
                if count > number_of_articals:
                    break

            new_id = title = body = None

            if re.search(title_pattern, artical) != None:
                new_id = re.search(new_id_pattern, artical).group(1)

            if re.search(title_pattern, artical) != None:
                title = re.search(title_pattern, artical).group(1)

            if re.search(body_pattern, artical) != None:
                body = re.search(body_pattern, artical).group(1)

            if new_id is None and title is None and body is None:
                pass  # Everything is Empty
            elif new_id is None:
                pass
            else:
                count += 1
                db[new_id] = text_cleaner(str(title) + " " + str(body))
                # print(title)
                # print(body)


def text_cleaner(string):
    string = string.replace("&lt;", "").replace(".", "")
    string = re.sub('[^a-zA-Z \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    return string


def tokenizer(text):
    tokens = word_tokenize(text)
    return tokens


def apply_porter_stemmer(tokens):
    stemmer = PorterStemmer()
    singles = [stemmer.stem(plural) for plural in tokens]
    return singles


def remove_stop_words(tokens):
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(word)
    return filtered


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def create_file(file_path, text):
    f = open(file_path, "w")
    f.write(text)
    f.close()


def save(reuters_file, id, name, content):
    create_folder("../outputs/" + reuters_file)
    create_folder("../outputs/" + reuters_file + "/" + id)
    create_file("../outputs/" + reuters_file + "/" + id + name, str(content))


def menu():
    global sgm_count, article_count
    try:
        sgm_count = int(input("How many SGM files you want to process? [1 or All]:"))
        if sgm_count <= 0 or sgm_count > 21:
            sgm_count = 1
    except:
        sgm_count = None

    try:
        article_count = int(input("How many articles from 1 SGM file you want to process? [5 or All]:"))
        if article_count <= 0 or article_count > 21:
            article_count = 5
    except:
        article_count = None
    print('Processing...')


def process(files=None, articles=None):
    global db
    file_counter = 1

    for reuters_file in reuters_files:

        # Reset DB
        db = dict()

        # Only Process 1 file
        if files is not None:
            if file_counter > sgm_count:
                break

        if articles is None:
            # Process all articles
            extract_raw_text(reuters_file)
        else:
            # Process 5 article
            extract_raw_text(reuters_file, article_count)

        for id, artical in db.items():
            # Write Article in File
            save(reuters_file, id, "/Step-1.txt", artical)

            # 2. tokenize
            tokens = tokenizer(artical)
            ## Write output to File
            save(reuters_file, id, "/Step-2.txt", tokens)

            # 3. make all text lowercase
            tokens = [token.lower() for token in tokens]
            ## Write output to File
            save(reuters_file, id, "/Step-3.txt", tokens)

            # 4. apply Porter stemmer
            new_tokens = apply_porter_stemmer(tokens=tokens)
            ## Write output to File
            save(reuters_file, id, "/Step-4.txt", new_tokens)

            # 5. given a list of stop words, remove those stop words from text.
            # Note that your code has to accept the stop word list as a parameter, do not hardcode a particular list
            filtered_tokens = remove_stop_words(new_tokens)
            ## Write output to File
            save(reuters_file, id, "/Step-5.txt", filtered_tokens)

        file_counter += 1


def main():
    # Download punkt
    nltk.download('punkt')
    # Read Stop Words
    read_stop_words()
    # Menu for choice
    menu()
    # 1. read the Reuter’s collection and extract the raw text of each article from the corpus
    ## trace all files
    trace_files()
    if sgm_count is None:
        # Process all files
        if article_count is None:
            # Process all articles
            process()
        else:
            # Process 5 articles
            process(articles=article_count)
    else:
        # Process 1 files
        if article_count is None:
            # Process all articles
            process(files=sgm_count)
        else:
            # Process 5 articles
            process(files=sgm_count, articles=article_count)

    print("Program Finished ;)")


if __name__ == '__main__':
    main()
