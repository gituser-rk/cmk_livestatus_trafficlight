#!/usr/bin/env python
# Sample program for accessing Livestatus from Python

import json, os, socket

# for local site only: file path to socket
# address = "%s/tmp/run/live" % os.getenv("OMD_ROOT")
# for local/remote sites: TCP address/port for Livestatus socket
address = ("172.20.20.92", 6557)

# connect to Livestatus
family = socket.AF_INET if type(address) == tuple else socket.AF_UNIX
sock = socket.socket(family, socket.SOCK_STREAM)


### start query 1
sock.connect(address)

# send our request and let Livestatus know we're done
sock.sendall(GET "hosts\nOutputFormat: json\nStats: state > 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: host_acknowledged = 0")
sock.shutdown(socket.SHUT_WR)

# receive the reply as a JSON string
chunks = []
while len(chunks) == 0 or chunks[-1] != "":
    chunks.append(sock.recv(4096))
sock.close()
reply = "".join(chunks)

# print the parsed reply
print("Hosts in ststus CRITICAL:")
print(json.loads(reply))
### end query 1
