import os
# import telnetlib
import sys
import socket
from easysnmp import *  # Python2 only
import netifaces
# import backend-connection-tests

# This will perform a platform agnostic ping to the address
# The output will be hidden
# A successful repsonse  is '0'
# https://stackoverflow.com/questions/2953462/pinging-servers-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qahttps://stackoverflow.com/questions/2953462/pinging-servers-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
hostname = str("10.3.3.254")
response = os.system("ping -c 1 " + hostname+"  > /dev/null 2>&1")
if response == 0:
    print (hostname + ' is up! [ping]')
else:
    print (hostname + ' is down! [ping]')

# Now want to test SSH connection, both the port and getting an SSH prompt
# tn = telnetlib.Telnet(str(hostname), "10443", 5)
# tn.read_until()
# tn.write("\r")
# tn.read_eager()
# tn.write(str("quit" + "\n"))
# output = tn.read_all()
# print (output)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('10.3.3.254', 22))
if result == 0:
    print ("Port 22  is open [Socket]")
else:
    print ("Port 22 is closed [Socket]")

result = sock.connect_ex(('10.3.3.254', 23))
if result == 0:
    print ("Port 23  is open [Socket]")
else:
    print ("Port 23 is closed [Socket]")


# http://easysnmp.readthedocs.io/en/latest/
# Create an SNMP session to be used for all our requests
session = Session(hostname='10.3.3.254', community='fc360collector', version=2)

# You may retrieve an individual OID using an SNMP GET
location = session.get(('sysContact', '0'))
device_version = session.get(('1.3.6.1.4.1.12356.101.4.1.1', '0'))

# print (device_version)
# print (type(device_version))
print (device_version.value)
# https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
if "5.6" in device_version.value:
    print (" 5.6 code")
    device_cpu = session.get(('1.3.6.1.4.1.12356.101.4.1.3', '0'))
    device_memory_used = session.get(('1.3.6.1.4.1.12356.101.4.1.4', '0'))
    print (device_memory_used.value + "memory used")
    if int(device_memory_used.value) > 20:
        print ("reboot the box")
print (type(device_memory_used))
print (device_memory_used)

# print (dir(location))
print ("The person to contact is " + str(location.value) + "[SNMP]")

# https://pypi.python.org/pypi/netifaces
gws = netifaces.gateways()
gws_add = (gws['default'][netifaces.AF_INET][0])
# print (gws['default'][netifaces.AF_INET][0])
gws_test_ping = os.system("ping -c 1 " + gws_add+"  > /dev/null 2>&1")
if gws_test_ping == 0:
    print ('Default gateway at ' + gws_add + ' is up! [ping]')
else:
    print ('Default gateway at ' + gws_add + hostname, ' is down! [ping]')
