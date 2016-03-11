#!/usr/bin/python
#dangers of snmp - ips of connected devices-possibly network management tools or manual users-mac addresses-firmware
#pip install pysnmp - required

from pysnmp.entity.rfc3413.oneliner import cmdgen

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def snmpscan(host):

	cmdGen = cmdgen.CommandGenerator()

	errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
	    cmdgen.CommunityData('public'),
	    cmdgen.UdpTransportTarget((host, 161)),
	    '1.3.6.1.2.1.1.1.0',
	)

	# Check for errors and print out results
	if errorIndication:
	    print(errorIndication)
	else:
	    if errorStatus:
	        print('%s at %s' % (
	            errorStatus.prettyPrint(),
	            errorIndex and varBinds[int(errorIndex)-1] or '?'
	            )
	        )
	    else:
	    	print bcolors.OKGREEN + str(host) + ":Default SNMP Enabled" + bcolors.ENDC
	    	return host