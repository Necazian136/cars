import sqlite3
import time

import requests

from client.client.settings import BASE_DIR


def get_ip():
    f = open(BASE_DIR + '/server_ip.txt')
    client_url = f.read().split('\n')[1].split('=')[1]
    f.close()
    return client_url


def sync():
    try:
        response = requests.post('http://' + get_ip() + ':8000/synchronization/')
    except:
        pass

def check_status():
    try:
        requests.post('http://' + get_ip() + ':8000/status/')
        return True
    except:
        return False


while True:
    online = False
    while not online:
        time.sleep(5)
        online = check_status()
    print('client online')
    checking_cnt = 0
    while online:
        time.sleep(1)
        checking_cnt += 1
        if checking_cnt % 60 == 0:
            checking_cnt = 1
            sync()
            online = check_status()
    print('client offline')

