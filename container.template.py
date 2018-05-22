#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from sys import argv
from base64 import b64decode

# FLAGS
check_flag = lambda *f: any([flag in argv for flag in f])
yes_flg = check_flag('-y', '--yes')
#rem_flg = check_flag('-r', '--remove')
#out_flg = check_flag('-o', '--out')


# FILE INFORMATION
original_filename = path.basename("$$ORIG_FILENAME$$")
custom_message = "$$CUSTOM_MSG$$"
is_base_encoded = $$BASE64_ENC$$
is_aes_encrypted = $$AES_ENC$$
aes_nonce = $$AES_NONCE$$
aes_tag = $$AES_TAG$$

binary_repr = $$BIN_DATA$$


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

    with open(original_filename, 'wb') as dest_file:
        size = dest_file.write(binary_repr)

    print(f"Done. {size // 1000}kB written.")
