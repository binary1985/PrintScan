#!/usr/bin/python
#requires beautifulsoup4 and pip install pysnmp - required
import urllib2, ssl, re, sys, csv, os, extractusers, snmpscan, ftpscan

os.system('clear')


if len(sys.argv) < 2:
    print "Usage is: " +sys.argv[0]+" <input printer ip file>"
    sys.exit()

vulnuserenum=[]
vulnsnmp=[]
vulnanonftp=[]

#color codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Test for Weak FTP Credentials

with open(sys.argv[1]) as f:
    for line in f:
        vulnerable=""
        cleanip = line.rstrip('\r\n')
        try:
            vulnerable = ftpscan.ftpscan(cleanip)
        except:
            print "Unable to Process FTP Login Request for "+cleanip
        if vulnerable:
            vulnanonftp.append(cleanip)
f.close()

#Test for Default SNMP Credentials

with open(sys.argv[1]) as f:
    for line in f:
        vulnerable=""
        cleanip = line.rstrip('\r\n')
        try:
            vulnerable = snmpscan.snmpscan(cleanip)
        except:
            print "Unable to Process SNMP Request for "+cleanip
        if vulnerable:
            vulnsnmp.append(cleanip)
f.close()




html =""
allusers = []
#open and clean ip from file
print "Harvesting Usernames"
with open(sys.argv[1]) as f:
    for line in f:
        print "----------------------------------------------------------------------------------------------------"
        cleanip = line.rstrip('\r\n')
        print "Identifying " + cleanip

        #test for HTTP or HTTPS
        #retrieve html via HTTPS -Default
        context = ssl._create_unverified_context()
        try:
            response = urllib2.urlopen("https://"+cleanip, context=context, timeout = 3)
            html = response.read()
        except Exception,e: 
            pass

        if html:
            print "Identified HTTPS"
            cleanip="https://"+cleanip
        #if html is empty, try HTTP
        if not html:
            try:
                response = urllib2.urlopen("http://"+cleanip, context=context, timeout = 3)
            except Exception,e: 
                print bcolors.FAIL + "Unable to connect to HTTP or HTTPS" + bcolors.ENDC
                continue

            html = response.read()
            if html:
                print "Identified HTTP"
                cleanip="http://"+cleanip

        if not html:
            print "Unable to connect to:" +cleanip
            continue
        users = extractusers.retreiveusers(cleanip)

        
        if users:
            vulnuserenum.append(cleanip)
            allusers = allusers + users

allusers=sorted(set(allusers))
#remove error when no username is present
allusers[:] = (value for value in allusers if value != "/span")

f=open('enumerated-users.txt','w')
for username in allusers:
    f.write(username+'\n')
f.close

#Print Vulnerability Results
print "Vulnerabilities Found:"
print "FTP:"
print vulnanonftp
print
print "SNMP:"
print vulnsnmp
print 
print "User Enum:"
print vulnuserenum
print "See enumerated users in enumerated-users.txt"
