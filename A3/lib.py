import os
import _pickle as pickle
import timeit

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
        pickle.dump(content, handle)


def save(name, content, mode="w"):
    create_folder(REUTERS_OUTPUT_FOLDER + "/text")
    write_to_file(REUTERS_OUTPUT_FOLDER + "/text/" + name, content, mode)


def save_pickle(name, content, mode="wb"):
    create_folder(REUTERS_OUTPUT_FOLDER + "/pickle")
    write_to_pickle_file(REUTERS_OUTPUT_FOLDER + "/pickle/" + name, content, mode)


def measured_run(function, name):
    print("Running", name + "() --->")
    start = timeit.default_timer()
    return_val = function()
    stop = timeit.default_timer()
    print('Run Time of ' + name + '(): ', stop - start, "Seconds")
    print("----------------------------------------------------------------")
    return return_val


def size(dictionary):
    number_of_postings = 0
    number_of_terms = len(dictionary)
    for k, v in dictionary.items():
        number_of_postings += len(v)
    return number_of_terms, number_of_postings
