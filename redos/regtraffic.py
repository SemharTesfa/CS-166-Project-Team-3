import requests
import json
import os
import psutil
import threading
import time
import random

HOST_URL = 'http://localhost:5000/'


def write_err(file, res):
    res_j = res.json()
    file.write('400, ' + res_j.get('message') + '\n')

def write_ok(file, res):
    res_j = res.json()
    file.write('200,' + str(res_j.get('time')) + ','+ res_j.get('payload') + ',' + str(res_j.get('memory')) + '\n')


def inject_traffic(reqs=25):
    target_url = HOST_URL + 'changepass'
    curr_newpass = 'aaaaaaaaaaaX'
    curr_oldpass = '^(a+)+$'
    with open("./inj_traffic.txt") as file:
        for j in range(reqs):
            payload = {
                "newpass": curr_newpass,
                "curr_oldpass": curr_oldpass
            }
            curr_newpass = 'a' + curr_newpass
            res = requests.post(target_url, data=payload)

'''
reqs - number of requests made.  If -1 it's unlimited.
payload - payload used if differeent from default
'''
def reg_traffic(reqs): #simulates regular traffic with 1s delay in between
    target_url = HOST_URL + "submit"
    with open("./reg_traffic.txt", "a") as file:
        for i in range(reqs):
            print("regular traffic req #", i, "sent")
            time.sleep(0.1)
            payload = {
                "body": "Random inconspicous text here!"
            }
            #5% chance that request has badword and gets rejected
            #if random.randint(1,20) == 10:
            #    payload["body"] += " badword"
            res = requests.post(target_url, data=payload)
            if res.status_code == 200:
                write_ok(file, res)
            else:
                write_err(file, res)

reg_traffic(30)
'''

def malicious_sub(reqs):
    target_url = HOST_URL + "submit"
    with open("./malicious_sub.txt", "a") as file:
        textStart = "badwooo"
        textEnd = "rx"
        for i in range(reqs):
            print("malicious traffic req #", i, "sent")
            time.sleep(1.5)
            payload = {
                "body": textStart + textEnd
            }
            res = requests.post(target_url, data=payload)
            if res.status_code == 200:
                write_ok(file, res)
            else:
                write_err(file, res)
            textStart += "o"

def malicious_changepass(reqs, payload):
    pass
'''