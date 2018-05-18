# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
import sys
from os import path
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import random, get_random_bytes
from argparse import ArgumentParser, FileType


def get_arguments():
    parser = ArgumentParser(
        prog="scriptify.py",
        description="Turn any file into a runnable python script",
        usage=("scriptify.py [-h] [--help]\n       "
               "scriptify.py 'source file' 'output file' [-m] [-b] [-c [pass]] [-s msg]"),
        epilog="If encryption is used and no password is set, a random key will be provided.")

    parser.add_argument('in_file',
                        metavar='source file',
                        # type=FileType('rb'),
                        help="input file to convert")

    parser.add_argument('out_file',
                        metavar='output file',
                        # type=FileType('wb'),
                        help="name/path for the output script")

    parser.add_argument('-m', '--minimal', action='store_true',
                        help="use a minimal/obfuscated recovery script")

    parser.add_argument('-b', '--base64', action='store_true',
                        help="encode data with base64")

    parser.add_argument('-c', '--crypted', metavar='*** ', dest='password',
                        nargs="?", default='', help="encrypt data with AES")

    parser.add_argument('-s', '--say', metavar='... ', dest='message',
                        help='print a message when the script is run')

    return parser.parse_args()


def print_welcome(args):
    print(f" - - Scriptify - - ")
    print(f"Source: {args.in_file}")
    print(f"Output: {args.out_file}\n")

    if args.minimal:
        print("- Minimal script")
    if args.base64:
        print("- Base64 encoding")
    if args.crypted and not args.password:
        print("- AES encryption (no password)")
    elif args.crypted and args.password:
        print("- AES encryption  -> " + args.password)
    if args.message:
        print("- Message display -> " + args.message)

    if input("\nDo you want to continue ? [Y/n] ") in {"n", "N"}:
        print("Cancelling.")
        exit()


def file_to_buffer(file_obj):
    with file_obj as source_file:
        binary_content = source_file.read()

    return binary_content


if __name__ == '__main__':
    args = get_arguments()
    in_file, out_file = args.in_file, args.out_file
    print_welcome(args)

    print(" * Reading source file... ")
    raw_buffer = file_to_buffer(in_file)

    if args.base64:
        print("* Encoding in Base64...")
        encoded_buffer = b64encode(raw_buffer)
    else:
        encoded_buffer = raw_buffer

    if args.password == None:
        file_buffer = encoded_buffer
    elif args.password == '':
        password = "".join(random.sample(string.hexdigits, 12))
        hasher = SHA3_256.new(password.encode('utf-8'))
        key = hasher.digest()

        aes_cipher = AES.new(key, AES.MODE_EAX)
        file_buffer = aes_cipher.encrypt(encoded_buffer)
    else:
        hasher = SHA3_256.new(args.password.encode('utf-8'))
        key = hasher.digest()

        aes_cipher = AES.new(key, AES.MODE_EAX)
        file_buffer = aes_cipher.encrypt(encoded_buffer)

    hex_string = repr(file_buffer)

    print("* Loading template... ", end='')
    with open_file("container.template.py", 'r') as template:
        script = template.read()
    print("OK.")

    print("* Creating script... ", end='')
    with open_file(dst_abspath, 'w') as output:
        filled = script.replace("$$BIN_DATA$$", hex_string)
        filled = filled.replace("$$ORIG_FILENAME$$", src_name)
        # COMBAK: here
        output.write(filled)
    print("OK.")
