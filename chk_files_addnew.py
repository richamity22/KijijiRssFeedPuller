#!/usr/bin/env python
# 
# Kijiji Search and Email Agent
#

import sqlite3
import datetime
import time
import os
import sys


def getPageData (addr):
	import requests
	print('\n ** opening [' + addr + '] **\n')
	try:
		response = requests.get(addr)
		data = response.text
		haram = data.replace('&amp;', '&')
		haram = haram.replace('&apos;', "'")
		haram = haram.replace('&quot;', chr(34))
		haram = haram.replace('&#8230;', ' ... ')
		haram = haram.replace('&#233;', 'e')
		haram = haram.replace('&#232;', 'e')
		haram = haram.replace('&#200;', 'E')
		data = haram.replace('&#201;', 'E')
		m = data.split('<item>')
		m.pop(0)
	except:
		m = '..............Failed..............'
	return(m)

def putResultData (	search_id, http_addr, out_text, is_ok):
	import sqlite3
	outResults = sqlite3.connect('kijiji_searches.db3')
	cursor = outResults.cursor()
	try:
		cursor.execute('''INSERT INTO results(search_id, http_addr, out_text, is_ok) VALUES(?,?,?,?)''', (search_id, http_addr, out_text, is_ok))
		outResults.commit()
	except:
		added = 0
		print("Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
		#print('*** failed to add record ***')
	else:
		added = 1
		print('record added successfully')
	del cursor
	outResults.close()
	#fixWeirdChars()
	return added

def updateSearchTime(id, xTime):
	import sqlite3
	back = True	
	outSearches = sqlite3.connect('kijiji_searches.db3')
	cursor = outSearches.cursor()
	try:
		sql = "UPDATE searches SET last_search = '" + xTime + "' where id = " + str(id) 
		cursor.execute(sql)
		outSearches.commit()
	except:
		print("Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
		print(sql)
		back = False
	del cursor
	outSearches.close()
	return back

def fixWeirdChars():
	import sqlite3
	fixFile = sqlite3.connect('kijiji_searches.db3')
	cursor = fixFile.cursor()
	try:
		m = open('c:/MailAlert/chk_files_sql.sql','r')
		updSQL = m.readlines()
		m.close()
		
		for line in updSQL:
			try:
				cursor.execute(line)
				fixFile.commit()
			except:
				pass
		
	except:
		pass
	del cursor
	fixFile.close()
	
WrkDir = "C:\\MailAlert"

	
# Change current directory to working directory
# On failure, the WrkDir variable is set to the current directory

if os.getcwd() != WrkDir:
	try:
		os.chdir(WrkDir)
	except:
		WrkDir = os.getcwd()

# Confirm there is a search database
		
try:
	inSearch = sqlite3.connect('kijiji_searches.db3')
	cursor = inSearch.cursor()
	cursor.execute('''select * from searches where active = "Y"''')
	all_rows = cursor.fetchall()
	del cursor
	inSearch.close()
except:
	print('database kijiji_searches must be created.')
	time.sleep(10)
	exit()

#	Execute the searches that were loaded 
num_added = 0
	
for row in all_rows:
		recID = row[0]
		http_addr = row[1]
		mail_title = row[2]
		mail_to = row[3]
		cc_to = row[4]
		last_search = row[5] 
		active = row[6]
		lastDateu = datetime.datetime.utcnow()
		lastDatel = datetime.datetime.now() - datetime.timedelta(hours=1)
		dateDiff = lastDateu - lastDatel
		timeZone_hrs = round(dateDiff.total_seconds() / 3600, 0)
		if type(last_search) != "str":
			lastSearch = datetime.datetime.utcnow() - datetime.timedelta(hours = 1)
			last_search = datetime.datetime.strftime(lastSearch, '%Y-%m-%dT%H:%M:%SZ')
		else:
			lastSearch = datetime.datetime.strptime(last_search, '%Y-%m-%dT%H:%M:%SZ')
		
		searchTime_hrs = (lastDateu - lastSearch).total_seconds() // 3600
		
		# abort if searched within the last hour
		
		if searchTime_hrs >= 1:
			
			lines = getPageData(http_addr)
			print(str(len(lines)) + ' lines of data to process ...\n')
			
			if len(lines) != 34:
				for line in lines:
					iStart = line.find('<title>') + len('<title>')
					print(iStart)
					title = line[iStart:iStart + line.find('</title>')]
					print(title)
					iStart = line.find('<link>') + len('<link>')
					link = line[iStart:line.find('</link>')]
					iStart = line.find('<pubDate>') + len('<pubDate>     ')
					sDate = line[iStart:line.find('</pubDate>')-4]
					ad_date = datetime.datetime.strptime(sDate, '%d %b %Y %H:%M:%S')
					uDate = datetime.datetime.strftime(ad_date, '%Y-%m-%dT%H:%M:%SZ')
					iStart = line.find('<description>') + len('<description>')
					descr = line[iStart:line.find('</description>')]
					is_ok = 'Y'
					
					if line.find('<g-core:price>') < 0:
						price = "0"
					else:
						iStart = line.find('<g-core:price>') + len('<g-core:price>')
						price = line[iStart:line.find('</g-core:price>')]
					
					if uDate >= last_search:
						out_txt = ['Kijiji Alerts']
						out_txt.append( 'Site: ' + http_addr)
						#out_txt.append(' ')
						c = link[21:]
						c = c[c.find('/') + 1:]
						c = c[0:c.find('/')]
						out_txt.append(c)
						out_txt.append(' ')
						out_txt.append('Item')
						out_txt.append('==============================================================================')
						out_txt.append(title)
						out_txt.append(link) 
						out_txt.append(descr) 
						out_txt.append(' ')
						d1 = ad_date - datetime.timedelta(hours = timeZone_hrs)
						out_txt.append(datetime.datetime.strftime(d1, '%I:%M %p') + '                        ' + '$ ' + str(float(price)))
						out_txt.append(' ')
						out_txt.append(' ')
						num_added = num_added + putResultData(recID, link, '\n'.join(out_txt), is_ok)
						
						if updateSearchTime(recID, last_search) == False:
							print('Error updating the last_search field\n\n')
						
					#print(str(num_added) + ' records added.')
					
fixWeirdChars()
