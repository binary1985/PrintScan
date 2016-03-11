#!/usr/bin/python
import urllib2
import ssl
import re
import time
import math
import requests
from bs4 import BeautifulSoup

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def retreiveusers(cleanip):
    users = []
    print "Trying Method 1 - " + cleanip + "/hp/device/JobLogReport/Index"
    #retreive /hp/device/JobLogReport/Index
    context = ssl._create_unverified_context()
    try:
        response = urllib2.urlopen(cleanip + "/hp/device/JobLogReport/Index", context=context, timeout = 20)
        html = response.read()
        #find JobLogUser in html
        for line in html.splitlines():
            #line = line.rstrip()
            if re.search ('JobLogUser', line):
                user = re.split(r'[<>]+',line)[2]
                users.append(user)
        #print usernames
        if users:
            users=sorted(set(users))
            #remove error when no username is present
            users[:] = (value for value in users if value != "/span")
            print "Identified " + str(len(users)) + " users on "+ cleanip
            return users

    except Exception,e: 
        print bcolors.FAIL + str(e) + bcolors.ENDC
        pass

    if not users:
        try:
            print "Trying Method 2 - " + cleanip + "/hp/device/this.LCDispatcher?nav=hp.ColorUsage - Method 1"
            context = ssl._create_unverified_context()
            url = cleanip+"/hp/device/this.LCDispatcher?nav=hp.ColorUsage"
            soup = BeautifulSoup(urllib2.urlopen(url, context=context, timeout = 20).read(), "html.parser")
            records = soup.find(id="Text6")
            records = int("{}".format(''.join(records).encode('utf-8')))
            for row in soup.findAll('span', {'class':'hpPageText'})[20::7]:
                users.append( "{}".format(''.join(row).encode('utf-8')))
            while records > 100:
                print "Processing Next Page..."
                url = cleanip+"/hp/device/this.LCDispatcher?nav=hp.ColorUsage"
                soup = BeautifulSoup(urllib2.urlopen(url, context=context, timeout = 20).read(), "html.parser")
                for row in soup.findAll('span', {'class':'hpPageText'})[20::7]:
                    users.append( "{}".format(''.join(row).encode('utf-8')))
                records=records-100
            if not users:
                print "No users found"
            else:
                users=sorted(set(users))
                #remove error when no username is present
                users[:] = (value for value in users if value != "/span")
                print "Identified " + str(len(users)) + " users on "+ cleanip

                return users
        except Exception,e: 
            print bcolors.FAIL + str(e) + bcolors.ENDC
            pass

    if users:
        users=sorted(set(users))
        #remove error when no username is present
        users[:] = (value for value in users if value != "/span")
        print "Identified " + str(len(users)) + " users on "+ cleanip
        users=sorted(set(users))
        return users

    if not users:
        try:
            print "Trying Method 3 - " + cleanip + "/hp/device/this.LCDispatcher?nav=hp.ColorUsage - Method 2"
           
            

            context = ssl._create_unverified_context()
            url = cleanip+"/hp/device/this.LCDispatcher?nav=hp.ColorUsage"
            soup = BeautifulSoup(urllib2.urlopen(url, context=context, timeout = 20).read(), "html.parser")

            data = []
            table = soup.find('table', attrs={'class':'hpTable'})
            table_body = table.find('tbody')

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values

            searchstring = "<td class=\"hpTableCell\"></td>"

            for entry in data[2::1]:
                if searchstring in str(entry):
                    continue
                #print entry[1]
                user = re.split(r'[<>]+',str(entry[1]))[3]
                users.append(user)
            users=sorted(set(users))
            print "Identified " + str(len(users)) + " users on "+ cleanip
            users=sorted(set(users))
            return users

        except Exception,e: 
            print bcolors.FAIL + str(e) + bcolors.ENDC
            pass
    return
