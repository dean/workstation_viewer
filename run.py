from flask import Flask
import sys
import subprocess
import json
import urllib2

this_color = subprocess.check_output(["hostname"]).split(".")[0]
sys.dont_write_bytecode = True

app = Flask(__name__)

@app.route("/loggedin")
def home():
    users = get_users()
    print users
    return json.dumps(users)

# https://gist.github.com/ecnahc515/6645184
def get_users():
    w = subprocess.check_output(["w", "-h", "-f"])
    users = [tuple(line.split()[:2]) for line in w.strip().split('\n')]
    return users

@app.route("/whosloggedin")
def whosloggedin():
    pre = "http://"
    workstation_subs = ['sub1', 'sub2', 'sub3']
    host = "host"
    endpoint = "/loggedin"

    output = ''

    for color in workstation_colors:
        try:
            if color != this_color:
                resp = urllib2.urlopen("http://" + color + host + endpoint)
                read_resp = resp.read()
                users = json.loads(read_resp)
            else:
                users = json.loads(home())

            output += color + host + ":\n"
            output += ''.join(["\t" + user[0] + "\t" + user[1] + "\n"
                                for user in users if user[0] != "root"])
            output += "\n"
        except:
            continue

    print output
    return output

app.run("127.0.0.1", 80, debug=True)
