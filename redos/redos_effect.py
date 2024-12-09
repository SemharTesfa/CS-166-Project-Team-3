import requests
import threading
import time

HOST_URL = 'http://localhost:5000/'


def write_err(file, res):
    res_j = res.json()
    file.write('400, ' + res_j.get('message') + '\n')

def write_ok(file, res):
    res_j = res.json()
    file.write('200,' + str(res_j.get('time')) + ','+ res_j.get('payload') + ',' + str(res_j.get('memory')) + '\n')


#post 25 malicious requests
def inject_traffic(reqs=25):
    print('attacker activity thread started')
    target_url = HOST_URL + 'changepass'
    curr_newpass = 'aaaaaaaaaaaaaaaaaaaaaaaaX'
    curr_oldpass = '^(a+)+$'
    for j in range(reqs):
        payload = {
            "newpass": curr_newpass,
            "oldpass": curr_oldpass
        }
        res = requests.post(target_url, data=payload)

'''
reqs - number of requests made.  If -1 it's unlimited.
payload - payload used if differeent from default
'''
def reg_traffic(reqs = 30): #simulates regular traffic with 1s delay in between
    print('regular user activity thread started')
    target_url = HOST_URL + "submit"
    with open("./disrupted_traffic.txt", "a") as file:
        for i in range(reqs):
            print("regular traffic req #", i, "sent")
            time.sleep(0.1)
            payload = {
                "body": "Random inconspicous text here!"
            }
            res = requests.post(target_url, data=payload)
            if res.status_code == 200:
                write_ok(file, res)
            else:
                write_err(file, res)


#default regular use traffic thread of 30 reqs
user_thread = threading.Thread(target=reg_traffic,args=())


user_thread.start()

#start 4 attacker threads (simulating 12 attacking machines in DDoS)
for i in range(0, 12):
    attacker_thread = threading.Thread(target=inject_traffic, args=())
    attacker_thread.start()