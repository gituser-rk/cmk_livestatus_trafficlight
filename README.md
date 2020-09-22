# cmk_livestatus_trafficlight
Trafficlight-style status display for CheckMK monitoring solution

# Livestatus API
A description can be found here:
https://checkmk.com/cms_livestatus.html


# Platform
Linux board with i/o ports and LAN interface as platform. For me a wired LAN interface was important. 
This is the board I used:

http://www.orangepi.org/orangepizero/

## OS
I've chosen Armbian as OS:
https://www.armbian.com/orange-pi-zero/

### Preparation
```
root@orangepizero:~# 
root@orangepizero:~# armbian-config
root@orangepizero:~# apt update
root@orangepizero:~# apt upgrade
root@orangepizero:~# apt install python3-dev
root@orangepizero:~# mkdir /opt/trafficlight/
root@orangepizero:~# cd /opt/trafficlight/
root@orangepizero:~# git clone https://github.com/nvl1109/orangepi_zero_gpio.git
root@orangepizero:~# cd orangepi_zero_gpio/
root@orangepizero:~# python3 setup.py install
```
## Script
Python script is located at:

/opt/trafficlight/checkstatus.py

Tasks: Query Livestatus, calculate and set LED Status

Loop every 30 seconds

## Livestatus Queries
Three queries are necessary:
1) check if hosts, which relates to certain 'contact_groups' are unacknowledged (and not in scheduled maintanance) in status CRITICAL or WARN
2) check if services, which relates to hosts in certain 'contact_groups' are unacknowledged (and not in scheduled maintanance) in status CRITICAL
3) check if services, which relates to hosts in certain 'contact_groups' are unacknowledged (and not in scheduled maintanance) in status WARN


Query 1 result>0 leads to a red Light

Query 2 result>0 leads to a red Light

Query 3 result>0 leads to a yellow Light

If none of the queries returns a number greater 0, the green light is turned on and all other lights are turned off.

# Enable Livestatus
Enable Livestatus API access from network:

omd stop;omd config set LIVESTATUS_TCP on;omd config set LIVESTATUS_TCP_ONLY_FROM '172.18.1.91';omd start

## GPIO

RED LED: Port PG6

YELLOW LED: Port PG7

GREEN LED: Port PA7

![Pic11](pics/Orange-Pi-Zero-Pinout.jpg)

https://github.com/nvl1109/orangepi_zero_gpio

![Pic5](pics/5.jpg)

## Power Supply

12V feeding via Ethernet cable spare pins. This should be enough for 5 to 10 meters cable length. which is the case for me. If you need to provide the power over a longer cable, you schould use a higher voltage. But ATTENTION: two resistors must be removed from the OrangePi Zero board. They are 750 Ohms parallel to the PoE input and would overheat at such high voltages. See documentation.
PoE pin of Orangepizero wired to input of stepdown converter. Output of stepdown converter wired to 5V pin of Orangepizero.

https://www.electrodragon.com/product/dc-dc-step-power-module-mp1584-fixed-output/

![Pic0](pics/stepdown.PNG)
![Pic4](pics/4.jpg)

## More Pictures

![Pic1](pics/1.jpg)

![Pic2](pics/2.jpg)

![Pic3](pics/3.jpg)

![Pic6](pics/6.jpg)

![Pic7](pics/7.jpg)
