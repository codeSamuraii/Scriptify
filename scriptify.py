# -*- coding: utf-8 -*-
"""
Scriptify v0.1
© Rémi Héneault (@codeSamuraii)
https://github.com/codeSamuraii
"""
import sys
from os import path


def print_exit(message):
    print(message)
    exit()


def open_file(path, mode):
    try:
        filename = path.basename(path)
        file_object = open(path, mode)
    except FileNotFoundError:
        print_exit(f"Error while opening \'{filename}\': not found.")
    except PermissionError:
        print_exit(f"Error while opening \'{filename}\': not allowed.")
    except OSError as err:
        print_exit(f"I/O Error while opening \'{filename}\': {err}")
    except Exception as unex:
        print_exit(f"Unknown exception while opening \'{filename}\': {unex}")

    return file_object


def file_to_string(file_path):
    with open_file(file_path, 'rb') as source_file:
        binary_content = source_file.read()

    hex_string = repr(binary_content)
    return hex_string


def string_to_file(hex_string, new_file_path):
    binary_data = eval(hex_string)
    if not new_file_path.endswith('.py'):
        new_file_path += '.py'

    with open_file(new_file_path, 'wb') as new_file:
        size = new_file.write(binary_data)

    filename = path.basename(new_file_path)
    return filename, size


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print_exit("Usage: scriptify.py [source] [destination].py")
    else:
        source_path = argv[1]
        dest_path = argv[2]

    src_name = path.basename(source_path)
    src_abspath = path.abspath(path.expanduser(source_path))
    src_size = path.getsize(source_path)

    dst_name = path.basename(dest_path)
    dst_abspath = path.abspath(path.expanduser(dest_path))

    print(" ~ ~ Scriptify v0.1 ~ ~\n")
    print(f"Source      : {src_name}")
    print(f"Destination : {dst_name}")

    if input("\nDo you want to continue ? [Y/n] ") in {"n", "N"}:
        print_exit("Aborting.")

# COMBAK: HERE
