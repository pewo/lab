#import pprint
import os
import socket
import json
import time
import subprocess
from flask import Flask, Response, request

app = Flask(__name__)

ROOT = "/var/tmp/labconf"

START = int(time.time())
refresh_conf = 0

print("Starting:", START)


def resolve_ip(ip_address):
    # type: (str) -> str
    """Resolve a hostname to its IP if possible"""
    try:
        interfaces = socket.gethostbyaddr(ip_address)
    except Exception as e:
        print("Error getting hostname using ip address", ip_address, " error: ", e)
        return ip_address
    else:
        if len(interfaces) == 0:
            return ip_address
        addr = interfaces[0]

    return addr

def labconf(ip_address):
    # type: (str) -> str
    """Try to find labonf and return it"""

    myjson = {}
    addr = resolve_ip(ip_address)
    conf = ROOT + "/" + addr + "/config"
    try:
        st_file = os.stat(conf)
    except Exception as e:
        print("Error checking file", conf, " error: ", e)
        return myjson
    else:
        myjson["mtime"] = int(st_file.st_mtime)

    try:
        f = open(conf, "r")
    except Exception as e:
        print("Error reading file", conf, " error: ", e)
        return myjson
    else:
        line_no = 0
        for line in f:
            line_no += 1
            # print("line(", line_no, "): ", line.strip())

            # Remove comments
            line = line.split("#", 1)[0]

            # key, value = line.strip().split(":", 2)
            mylist = line.strip().split(":", 2)

            if len(mylist) < 2:
                print("Bad line on line", line_no)
                continue

            key, value = mylist
            if key:
                key = key.rstrip().lstrip()
            else:
                print("Bad key on line", line_no)
                continue

            if value:
                value = value.rstrip().lstrip()
            else:
                print("Bad value on line", line_no)
                continue

            myjson[key] = value
        f.close()

    return myjson



@app.route('/')
def home():
    """Function to get labconf"""
    res = ""
    global refresh_conf

    refresh_age = int(time.time()) - refresh_conf

    print("refresh_age:", refresh_age)
    print("refresh_conf:", refresh_conf)

    if refresh_conf < 1 or refresh_age > 20: 
        refresh_conf = int(time.time())
        print("Refreshing labconf")
        try:
            subprocess.call(["/usr/bin/git", "-C", ROOT, "pull"])
        except Exception as e:
            print("Error updating labconf, error:", e)
        else:
            print("Updating labconf ok")

    myjson = labconf(request.remote_addr)
    res = json.dumps(myjson)
    return Response(res)

if __name__ == "__main__":
    #PORT = 8443
    #PORT = int(os.environ.get('PORT', PORT))
    #app.run(debug=True, host='0.0.0.0', port=PORT)
    app.run(debug=True, host='0.0.0.0')
