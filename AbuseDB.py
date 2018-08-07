import requests
import json
from init import *

class AbuseDB:

    def getSpamStatus(self, ipaddress):
        response = requests.get('https://www.abuseipdb.com/check/' + str(ipaddress) + '/json?key=' + str(config['abusedb']['ApiKey']) + '&verbose&days=30')
        data = json.loads(response.content.decode())
        reportnumber = 0

        # get category
        cate = []
        cate_str = ''

        if (str(type(data)) == "<class 'dict'>"):
            reportnumber = 1

            for cat in data['category']:
                cate.append(cat)
            cate = unique(cate)
            for c in cate:
                cate_str = cate_str + ' ' + categories[str(c)]

        if (str(type(data)) == "<class 'list'>"):
            reportnumber = len (data)
            if (reportnumber > 0):
                for item in data:
                    for cat in item['category']:
                        cate.append(cat)
                cate = unique(cate)
                for c in cate:
                    cate_str = cate_str + ' - ' + categories[str(c)]

        # return
        ipInfo = {}
        ipInfo['reportnumber'] = reportnumber
        ipInfo['cate_str'] = cate_str

        return ipInfo

        