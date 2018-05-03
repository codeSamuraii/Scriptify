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


def open_file(filepath, mode):
    try:
        filename = path.basename(filepath)
        file_object = open(filepath, mode)
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

    print("\n ~ ~ Scriptify v0.1 ~ ~\n")
    print(f"Source      : {src_name}")
    print(f"Destination : {dst_name}")

    if input("\nDo you want to continue ? [Y/n] ") in {"n", "N"}:
        print_exit("Aborting.")

    print("* Reading source file... ", end='')
    bin = file_to_string(src_abspath)
    print("OK.")

    print("* Loading template... ", end='')
    with open_file("container_script.template", 'r') as template:
        script = template.read()
    print("OK.")

    print("* Creating script... ", end='')
    with open_file(dst_abspath, 'w') as output:
        filled = script.replace("$ID_DATA", bin).replace("$ID_FILENAME", src_name)
        output.write(filled)
        print("OK.")

    print("Finished. Launch the script with Python to recover your file.")

# TODO:
#     - Documentation
#     - Binary data compression
#     - Binary data encryption w/ password protect
#     - Cleaning, design improvements
