#!/usr/bin/python3
from geolite2 import geolite2
import colorama
from colorama import Fore, Back, Style
import time
from init import *
import databaseaccess
import AbuseDB

data = databaseaccess.DatabaseAccess()
abuse = AbuseDB.AbuseDB()

print ()
print ()
colorama.init()

line = int(config['alert']['ProcessLine'])
reader = geolite2.reader()

while(True):
    alert = data.getAlert(line)

    if (len(alert) > 0):
        ipInfo = abuse.getSpamStatus(alert['ip_src'])

        print (Fore.YELLOW + alert['sensor'] + " - " + alert['timestamp'] + '\t' + alert['ip_src'] + '\t' + alert['signature'] + Style.RESET_ALL)
        if (ipInfo['reportnumber'] > 0):
            print (Fore.RED + '\tMarked as abuse with ' + Fore.GREEN + str(ipInfo['reportnumber']) + Fore.RED + ' times in last 30 days.')
            print ('\tAbuse category: ' + ipInfo['cate_str'] + Style.RESET_ALL)

            if (ipInfo['reportnumber'] >= 10):
                with open('badip.txt', 'a') as f:
                    f.write(alert['ip_src'] + '\n')

        else:
            print (Fore.GREEN + '\tNot marked as abuse' + Style.RESET_ALL)

        location = reader.get(alert['ip_src'])
        try:
            print ('\tCountry: ' + location['country']['names']['en'] + ' - ' + location['city']['names']['en'])
        except Exception as e:
            try:
                print ('\tCountry: ' + location['country']['names']['en'])
            except Exception as e:
                print ('\tCannot get country name')
            

        print ()
        line += 1
    else:
        time.sleep(1)

    config['alert']['ProcessLine'] = str(line)
    saveConfig(config)