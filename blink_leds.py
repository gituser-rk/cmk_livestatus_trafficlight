#!/usr/bin/env python

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must run as root')

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

ledR = port.PG6
ledY = port.PG7
ledG = port.PA7

gpio.init()
gpio.setcfg(ledR, gpio.OUTPUT)
gpio.setcfg(ledY, gpio.OUTPUT)
gpio.setcfg(ledG, gpio.OUTPUT)

try:
    print ("Press CTRL+C to exit")
    while True:
        gpio.output(ledR, 1)
        gpio.output(ledY, 1)
        gpio.output(ledG, 1)
        #print "led set 1 \r\n"
        sleep(2)
        gpio.output(ledR, 0)
        gpio.output(ledY, 0)
        gpio.output(ledG, 0)
        #print "led set 0 \r\n"
        sleep(2)
        """
        gpio.output(ledR, 1)
        gpio.output(ledY, 1)
        gpio.output(ledG, 1)
        sleep(0.1)
        gpio.output(ledR, 0)
        gpio.output(ledY, 0)
        gpio.output(ledG, 0)
        sleep(0.1)

        sleep(0.6)
        """
except KeyboardInterrupt:
    print ("Goodbye.")
