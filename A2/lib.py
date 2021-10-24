import os
import pickle
import shutil

REUTERS_OUTPUT_FOLDER = "outputs"


def create_folder(path):
    """Create folder at given path if it's not exist"""
    if not os.path.isdir(path):
        os.makedirs(path)


def write_to_file(file_path, text, mode="w"):
    """Create file at given path if it's not exist"""
    with open(file_path, mode) as file:
        file.write(text)


def write_to_pickle_file(file_path, content, mode="wb"):
    with open(file_path, mode) as handle:
        pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save(name, content, mode="w"):
    create_folder(REUTERS_OUTPUT_FOLDER + "/text")
    write_to_file(REUTERS_OUTPUT_FOLDER + "/text/" + name, content, mode)


def save_pickle(name, content, mode="wb"):
    create_folder(REUTERS_OUTPUT_FOLDER + "/pickle")
    write_to_pickle_file(REUTERS_OUTPUT_FOLDER + "/pickle/" + name, content, mode)


def remove_old_outputs():
    try:
        shutil.rmtree(REUTERS_OUTPUT_FOLDER)
    except:
        pass
