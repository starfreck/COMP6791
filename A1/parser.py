file_name = "reut2-000.sgm"
import re
db = []


def extract_raw_text(file_name):
    """Extract the raw text of each article from the corpus"""

    new_id_pattern = "NEWID=\"([\s\S]*?)\""
    title_pattern = "<TITLE>([\s\S]*?)</TITLE>"
    body_pattern = "<BODY>([\s\S]*?)</BODY>"

    url = "c://Users//vasur//Downloads//reuters21578//" + file_name

    with open(url) as fp:
        file_str = fp.read()
        articals = file_str.split("</REUTERS>")

        for artical in articals:

            new_id = title = body = None

            if re.search(title_pattern, artical) != None:
                new_id = re.search(new_id_pattern, artical).group(1)

            if re.search(title_pattern, artical) != None:
                title = re.search(title_pattern, artical).group(1)

            if re.search(body_pattern, artical) != None:
                body = re.search(body_pattern, artical).group(1)

            if new_id  is None and title is None and body is None:
                pass  # Everything is Empty
            else:
                db.append(text_cleaner(str(title)+" "+str(body)))
                # print(title)
                # print(body)

def text_cleaner(string: str):
    # &#3;, <, >, \n
    string = string.replace("&#3;"," ").replace("&lt;", " ").strip()\
        .replace(">"," ") \
        .replace("(", " ") \
        .replace(")", " ") \
        .replace("\n", "") \
        .replace("\"","") \
        .replace(":", " ") \
        .replace(",", " ") \
        .replace("_", " ") \
        .replace("-", " ")
    string = re.sub('[^A-Za-z]+', ' ', string)
    return string

# def extract_raw_text_old(self):
#     """Extract the raw text of each article from the corpus"""
#     with open(".\\" + self.reuters_file) as fp:
#         soup = BeautifulSoup(fp, 'html.parser')
#
#     count = 0
#     for artical in soup.find_all('reuters'):
#         if count == 5:
#             break
#         new_id = artical.get('newid')
#         body = artical.find("body")
#         body = str(body).replace("<body>", "").replace("</body>", "").strip()
#         if body != 'None':
#             self.db[new_id] = body.lower().replace("\\", "").replace("\n", "")
#             count += 1

if __name__ == '__main__':
    extract_raw_text(file_name)
    print(db)
