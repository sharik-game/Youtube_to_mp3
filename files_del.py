from os import getcwd, remove
import logging
def delete_file(name: str):
    try:
        remove(getcwd() + "/" + name)
        print("files_del done everything")
    except FileNotFoundError:
        print("error")