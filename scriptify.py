#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scriptify v0.2
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
import os
from argparse import ArgumentParser, FileType
from base64 import b64encode
from lzma import compress
from os import path
from string import Template

from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import random


def get_arguments():
    def u(s): return "\033[4m" + s + "\033[0m"

    parser = ArgumentParser(
        prog="scriptify.py",
        description="Turn any file into a runnable python script",
        usage=(f"scriptify.py [-h] [--help]\n       "
               f"scriptify.py {u('source')} {u('output')} [-m] [-c[c]] [-b] [-p [password]] [-s message]"),
        epilog="If encryption is used and no password is set, a random key will be provided.")

    parser.add_argument('in_file',
                        metavar='source',
                        type=FileType('rb'),
                        help="input file to convert")

    parser.add_argument('out_file',
                        metavar='output',
                        type=FileType('w'),
                        help="name/path for the output script")

    parser.add_argument('-m', '--minimal', action='store_true',
                              help="use a minimal/obfuscated recovery script (requires pyminifier)")

    parser.add_argument('-c', '--compress', action='count',
                              help="compress file data with LZMA (x1 = level 6, x2 = level 9)")

    parser.add_argument('-p', '--password', metavar='***', dest='password',
                        nargs="?", default='', help="encrypt data with AES and password protect output script")

    parser.add_argument('-s', '--say', metavar='... ', dest='message',
                        help='print a message when the script is run')

    return parser.parse_args()


def print_welcome(args):
    print(f" - - Scriptify - - ")
    print(f"Source: {args.in_file.name}")
    print(f"Output: {args.out_file.name}\n")

    if args.minimal:
        print("- Minimal script")
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

    in_name = path.basename(args.in_file.name)
    in_path = path.abspath(path.dirname(args.in_file.name))
    out_name = path.basename(args.out_file.name)
    out_path = path.abspath(path.dirname(args.out_file.name))

    print("\n* Loading template... ")
    with open("container.template.py", 'r') as template:
        content = template.read()

    print("* Reading source file... ")
    file_buffer = file_to_buffer(args.in_file)
    substitutes = dict(name=in_name,
                       msg='',
                       base64_enc='False', compression='False',
                       aes_enc='False', nonce='None', tag='None',
                       bin="None")

    if args.compress:
        if args.compress >= 2:
            comp_level = 9
        else:
            comp_level = 6
        print(f"* Compressing (level {comp_level})...")
        file_buffer = compress(file_buffer, preset=comp_level)
        substitutes['compression'] = 'True'

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

    if args.message:
        substitutes['msg'] = args.message

    if args.minimal:
        # Base64 required, otherwise minifying breaks the file
        print("* Encoding in Base64...")
        file_buffer = b64encode(file_buffer)
        substitutes['base64_enc'] = 'True'

    substitutes["bin"] = repr(file_buffer)
    script = Template(content).substitute(substitutes)

    print("* Creating script... ")
    with args.out_file as output:
        size = output.write(script)
    print(f"  -> {size // 1000}kB written.")

    if args.minimal:
        print("* Minifying script...")
        tmp_name = "tmp_" + out_name
        cmd_mv = f"mv {out_name} {tmp_name}"
        cmd_mini = f"pyminifier --outfile={out_name} {tmp_name}"
        cmd_rm = f"rm {tmp_name}"

        current_path = os.getcwd()
        os.chdir(out_path)
        print(f"  -> Calling '{cmd_mv}'...")
        os.system(cmd_mv)
        print(f"  -> Calling '{cmd_mini}'...")
        os.system(cmd_mini)
        print(f"  -> Calling '{cmd_rm}'...")
        os.system(cmd_rm)
        os.chdir(current_path)

    size_before = path.getsize(path.join(in_path, in_name))
    size_after = path.getsize(path.join(out_path, out_name))

    print(f"* Done! {size_before // 1000}kB  ->  {size_after // 1000}kB")
