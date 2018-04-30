# -*- coding: utf-8 -*-
from sys import argv


# OPTIONAL FLAGS #

yes_flg = ('-y' or '--yes') in argv
#rem_flg = ('-r' or '--remove') in argv
#out_flg = ('-o' or '--out') in argv


# FILE DATA #

ORIG_FILENAME = "$ID_FILENAME"
BIN_DATA = "$ID_DATA"


# EXTRACT SCRIPT #

if __name__ == '__main__':
    if not yes_flg:
        if input("Recover original file ? [Y/n] ") in "Nn":
            print("Cancelling.")
            exit()

    print("Recovering \'{ORIG_FILENAME}\'... ", end="")
    binary_data = eval(BIN_DATA)
    with open_file(ORIG_FILENAME, 'wb') as new_file:
        size = new_file.write(binary_data)
    print(f"Done.\n{size // 1000} written.")
