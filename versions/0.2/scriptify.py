# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
from os import path
from argparse import ArgumentParser, FileType


def get_arguments():
    parser = ArgumentParser(
        prog="scriptify.py",
        description="Turn any file into a runnable python script",
        usage=("scriptify.py [-h] [--help]\n       "
               "scriptify.py 'source file' 'output file' [-m] [-b] [-c [-p pass]] [-s msg]"),
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

    parser.add_argument('-b', '--base64', action='store_true',
                        help="encode data with base64")

    parser.add_argument('-c', '--crypted', action='store_true',
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


if __name__ == '__main__':
    args = get_arguments()
    print_welcome(args)
