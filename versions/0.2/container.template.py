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
original_filename = "$$ORIG_FILENAME$$"
custom_message = "$$CUSTOM_MSG$$"
is_base_encoded = $$BASE64_ENC$$
is_aes_encrypted = $$AES_ENC$$
aes_key = $$AES_KEY$$

binary_repr = $$BIN_DATA$$


def display_message():
    if custom_message:
        print("\n - - - - - - - - - - - -")
        print(DISP_MESSAGE)
        print(" - - - - - - - - - - - -\n")


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
    data_buffer = eval(binary_repr)

    if is_base_encoded:
        data_buffer = b64decode(data_buffer)
    elif is_aes_encrypted:
        # ...
        pass

    with open(original_filename, 'wb') as dest_file:
        size = dest_file.write(data_buffer)

    print(f"Done. {size // 1000}kB written.")
