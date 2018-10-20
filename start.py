import os
from subprocess import call
import multiprocessing.dummy as multiprocessing
import sys

MAIN_DIR = os.path.dirname(__file__)

def start_server():
    f = open(MAIN_DIR + '/client/server_ip.txt')
    client_url = f.read().split('\n')[1].split('=')[1]
    f.close()
    os.system(MAIN_DIR + "/venv/bin/python3 " + MAIN_DIR + "/client/manage.py runserver " + client_url + ":8000")
    return True


def start_chip():
    os.system(MAIN_DIR + "/venv/bin/python3 " + MAIN_DIR + '/client/chip/main.py')
    return True


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pool.map(lambda f: f(), [start_server, start_chip])
    pool.close()
    pool.join()
