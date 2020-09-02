# cmk_livestatus_trafficlight
Trafficlight-style status display for CheckMK monitoring solution

# Livestatus API
A description can be found here:
https://checkmk.com/cms_livestatus.html


# Platform
Linux board with i/o ports and LAN interface as platform

http://www.orangepi.org/orangepizero/

## OS
I've chosen Armbian as OS:
https://www.armbian.com/orange-pi-zero/

### Preparation
root@orangepizero:~# 
armbian-config
apt update
apt upgrade
#apt install python3-pip
apt install python-dev
cd /opt/trafficlight/
git clone https://github.com/nvl1109/orangepi_zero_gpio.git
cd orangepi_zero_gpio/
python setup.py install


## GPIO
The gpio are named two ways:

    By port name: PH0, PG2, PE10, etc. These can be imported from port module:

>>> from pyA20.gpio import port
>>> dir(port)

    By connector name and pin number: gpio2p12, gpio3p8, lcdp18, uext1p3 and etc:

>>> from pyA20.gpio import connector
>>> dir(connector)

#pics/Orange-Pi-Zero-Pinout.jpg


https://github.com/nvl1109/orangepi_zero_gpio

## Script
Python script is located at:
/opt/trafficlight/checkstatus.py


## Livestatus Queries
Three queries are necessary:
1) check if hosts, which relates to certain 'contact_groups' are unacknowledged in status CRITICAL or WARN
2) check if services, which relates to hosts in certain 'contact_groups' are unacknowledged in status CRITICAL
3) check if services, which relates to hosts in certain 'contact_groups' are unacknowledged in status WARN


Query 1 result>0 leads always to a red Light

Query 2 result>0 leads to a red Light

Query 3 result>0 leads to a yellow Light

If none of the queries returns a number greater 0, the green light is turned on and all other lights are turned off.

# Enable Livestatus
Enable Livestatus API access from network:

omd stop;omd config set LIVESTATUS_TCP on;omd config set LIVESTATUS_TCP_ONLY_FROM '172.18.1.91';omd start
