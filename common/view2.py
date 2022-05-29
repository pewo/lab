#import pprint
import os
import socket
import json
from flask import Flask, Response, request

APP = Flask(__name__)

ROOT = "/var/tmp/labconf"


def resolve_ip(ip_address):
    # type: (str) -> str
    """Resolve a hostname to its IP if possible"""
    interfaces = socket.gethostbyaddr(ip_address)
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
    except:
        return myjson
    else:
        for line in f:
            print("line:", line)
            #y = line.strip()
            #print("y:", y)
            key, value = line.strip().split(":", 2)
            if key:
                key = key.rstrip().lstrip()
            else:
                continue

            if value:
                value = value.rstrip().lstrip()
            else:
                continue
            myjson[key] = value
        f.close()

    return myjson



@APP.route('/test')
def test():
    """Function to get labconf"""
    res = ""
    #for k, v in os.environ.items():
    #   str += k + "=" + v + "<BR>"
    #str += pprint.pformat(request.environ, depth=5) + '<BR><BR>'
    #str += pprint.pformat(request.headers, depth=5) + '<BR><BR>'
    #str += pprint.pformat(request.remote_addr, depth=5) + '<BR><BR>'
    #str += pprint.pformat(resolve_ip(request.remote_addr), depth=5) + '<BR><BR>'
    #str += pprint.pformat(labconf(request.remote_addr), depth=5)
    myjson = labconf(request.remote_addr)
    res = json.dumps(myjson)
    #return Response(str, mimetype="text/text")
    return Response(res)
    #return(str)

if __name__ == "__main__":
    PORT = 8443
    PORT = int(os.environ.get('PORT', PORT))
    APP.run(debug=True, host='0.0.0.0', port=PORT)
