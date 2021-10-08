import os
import shutil

REUTERS_OUTPUT_FOLDER = "outputs"


def load_folders():
    input_folders = []
    for root, dirs, files in os.walk(REUTERS_OUTPUT_FOLDER, topdown=False):
        for name in dirs:
            input_folders.append(os.path.join(name))
    return input_folders


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def create_file(file_path, text):
    f = open(file_path, "w")
    f.write(text)
    f.close()


def save(id, name, content):
    create_folder(REUTERS_OUTPUT_FOLDER + "/" + id)
    create_file(REUTERS_OUTPUT_FOLDER + "/" + id + "/" + name, str(content))


def remove_old_outputs():
    try:
        shutil.rmtree(REUTERS_OUTPUT_FOLDER)
    except:
        pass
