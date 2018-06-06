# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
import os
import sys
from argparse import ArgumentParser, FileType
from base64 import b64encode
from lzma import compress
from os import path, system
from string import Template

from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes, random


def get_arguments():
    parser = ArgumentParser(
        prog="scriptify.py",
        description="Turn any file into a runnable python script",
        usage=("scriptify.py [-h] [--help]\n       "
               "scriptify.py 'source file' 'output file' [-b] [-c[c]] [-p [pass]] [-s msg]"),
        epilog="If encryption is used and no password is set, a random key will be provided.")

    parser.add_argument('in_file',
                        metavar='source file',
                        type=FileType('rb'),
                        help="input file to convert")

    parser.add_argument('out_file',
                        metavar='output file',
                        type=FileType('w'),
                        help="name/path for the output script")

    parser.add_argument('-m', '--minimal', action='store_true',
                        help="use a minimal/obfuscated recovery script")

    parser.add_argument('-c', '--compress', action='count',
                        help="compress file data with LZMA (-c = level 6, -cc = level 9)")

    parser.add_argument('-p', '--password', metavar='***', dest='password',
                        nargs="?", default='', help="encrypt data and password protect")

    parser.add_argument('-b', '--base64', action='store_true',
                        help="encode data with base64")

    parser.add_argument('-s', '--say', metavar='... ', dest='message',
                        help='print a message when the script is run')

    return parser.parse_args()


def print_welcome(args):
    print(f" - - Scriptify - - ")
    print(f"Source: {args.in_file.name}")
    print(f"Output: {args.out_file.name}\n")

    # if args.minimal:
    #     print("- Minimal script")
    if args.base64:
        print("- Base64 encoding")
    if args.compress:
        print("- LZMA compression")
    if args.password == '':
        print("- AES encryption (no password)")
    elif args.password:
        print("- AES encryption  -> " + args.password)
    if args.message:
        print("- Message display -> " + args.message)

    if input("\nDo you want to continue ? [Y/n] ") in {"n", "N"}:
        args.in_file.close()
        args.out_file.close()
        print("Cancelling.")
        exit()


def file_to_buffer(file_obj):
    # TODO: Memory improvements
    with file_obj as source_file:
        binary_content = source_file.read()
    return binary_content


if __name__ == '__main__':
    args = get_arguments()
    print_welcome(args)

    print("\n* Loading template... ")
    with open("container.template.py", 'r') as template:
        content = template.read()

    print("* Reading source file... ")
    file_buffer = file_to_buffer(args.in_file)
    original_filename = path.basename(args.in_file.name)
    substitutes = dict(name=original_filename,
                       msg='',
                       base64_enc='False', compression='False',
                       aes_enc='False', nonce='None', tag='None',
                       bin='None')

    if args.base64:
        print("* Encoding in Base64...")
        file_buffer = b64encode(file_buffer)
        substitutes['base64_enc'] = 'True'

    if args.password is not None:
        print("* Encrypting...")
        if args.password == '':
            password = ''.join(random.sample(string.hexdigits, 12))
        else:
            password = args.password
        print("  ->", password)

        hasher = SHA3_256.new(password.encode('utf-8'))
        key_hash = hasher.digest()

        aes_cipher = AES.new(key_hash, AES.MODE_EAX)
        file_buffer, tag = aes_cipher.encrypt_and_digest(file_buffer)
        nonce = aes_cipher.nonce

        substitutes['aes_enc'] = 'True'
        substitutes['tag'] = repr(tag)
        substitutes['nonce'] = repr(nonce)

    if args.compress:
        if args.compress >= 2:
            comp_level = 9
        else:
            comp_level = 6
        print(f"* Compressing (level {comp_level})...")
        file_buffer = compress(file_buffer, preset=comp_level)
        substitutes['compression'] = 'True'

    if args.message:
        substitutes['msg'] = args.message

    substitutes['bin'] = repr(file_buffer)
    script = Template(content).substitute(substitutes)

    print("* Creating script... ")
    with args.out_file as output:
        size = output.write(script)
    print(f"  -> {size // 1000}kB written.")

    if args.minimal:
        print("* Minifying script...")
        command = "pyminifier -O " + args.out_file.name + " > mini.py"
        print(f"  -> Calling '{command}'...")
        # os.system(command)

    size_before = path.getsize(args.in_file.name)
    size_after = path.getsize(args.out_file.name)

    print(f"* Done! {size_before // 1000}kB  ->  {size_after // 1000}kB")
