#!/usr/bin/python3
import mysql.connector
import ipaddress
from datetime import datetime
from init import *
import AbuseDB

class DatabaseAccess:
    abuse = AbuseDB.AbuseDB()

    def __init__(self):
        self.checkDatabaseConnection()
        self.createIPTable()

    def getAlert(self, line):
        alert = {}

        # get ipaddress_ID, signature_ID and time
        self.datacursor.execute('SELECT * FROM `event` ORDER BY `timestamp` ASC LIMIT ' + str(line - 1) + ' , 1');
        for (event_sid, event_cid, event_signature, event_timestamp) in self.datacursor:
            alert['timestamp'] = str(event_timestamp)

            # get signature name
            self.datacursor.execute('SELECT sig_id, sig_name, sig_class_id FROM `signature` WHERE sig_id = ' + str(event_signature))
            for (sig_id, sig_name, sig_class_id) in self.datacursor:
                alert['signature'] = sig_name

            # get source IP address
            self.datacursor.execute('SELECT cid, ip_src, ip_dst FROM `iphdr` where cid = ' + str(event_cid))
            for (cid, ip_src, ip_dst) in self.datacursor:
                alert['ip_src'] = int(ip_src)
            
            # get sensor name
            self.datacursor.execute('SELECT sid, hostname FROM `sensor` where sid = ' + str(event_sid))
            for (sid, hostname) in self.datacursor:
                alert['sensor'] = str(hostname)

        self.mydb.commit() # clear query cache
        return alert

    def getIPInfo(self, ip):
        self.datacursor.execute('SELECT * FROM `ipinfo` WHERE `IPAddress` = ' + str(ip))

        if (self.datacursor.rowcount <= 0):
            info = self.abuse.getSpamStatus(ip)
            self.datacursor.execute("INSERT INTO `ipinfo`(`IPAddress`, `lastcheck`, `reports`, `categories`) VALUES ({},'{}',{},'{}')".format(str(ip), datetime.now(), info['reportnumber'], info['cate_str']))

            return info
        else:
            for (ipadd, lastcheck, reports, categories) in self.datacursor:
                current_date = datetime.now()
                diff = current_date - lastcheck
                if (diff.days < 5):
                	# if info was updated in a month
                    ipInfo = {}
                    ipInfo['reportnumber'] = reports
                    ipInfo['cate_str'] = categories

                    return ipInfo
                else:
                	info = self.abuse.getSpamStatus(ip)
                	self.mydb.commit()
                	self.datacursor.execute("UPDATE `ipinfo` SET `lastcheck`='{}',`reports`={},`categories`='{}' WHERE `IPAddress` = {}".format(datetime.now(), info['reportnumber'], info['cate_str'], str(ip)))
                	
                	return info


    def checkDatabaseConnection(self):
        try:
            self.mydb = mysql.connector.connect(host=config['mysql']['ServerAddress'],
                                                user=config['mysql']['User'],
                                                passwd=config['mysql']['Password'],
                                                database=config['mysql']['Database'])
            print("Connection to database success.")
            self.datacursor = self.mydb.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(format(e))
            exit()

    def createIPTable(self):
        self.datacursor.execute('CREATE TABLE IF NOT EXISTS `suricata`.`ipinfo` ( `IPAddress` BIGINT NOT NULL , `lastcheck` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `reports` INT NOT NULL , `categories` TEXT NULL DEFAULT NULL , PRIMARY KEY (`IPAddress`)) ENGINE = InnoDB;')