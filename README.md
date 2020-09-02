# cmk_livestatus_trafficlight
Trafficlight-style status display for CheckMK monitoring solution

# Platform
Linux board with i/o ports and LAN interface as platform

http://www.orangepi.org/orangepizero/


# Enable Livestatus
Enable Livestatus API access from network:

omd stop;omd config set LIVESTATUS_TCP on;omd config set LIVESTATUS_TCP_ONLY_FROM '172.18.1.91';omd start
