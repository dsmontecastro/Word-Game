import os, sys


def get_file(file):
    address = ""
    if getattr(sys, "frozen", False):
        address = sys._MEIPASS
    else:
        address = os.getcwd()

    return os.path.join(address, file)
