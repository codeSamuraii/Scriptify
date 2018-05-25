#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from sys import argv
from lzma import decompress
from base64 import b64decode

# FLAGS
check_flag = lambda *f: any([flag in argv for flag in f])
yes_flg = check_flag('-y', '--yes')
#rem_flg = check_flag('-r', '--remove')
#out_flg = check_flag('-o', '--out')


# FILE INFORMATION
original_filename = "${name}"
custom_message = "${msg}"
is_base_encoded = ${base64_enc}
is_aes_encrypted = ${aes_enc}
is_compressed = ${compression}
aes_nonce = ${nonce}
aes_tag = ${tag}

binary_repr = ${bin}


def display_message():
    if custom_message:
        print("\n- - - - - - - - - - - -")
        print(custom_message)
        print("- - - - - - - - - - - -\n")


def confirm_recovery():
    if not yes_flg:
        if input(f"Recover original file ? [Y/n] ") in {'n', 'N'}:
            print("Cancelling.")
            exit()
    else:
        print("Argument -y specified, skipping confirmation.")


if __name__ == '__main__':
    # Print custom message
    display_message()

    # Confirm file recovery
    confirm_recovery()

    print(f"Recovering \'{original_filename}\'... ")

    if is_compressed:
        binary_repr = decompress(binary_repr)

    if is_aes_encrypted:
        from Crypto.Cipher import AES
        from Crypto.Hash import SHA3_256
        good_password = False

        while not good_password:
            password = input("Password : ")
            hasher = SHA3_256.new(password.encode('utf-8'))
            key_hash = hasher.digest()
            cipher = AES.new(key_hash, AES.MODE_EAX, aes_nonce)

            try:
                binary_repr = cipher.decrypt_and_verify(binary_repr, aes_tag)
            except ValueError:
                print("Wrong password.")
            else:
                good_password = True

    if is_base_encoded:
        binary_repr = b64decode(binary_repr)

    while path.exists(original_filename):
        original_filename = input("File already exists. New name: ")

    with open(original_filename, 'wb') as dest_file:
        size = dest_file.write(binary_repr)

    print(f"Done. {size // 1000}kB written.")
