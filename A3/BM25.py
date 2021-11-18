import math
import re
import os
import glob
from nltk import word_tokenize
from nltk.corpus import stopwords
import operator


class BM25:
    _REUTERS_FOLDER = "./reuters21578"

    def __init__(self, no_of_docs=21578, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.N = no_of_docs

        self._counter = 0
        self._avg_doc_length = 0

        self._tf = {}
        self._df = {}
        self._idf = {}
        self._corpus = {}
        self._original_corpus = {}
        self._doc_len = {}
        self._word_count_dict = {}

        self._reuters_files = []

        # load router's files
        self._trace_files()

    def _trace_files(self):
        """Get all files and make a list to process each files."""
        os.chdir(self._REUTERS_FOLDER)
        for file in glob.glob("*.sgm"):
            self._reuters_files.append(self._REUTERS_FOLDER + "/" + file)
        os.chdir("..")

    @staticmethod
    def text_cleaner(string):
        string = string.replace("&lt;", "").replace(".", "")
        string = re.sub('[^a-zA-Z0-9 .]', ' ', string)
        string = re.sub(' +', ' ', string)
        return string.lower()

    @staticmethod
    def tokenizer(text):
        # Clean the text and tokenize it
        tokens = word_tokenize(BM25.text_cleaner(text))
        # Remove stopwords
        tokens = [token for token in tokens if token not in stopwords.words('english')]
        return tokens

    def parser_collection(self):
        for reuters_file in self._reuters_files:
            self._parser(reuters_file)

        # build a word count dictionary
        for new_id, tokens in self._corpus.items():
            for token in tokens:
                self._word_count_dict[token] = self._word_count_dict.get(token, 0) + 1
        # remove words that appear only once
        for new_id, tokens in self._corpus.items():
            self._corpus[new_id] = [token for token in tokens if self._word_count_dict[token] > 1]

        # Start the process
        for new_id, doc in self._corpus.items():

            self._doc_len[new_id] = len(doc)

            # calculate term frequency per document
            frequencies = {}
            for term in doc:
                term_count = frequencies.get(term, 0) + 1
                frequencies[term] = term_count

            self._tf[new_id] = frequencies

            # calculate document frequency per term
            for term, _ in frequencies.items():
                df_count = self._df.get(term, 0) + 1
                self._df[term] = df_count



        for term, freq in self._df.items():
            self._idf[term] = math.log(1 + (self.N - freq + 0.5) / (freq + 0.5))

        # Calculate the Average document length
        self._avg_doc_length = sum(self._doc_len.values()) / self.N

    def _parser(self, reuters_file):
        """Extract the raw text of each article from the corpus"""

        new_id_pattern = "NEWID=\"([\s\S]*?)\""
        title_pattern = "<TITLE>([\s\S]*?)</TITLE>"
        body_pattern = "<BODY>([\s\S]*?)</BODY>"

        with open(reuters_file) as fp:
            file_str = fp.read()
            articles = file_str.split("</REUTERS>")

            for article in articles:

                if self._counter >= self.N:
                    break

                new_id = title = body = None

                if re.search(title_pattern, article) is not None:
                    new_id = re.search(new_id_pattern, article).group(1)

                if re.search(title_pattern, article) is not None:
                    title = re.search(title_pattern, article).group(1)

                if re.search(body_pattern, article) is not None:
                    body = re.search(body_pattern, article).group(1)

                if new_id is None:
                    pass  # If can't fine ID then skip article
                else:
                    # Process the Article
                    self._original_corpus[new_id] = [str(title), str(body)]
                    self._corpus[new_id] = BM25.tokenizer(str(title) + " " + str(body))

                # Increment the counter
                self._counter += 1

    def search(self, query):
        query = [keyword for keyword in query.lower().split() if keyword not in stopwords.words('english')]

        result = {}
        for new_id in self._corpus.keys():
            score = self._ranking_score(query, new_id)
            if score > 0:
                result[int(new_id)] = score
        # Sort according to Ranking Score
        return sorted(result.items(), key=operator.itemgetter(1), reverse=True)

    def _ranking_score(self, query, new_id):
        score = 0.0
        doc_len = self._doc_len[new_id]
        frequencies = self._tf[new_id]
        for term in query:
            if term not in frequencies:
                continue
            freq = frequencies[term]
            numerator = self._idf[term] * freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self._avg_doc_length)
            score += (numerator / denominator)
        return score

    def get_document_title(self, new_id=None):
        if new_id is not None:
            if 1 <= new_id <= 21578:
                return self._original_corpus[str(new_id)][0]
        return "Invalid NEWID !"

    def get_document_body(self, new_id=None):
        if new_id is not None:
            if 1 <= new_id <= 21578:
                return self._original_corpus[str(new_id)][1]
        return "Invalid NEWID !"
