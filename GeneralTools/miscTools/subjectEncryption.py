'''
Given a list of subject names, output an encrypted list of
hexadecimal values that correspond to each subject. The output
will be a file containing 1 subject ID per line.

For research purposes, subject IDs will be the last 10 digits
of the encrypted key, not counting the last 2 ==
'''
from cryptography.fernet import Fernet
import random
random.seed(10)


def encryptSubjects(file, output, key=False):
    '''
    Given a .txt file of subject names (1 per line),
    return subject id
    '''
    if key:
        print(key)
        key = bytes(key, 'utf-8')
    else:
        key = Fernet.generate_key()
        now = datetime.datetime.now()
        new_key = f"{now.day}-{now.month}-{now.year}.key"
        with open(new_key, 'w') as okey:
            okey.write(str(key))

    with open(file) as f:
        names = [name.strip() for name in f.readlines()]
        random.shuffle(names)

    with open(output, 'w') as out:
        for name in names:
            name = bytes(name, 'utf-8')
            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(name).decode("utf-8")
            out.write(f"{encoded_text}\n")


def decryptSubjects(file, output, inkey):
    '''
    Given a .txt file of encrypted subject ids (1 per line),
    return each subjects name
    '''
    inkey = bytes(inkey, 'utf-8')
    with open(file) as f:
        names = [name.strip() for name in f.readlines()]

    cipher_suite = Fernet(inkey)

    with open(output, 'w') as out:
        for name in names:
            name = bytes(name, 'utf-8')
            decoded_text = cipher_suite.decrypt(name).decode('utf-8')
            out.write(f"{decoded_text}\n")


if __name__ == '__main__':
    import argparse
    import datetime
    parser = argparse.ArgumentParser(description="Parser")
    # Store true flags
    parser.add_argument("-e", "--Encrypt",
                        help="If flagged, encrypt the input file",
                        required=False, action='store_true', default=False)
    parser.add_argument("-d", "--Decrypt",
                        help="If flagged, decrypt the input file",
                        required=False, action='store_true', default=False)
    # File flags
    parser.add_argument("-f", "--File",
                        help="File to encrypt or decrypt (depending on flag)",
                        required=True)
    parser.add_argument("-k", "--Key",
                        help="If encrypting/decrypting, key used to encrypt/decrypt.\
If nothing is provided, encryption will occur generating a new key.",
                        required=False, default=False)
    parser.add_argument("-o", "--Output",
                        help="Depending on whether --Encrypt or --Decrypt is \
flagged, the file containing the encrypted or decrypted values.",
                        required=False, default=50)
    argument = parser.parse_args()

    if argument.Encrypt:
        encryptSubjects(argument.File, argument.Output, argument.Key)
    elif argument.Decrypt:
        decryptSubjects(argument.File, argument.Output, argument.Key)
