import requests
import json
import ipaddress
from init import *
import time

class AbuseDB:

    def getSpamStatus(self, ip, count = 0):
        response = requests.get('https://api.abuseipdb.com/api/v2/check?ipAddress=' + str(ipaddress.IPv4Address(ip)) + '&key=' + str(config['abusedb']['ApiKey']) + '&verbose&maxAgeInDays=30')
        if response.status_code == 200:
            data = None
            try:
                data = json.loads(response.content.decode())
            except:
                print (ip);
                print (response);
            data = json.loads(response.content.decode())
            reportnumber = data['data']['totalReports']

            # get category
            cate = []
            cate_str = ''

            if (str(type(data)) == "<class 'dict'>"):
                try:
                    for report in data['data']['reports']:
                        for cat in report['categories']:
                            cate.append(cat)
                    cate = unique(cate)
                    for c in cate:
                        cate_str = cate_str + ' - ' + categories[str(c)]
                            
                except:
                    cate_str = ''

            # return
            ipInfo = {}
            ipInfo['reportnumber'] = reportnumber
            ipInfo['cate_str'] = cate_str

            if (reportnumber >= 14):
                with open('badip.txt', 'a') as f:
                    f.write(str(ipaddress.IPv4Address(ip)) + '\n')
                    
            return ipInfo
        else:
            if count < 5:
                time.sleep(2)
            else:
                time.sleep(30)
            return self.getSpamStatus(ip, count + 1)
        