
import os
import sys
import datetime


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'src\\', relative_path)

def getTimeNowText():
    time = datetime.datetime.now()
    return f'{time.hour}_{time.minute}_{time.second}'


def readLocalFile(filename):
    f = open(filename, 'r')
    txt = f.read()
    f.close()

    return txt


def writeLocalFile(filename, txt):
    f = open(filename, 'w')
    f.write(txt)
    f.close()