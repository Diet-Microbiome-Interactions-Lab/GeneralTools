#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python

# print('In the module')


# def main():
#     print('Script run as __main__')


# import sys

# print(sys.path)

# if __name__ == '__main__':
#     main()
import sys


def fx(**kwargs):
    print(a, b, c)
    for arg in args:
        print(arg)
    for kwarg in kwargs:
        print(kwargs)
    return 0


mycommand = "run myprogram -f file -o output"
arguments = mycommand.split()[2:]


def parseArgs(command):
    print(command)


parseArgs(arguments)
