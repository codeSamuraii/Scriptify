# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
from os import path
from argparse import ArgumentParser, FileType


def get_arguments():
    arg_parser = ArgumentParser(
        description="Turn any file into a python script",
        usage="scriptify.py [-h] [--help]\n       scriptify.py \'source file\' \'output file\' [-m] [-b | -c [-p pass]] [-s msg]")

    encryption = arg_parser.add_mutually_exclusive_group()
    arg_parser.add_argument('in_file',
                            metavar='source file',
                            #type=FileType('rb'),
                            help="input file to convert")
    arg_parser.add_argument('out_file',
                            metavar='output file',
                            #type=FileType('wb'),
                            help="name/path for the output script")

    arg_parser.add_argument('-m', '--minimal', action='store_true',
                            help="use a minimal/obfuscated recovery script")
    encryption.add_argument('-b', '--base64', action='store_true',
                            help="encode data with base64 - incompatible with encryption or password")
    encryption.add_argument('-c', '--crypted', action='store_true',
                            help="encrypt data with AES")
    arg_parser.add_argument('-p', '--password', metavar='... ', dest='password',
                            help="password to use with AES encryption  - if no password is set, the key will be stored in the script")
    arg_parser.add_argument('-s', '--say', metavar='... ', dest='message',
                            help='print a message when the script is run')
    return arg_parser.parse_args()

if __name__ == '__main__':
    args = get_arguments()
    print(args)
