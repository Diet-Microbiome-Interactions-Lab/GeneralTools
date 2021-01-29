"""
Program to recursively grab a bunch of .* files (specified via argument 1)
and put them into the same directory. If 'make' is specified, you make the
directory specified as <directory>
"""
import os
import shutil
import sys


def move_files(string, directory):
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)
    for root, dirs, files in os.walk("."):
        for file in files:
            if string in file:
                movefile = os.path.join(root, file)
                shutil.copy(movefile, directory)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-s", "--String",help="String to match",
                        required=True)
    parser.add_argument("-d", "--Directory",
                        help="Directory to move the file to",
                        required=True)
    argument = parser.parse_args()
    move_files(sys.argv[1], sys.argv[2])
