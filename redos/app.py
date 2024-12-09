from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from memory_profiler import memory_usage

import re
import time 

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "60 per hour"],
)

@app.route('/')
def retdef():
    return render_template('index.html')


#regular regex
@app.route('/signform')
def signform():
    return render_template('signform.html')

@app.route('/change')
def change():
    return render_template('changepass.html')

#this wrapper using memory_profiler is required to profile memory
def badword_regex(regex, payload):
    return re.search(regex, payload)


#vulnerability: totally unprotected regex with catastrophic backtracking
@app.route('/submit', methods=['POST'])
def submit():
    payload = request.form.get('body')
    start = time.time()
    mem_use, has_bad_word = memory_usage((badword_regex, (r"badw(o+|0+|O+)+rd", payload)), retval=True, max_iterations=1)

    if has_bad_word:
            return jsonify({
                "success": False,
                "message": "error, form has inapropriate language"
            }), 400
    else:
        with open("./messages.txt", "a") as file:
            file.write(payload + "\n")
        return jsonify({
                 "success": True,
                 "time": time.time() - start,
                 "payload": payload,
                 "memory": mem_use
            }), 200


#mitigation: have server side length limiting and rate limiting + safer regex
@app.route('/submit_limited', methods=['POST'])
@limiter.limit("1/second", override_defaults=False) #limits to one request pers second + the defaults
def submit_limited():
    payload = request.form.get('body')
    if len(payload) > 100:
        return jsonify({
                "success": False,
                "message": "request message too long!"
            }), 400
    else:
        start = time.time()
        #uses regex to check if badword in payload
        mem_use, has_bad_word = memory_usage((badword_regex,(r"(badw[0,O,o]+rd)",payload,)), retval=True, max_iterations=1)
        if has_bad_word:
            return jsonify({
                    "success": False,
                    "message": "error, form has inapropriate language"
                }), 400
        else:
            return jsonify({
                    "success": True,
                    "time": time.time() - start,
                    "payload": payload,
                    "memory": mem_use
                }), 200

#regex injection attack
@app.route('/changepass', methods=['POST'])
def changepass():
    oldpass = request.form.get('oldpass')
    newpass = request.form.get('newpass')
    start = time.time()
    mem_use, has_oldpass = memory_usage((badword_regex,(oldpass, newpass,)), retval=True, max_iterations=1)
    print(sum(mem_use))
    if has_oldpass:
         return jsonify({
                   "success": False,
                   "message": "new password cannot contain old!"
              }),400 
    else:
        return jsonify({
                 "success": True,
                 "message": "password successfully changed!",
                 "time": time.time() - start,
                 "payload": oldpass,
                 "searched": newpass,
                 "memory": mem_use
            }), 200

#mitigation: sanitize inputs by escaping characters
#regex injection attack

def changepass_filtered():
    oldpass = request.form.get('oldpass')
    newpass = request.form.get('newpass')

    escaped_oldpass = re.escape(oldpass)
    escaped_newpass = re.escape(newpass)

    start = time.time()
    mem_use, has_oldpass = memory_usage((badword_regex, (escaped_oldpass, escaped_newpass)), retval=True, max_iterations=1)

    if has_oldpass:
        return jsonify({
            "success": False,
            "message": "new password cannot contain old!"
        }), 400 
    else:
        return jsonify({
            "success": True,
            "time": time.time() - start,
            "payload": oldpass,
            "memory": mem_use
        }), 200

if __name__ == '__main__':
    app.run(debug=True)