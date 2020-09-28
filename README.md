# cmk_livestatus_trafficlight
Trafficlight-style status display for CheckMK monitoring solution

# CheckMK Livestatus API
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
update linux system and compile the GPIO library
```
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
## Python program
Copy the Python program "checkstatus.py" to the folder /opt/trafficlight.

or:
root@orangepizero:~# cd /opt/trafficlight/
root@orangepizero:~# git clone https://github.com/nvl1109/orangepi_zero_gpio.git


/opt/trafficlight/checkstatus.py

Tasks of the program: Query Livestatus, calculate and set LED Status
Loop every 10 seconds.

### Autostart
Put the following two lines in /etc/rc.local (before 'exit 0' !!!):
```
cd /opt/trafficlight/
./checkstatus.py
```

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
Enable Livestatus API access in CheckMK from network:

omd stop;omd config set LIVESTATUS_TCP on;omd config set LIVESTATUS_TCP_ONLY_FROM '172.18.1.91';omd start

## GPIO

RED LED: Port PG6

YELLOW LED: Port PG7

GREEN LED: Port PA7

![Pic11](pics/Orange-Pi-Zero-Pinout.jpg)

https://github.com/nvl1109/orangepi_zero_gpio

![Pic9](pics/9.jpg)

## Power Supply

12V/0.5A feeding via Ethernet cable spare pins. This should be enough for 5 to 15 meters cable length depending on the cable quality. If you need to provide the power over a longer cable, you schould use a higher voltage. But ATTENTION: two resistors must be removed from the OrangePi Zero board. They are 750 Ohms parallel to the PoE input and would overheat at such high voltages. See documentation. I've removed them anyway.
PoE pin of Orangepizero wired to input of stepdown converter. Output of stepdown converter wired to 5V pin of Orangepizero.

Power consumtion: The maximum power consumtion I saw at 12V side was 3.4 Watt during bootup when all LEDs (external, trafficlight) are on. After bootup a maximum of 1.6 Watts is drawn when all LEDs are on.
Also, I've added a Diode 1N4007 in series between 12V+ PoE and Vin of the buck converter as a protection in case of wrong polarity.
```
+12V PoE o----=>|----o +Vin buck converter +5V Vout o----------o +5V OrangePi Zero
             1N4007
             
  0V PoE o-----------o -Vin buck converter -5V Vout o----------o GND OrangePi Zero
```

https://www.electrodragon.com/product/dc-dc-step-power-module-mp1584-fixed-output/

![Pic0](pics/stepdown.PNG)
(use the fixed-output version. The ones with variable output are unreliable! Tried it with no luck)

![Pic4](pics/4.jpg)

## More Pictures

![Pic1](pics/1.jpg)
(The trafficlight was delivered with a tiny microcontroller and driver transistors at the LED board)

![Pic2](pics/2.jpg)
(I've removed the microcontroller and connected the OrangePi Zero through flexible cables to the solder pads where the output pins of the removed microcontroller where)

![Pic3](pics/3.jpg)

![Pic6](pics/6.jpg)

![Pic7](pics/7.jpg)

![Pic8](pics/8.jpg)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4MzIwOTM4MzZdfQ==
-->