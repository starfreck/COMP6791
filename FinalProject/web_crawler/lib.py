import os
import shutil


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def create_file(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            pass  # file already exists.
    else:
        # print("created file : ", path)
        f = open(path, "w")
        f.write("[]")
        f.close()


def remove_old_outputs():
    try:
        shutil.rmtree("Outputs")
    except:
        pass