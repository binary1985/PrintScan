import ftplib



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ftpscan(host):

    user="anonymous"
    password="test@email.com"

    try:
        print "Trying to FTP to "+host
        ftp = ftplib.FTP(host,user,password,"",3)    
        #ftp.login(user,password)
    except Exception,e:
        print bcolors.FAIL + str(e) + bcolors.ENDC
    else:
        print bcolors.OKGREEN + str(host) + ":Anonymous FTP Enabled" + bcolors.ENDC
        return host
        #filelist = [] #to store all files
        #ftp.retrlines('LIST',filelist.append)    # append to list  
        #print filelist
