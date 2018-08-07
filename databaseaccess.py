#!/usr/bin/python3
import mysql.connector
import ipaddress
from init import *


class DatabaseAccess:

	def __init__(self):
		self.checkDatabaseConnection()

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
				alert['ip_src'] = str(ipaddress.IPv4Address(ip_src))
			
			# get sensor name
			self.datacursor.execute('SELECT sid, hostname FROM `sensor` where sid = ' + str(event_sid))
			for (sid, hostname) in self.datacursor:
				alert['sensor'] = str(hostname)

		self.mydb.commit() # clear query cache
		return alert

	def checkDatabaseConnection(self):
		try:
			self.mydb = mysql.connector.connect(host=config['mysql']['ServerAddress'],
												user=config['mysql']['User'],
												passwd=config['mysql']['Password'],
												database=config['mysql']['Database'])
			print("Connection to database success.")
			self.datacursor = self.mydb.cursor()
		except mysql.connector.Error as e:
			print(format(e))
			exit()