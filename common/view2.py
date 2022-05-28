from flask import Flask, Response, request
import pprint
import os
import socket
import json

app = Flask(__name__)

root = "/var/tmp/labconf"


def resolve_ip(ip):
    # type: (str) -> str
    """Resolve a hostname to its IP if possible"""
    interfaces = socket.gethostbyaddr(ip)
    if len(interfaces) == 0:
        return ip
    addr = interfaces[0]
    return(addr)

def labconf(ip):
    # type: (str) -> str
    
    myjson = {}
    res = ""
    addr = resolve_ip(ip)
    conf = root + "/" + addr + "/config"
    try:
        st = os.stat(conf)
    except:
        return(mysjon)
    else:
        myjson["mtime"]=int(st.st_mtime)

    try:
       f = open(conf,"r")
    except:
       return(myjson)
    else:
       for x in f:
           print("x:",x)
           y = x.strip()
           print("y:",y)
           key,value = y.split(":",2)
           if key:
               key = key.rstrip().lstrip()
           else:
               continue

           if value:
               value = value.rstrip().lstrip()
           else:
               continue
           myjson[key]=value
       f.close()

    return(myjson)



@app.route('/test')
def test():
    str = ""
    #for k, v in os.environ.items():
    #   str += k + "=" + v + "<BR>"
    #str += pprint.pformat(request.environ, depth=5) + '<BR><BR>'
    #str += pprint.pformat(request.headers, depth=5) + '<BR><BR>'
    #str += pprint.pformat(request.remote_addr, depth=5) + '<BR><BR>'
    #str += pprint.pformat(resolve_ip(request.remote_addr), depth=5) + '<BR><BR>'
    #str += pprint.pformat(labconf(request.remote_addr), depth=5) 
    myjson = labconf(request.remote_addr)
    str = json.dumps(myjson)
    #return Response(str, mimetype="text/text")
    return Response(str)
    #return(str)

#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 5001))
app.run(debug=True, host='0.0.0.0', port=8443)

