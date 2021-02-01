#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python

# print('In the module')


# def main():
#     print('Script run as __main__')


# import sys

# print(sys.path)

# if __name__ == '__main__':
#     main()


a = ['--help', '-h', '-H']
b = ['example', 'dane']

if any(x in a for x in b):
    print(a)
