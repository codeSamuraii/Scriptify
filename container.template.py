#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base64 import b64decode
from lzma import decompress
from os import path
from sys import argv

# FILE INFORMATION
original_filename = "${name}"
custom_message = "${msg}"
is_base_encoded = ${base64_enc}
is_aes_encrypted = ${aes_enc}
is_compressed = ${compression}
aes_nonce = ${nonce}
aes_tag = ${tag}

blob_repr = ${bin}


if __name__ == '__main__':
    # Print custom message
    if custom_message:
        print(f"\n{' - ' * 12}\n{custom_message}\n{' - ' * 12}\n")

    # Confirm file recovery
    if input(f"Recover original file ? [Y/n] ") in {'n', 'N'}:
        print("Cancelling.")
        exit()

    print(f"Recovering \'{original_filename}\'... ")

    # if is_base_encoded:
    #     blob_repr = b64decode(blob_repr)

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
                blob_repr = cipher.decrypt_and_verify(blob_repr, aes_tag)
            except ValueError:
                print("Wrong password.")
            else:
                good_password = True

    if is_compressed:
        blob_repr = decompress(blob_repr)


    while path.exists(original_filename):
        original_filename = input("File already exists. New name: ")

    with open(original_filename, 'wb') as dest_file:
        size = dest_file.write(blob_repr)

    print(f"Done. {size // 1000}kB written.")
