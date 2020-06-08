"""
Program to grab a bunch of .* files and
put them into the same directory. If 'make'
is specified, you make the directory specified
as <directory>
"""
import os
import shutil
import sys


def move_files(string, directory, make=False):
    desfiles = []
    if make is True:
        os.mkdir(directory)
    else:
        pass
    for root, dirs, files in os.walk("."):
        for file in files:
            if string in file:
                desfiles.append(os.path.join(root, file))
    for f in desfiles:
        shutil.copy(f, directory)


if __name__ == "__main__":
    move_files(sys.argv[1], sys.argv[2], sys.argv[3])
