# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
import base64 as base64enc
from os import path
from argparse import ArgumentParser, FileType


def get_arguments():
    parser = ArgumentParser(
        prog="scriptify.py",
        description="Turn any file into a runnable python script",
        usage=("scriptify.py [-h] [--help]\n       "
               "scriptify.py 'source file' 'output file' [-m] [-b | -c [-p pass]] [-s msg]"),
        epilog="If encryption is used and no password is set, the key will be stored in the script!")

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

    encryption = parser.add_mutually_exclusive_group()
    encryption.add_argument('-b', '--base64', action='store_true',
                            help="encode data with base64")

    encryption.add_argument('-c', '--crypted', action='store_true',
                            help="encrypt data with AES")

    parser.add_argument('-p', '--pass', metavar='*** ', dest='password',
                        help="password to use with AES encryption")

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


def file_to_string(file_obj):
    print("* Reading source file... ", end='')
    with file_obj as source_file:
        binary_content = source_file.read()

    hex_string = repr(binary_content)
    print("OK.")
    return hex_string


def file_to_buffer(file_obj):
    print("* Reading source file... ", end='')
    with file_obj as source_file:
        binary_content = source_file.read()

    print("OK.")
    return binary_content


if __name__ == '__main__':
    args = get_arguments()
    print_welcome(args)

    in_file, out_file = args.in_file, args.out_file
    raw_buffer = file_to_buffer(in_file)

    if args.base64:
        print("* Encoding in Base64...", end='')
        file_buffer = base64enc.b64encode(raw_buffer)
        print("OK.")

    elif args.crypted:
        # TODO: ...
        pass

    else:
        file_buffer = raw_buffer

    hex_string = repr(file_buffer)
