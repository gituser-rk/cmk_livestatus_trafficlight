#!/usr/bin/env python3
# Program for accessing CheckMK Livestatus over network and switching a traffic light depending of the query results
# recommended location of the program: /opt/trafficlight/checkstatus.py
import socket, os, sys
if not os.getegid() == 0:
    sys.exit('Script must run as root')
# set to true for debug output, otherwise to false
debug = true
clear = lambda: os.system('clear')

# for local/remote sites: TCP address/port for CheckMK Livestatus socket
#HOST = '172.20.20.92'
HOST = 'omd.ilb.int'
PORT = 6557

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
# define Ports for LEDs
ledR = port.PG6
ledY = port.PG7
ledG = port.PA7
# initialize LED ports
gpio.init()
gpio.setcfg(ledR, gpio.OUTPUT)
gpio.setcfg(ledY, gpio.OUTPUT)
gpio.setcfg(ledG, gpio.OUTPUT)

#count of unacknowledged hosts not in scheduled downtime in state CRITICAL:
query1 = "GET hosts\nStats: state > 0\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: host_acknowledged = 0\n\n\n"
#count of unacknowledged service errors not in scheduled downtime in state CRITICAL:
query2 = "GET services\nStats: state = 2\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: service_acknowledged = 0\n\n\n"
#count of unacknowledged service errors not in scheduled downtime in state WARNING:
query3 = "GET services\nStats: state = 1\nFilter: scheduled_downtime_depth = 0\nFilter: contact_groups ~ Netzwerk|Linux\nFilter: service_acknowledged = 0\n\n\n"

try:
    print ("Press CTRL+C to exit")
    # main loop
    while True:
        ### start query 1
        # connect to Livestatus
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        # send our request and let Livestatus know we're done
        s.sendall(query1.encode('utf-8'))
        # read reply
        reply1 = s.recv(1024)
        # close connection
        s.close()
        ### end query 1
        ### start query 2
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(query2.encode('utf-8'))
        reply2 = s.recv(1024)
        s.close()
        ### end query 2
        ### start query 3
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(query3.encode('utf-8'))
        reply3 = s.recv(1024)
        s.close()
        ### end query 3

        if debug == true:
            clear()
            print('   Hosts in state CRITICAL: ', reply1.decode('utf-8'))
            print('Services in state CRITICAL: ', reply2.decode('utf-8'))
            print(' Services in state WARNING: ', reply3.decode('utf-8'))

        # calculate LED state
        # Red LED
        if reply1 > 0 or reply2 > 0: 
            stateR = 1
        else:
            stateR = 0
        # Yellow LED
        if reply3 > 0: 
            stateY = 1
        else:
            stateY = 0
        # Green LED
        if stateR == 0 and stateY == 0: 
            stateG = 1
        else:
            stateG = 0       
        # set LED state
        gpio.output(ledR, stateR)
        gpio.output(ledY, stateY)
        gpio.output(ledG, stateG)
        if debug == true:
            print ('LED Red     state: ', stateR)
            print ('LED Yellow  state: ', stateY)
            print ('LED Green   state: ', stateG)
        sleep(10)
    except KeyboardInterrupt:
        print ("Goodbye.")