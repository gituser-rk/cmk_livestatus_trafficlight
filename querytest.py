#!/usr/bin/env python3
# Program for accessing Livestatus from Python
# /opt/trafficlight/checkstatus.py
import socket
#import json, os, socket

# for local/remote sites: TCP address/port for Livestatus socket
HOST = 'omd.domain.tld'
PORT = 6557

#count of unacknowledged hosts in state CRITICAL:
#query1 = "GET hosts\\nStats: state > 0\\nFilter: contact_groups ~ Netzwerk|Linux\\nFilter: host_acknowledged = 0\\n"
query1 = "GET hosts\nStats: state > 0\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: host_acknowledged = 0\n\n\n"
#count of unacknowledged service errors in state CRITICAL:
query2 = "GET services\nStats: state = 2\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: service_acknowledged = 0\n\n\n"
#count of unacknowledged service errors in state WARNING:i
query3 = "GET services\nStats: state = 1\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: service_acknowledged = 0\n\n\n"

### start query 1
# connect to Livestatus
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# send our request and let Livestatus know we're done
s.sendall(query1.encode('utf-8'))
# read reply
reply = s.recv(1024)
# close connection
s.close()
print('Hosts in state CRITICAL:', reply.decode('utf-8'))
### end query 1
### start query 2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(query2.encode('utf-8'))
reply = s.recv(1024)
s.close()
print('Services in state CRITICAL:', reply.decode('utf-8'))
### end query 2

### start query 3
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(query3.encode('utf-8'))
reply = s.recv(1024)
s.close()
print('Services in state WARNING:', reply.decode('utf-8'))
### end query 3
