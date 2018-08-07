#!/usr/bin/python3
# This file contains some functions and anything about config

import configparser
import os

def unique(list1):
	# insert the list to the set
	list_set = set(list1)
	# convert the set to the list
	return list(list_set)

def readConfig():
	configreader = configparser.ConfigParser()
	configreader.read('config.ini')
	return configreader

def writeConfig():
	configwriter = configparser.ConfigParser()

	configwriter['mysql'] = { 	'ServerAddress': '127.0.0.1', 
								'User': 'suricata',
								'Password': 'password',
								'Database': 'suricata'}	
	configwriter['alert'] = {	'ProcessLine': '0'	}
	configwriter['abusedb'] = {	'ApiKey': 'put_your_api_key_here'}
	saveConfig(configwriter);

	print("Write new config successful. Please edit config.ini file and restart program.")
	exit()

def saveConfig(newconfig):
	with open('config.ini', 'w') as configfile:
		newconfig.write(configfile)

def verifyConfig():
	print ("Reading config.")
	configverify = readConfig()

	if ('mysql' not in configverify):
		writeConfig()
	elif ('ServerAddress' not in configverify['mysql']):
		print("ServerAddress value is empty.")
	elif ('User' not in configverify['mysql']):
		print("User value is empty.")
	elif ('Password' not in configverify['mysql']):
		print("Password value is empty.")
	elif ('Database' not in configverify['mysql']):
		print("Database value is empty.")
	elif ('alert' not in configverify):
		writeConfig()
	elif ('ProcessLine' not in configverify['alert']):
		print("ProcessLine value is empty.")
	elif ('abusedb' not in configverify):
		writeConfig()
	elif ('ApiKey' not in configverify['abusedb']):
		print("ApiKey value is empty.")
	else:
		print ("Read config success.")
		return configverify
	
	writeConfig() #write default config
	exit()	# quit if anything wrong

# clear screen
os.system('cls' if os.name=='nt' else 'clear')
config = verifyConfig()


categories = {}
categories['3'] = 'Fraud Orders'
categories['4'] = 'DDoS Attack'
categories['5'] = 'FTP Brute-Force'
categories['6'] = 'Ping of Death'
categories['7'] = 'Phishing'
categories['8'] = 'Fraud VoIP'
categories['9'] = 'Open Proxy'
categories['10'] = 'Web Spam'
categories['11'] = 'Email Spam'
categories['12'] = 'Blog Spam'
categories['13'] = 'VPN IP'
categories['14'] = 'Port Scan'
categories['15'] = 'Hacking'
categories['16'] = 'SQL Injection'
categories['17'] = 'Spoofing'
categories['18'] = 'Brute-Force'
categories['19'] = 'Bad Web Bot'
categories['20'] = 'Exploited Host'
categories['21'] = 'Web App Attack'
categories['22'] = 'SSH'
categories['23'] = 'IoT Targeted'