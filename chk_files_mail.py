#!/usr/bin/env python
# 
# Kijiji Search and Email Agent - Step III - Email Ads
#

import sqlite3
import datetime
import time
import os
import sys

WrkDir = "C:\\MailAlert"

	
# Change current directory to working directory
# On failure, the WrkDir variable is set to the current directory

if os.getcwd() != WrkDir:
	try:
		os.chdir(WrkDir)
	except:
		WrkDir = os.getcwd()

		
# delete all alert_*.html files

for filename in os.listdir('c:\\mailalert'):
	#print filename, filename[0:5], filename[-5:]
	if filename[0:6] == 'alert_':
		#print "*"
		if filename[-5:] == '.html':
			#print filename
			os.remove("c:\\mailalert\\" + filename)
			

		
# Confirm there is a search database

#cmd_sql_1 = "select mail_title, mail_to, cc_to, (select count(*) from results where results.search_id = searches.id and results.is_ok = 'Y') from searches where (select count(*) from results where results.search_id = searches.id and results.is_ok = 'Y')  > 0"
cmd_sql = "select * from (select mail_title, mail_to, cc_to, sum((select count(*) from results where search_id = searches.id and is_ok='Y')) as NumRecords from searches where active = 'Y' group by mail_title, mail_to, cc_to) as info where NumRecords > 0"
try:
	inSearch = sqlite3.connect('kijiji_searches.db3')
	cursor = inSearch.cursor()
	#sql = "select mail_title, mail_to, cc_to, results.id, results.out_text from searches inner join results on searches.id = results.search_id where results.is_ok = 'Y' order by mail_title, mail_to, searches.id, results.id"
	cursor.execute(cmd_sql)
	all_rows = cursor.fetchall()
	#all_emails = cursor.execute(cmd_sql_2)
	del cursor
	inSearch.close()
except:
	print 'database kijiji_searches must be created.'
	time.sleep(10)
	exit()

print str(len(all_rows)) + ' emails to be sent.\n'


# write the command file
cmd_out = ""
for row in all_rows:
	cmd_out = cmd_out + 'MailAlert -r "' + row[1] + '" '
	if row[2] is not None:
		if len(row[2]) > 9:
			cmd_out = cmd_out + '-u "' + row[2] + '" '
	cmd_out = cmd_out + '-s "' + row[0] + '" '
	cmd_out = cmd_out + '-b @alert_' + row[0].strip().replace(' ', '_') + '.html\n'
	cmd_out = cmd_out + 'chk_files_mailed_ok.py "' + row[0].strip() + '"\n'

c = open('mail_stuff.cmd', 'w')
c.write(cmd_out)
c.close()

for row in all_rows:
	
	fileTitle = 'alert_' + row[0].strip().replace(' ','_') + '.html'
	# make the details file
	sql = "select mail_title, mail_to, cc_to, results.id, results.out_text from searches inner join results on searches.id = results.search_id where results.is_ok = 'Y' and mail_title = '" + str(row[0]) + "' order by mail_title, mail_to, searches.id, results.id"
	inSearch = sqlite3.connect('kijiji_searches.db3')
	cursor = inSearch.cursor()
	cursor.execute(sql)
	q = cursor.fetchall()
	
	m = open(fileTitle, 'a')
	for a in q:
		m.write(str(a[4]).replace('</title>', ''))
		sql = 'update results set is_ok = "M" where id = ' + str(a[3])
		#cursor.execute(sql)
		#inSearch.commit()
	m.close()
	
	del cursor
	inSearch.close()
	

#curTitle = ''
#Cmds = []
#xCmd = ''
#mail_title = ''
#mail_to = ''
#cc_to = ''
#id = 0
#owt = ''

#for row in all_rows:
#	if (row == all_rows[0]):
#		curTitle = row[0]
#		mail_title = row[0]
#		mail_to = row[1]
#		cc_to = row[2]
#		id = row[3]
#		owt = row[4] + '\n\n'
#	if curTitle != row[0]:
#		if (curTitle != ''): 
#			xCmd = 'MailAlert -r ' + chr(34) + mail_to + chr(34) + ' ' 
#			if len(cc_to) > 0:
#				xCmd = xCmd + '-u ' + chr(34) + cc_to + chr(34) + ' '
#			xCmd = xCmd + '-s ' + chr(34) + mail_title + chr(34) + ' -b @alert_' + mail_title.replace(' ', '_') + '.html'
#			c = open('alert_' + mail_title.replace(' ', '_') + '.html', 'w')
#			print owt
#			c.write(owt)
#			c.close()
#			owt = ''
#			Cmds.append(xCmd)
#			
#			curTitle = row[0]
#			mail_title = row[0]
#			mail_to = row[1]
#			cc_to = row[2]
#			id = row[3]
#			owt = owt + row[4] + '\n\n'
#			
#		if (all_rows[-1:] == row):
#			xCmd = 'MailAlert -r ' + chr(34) + mail_to + chr(34) + ' ' 
#			if len(cc_to) > 0:
#				xCmd = xCmd + '-u ' + chr(34) + cc_to + chr(34) + ' '
#			xCmd = xCmd + '-s ' + chr(34) + mail_title + chr(34) + ' -b @alert_' + mail_title.replace(' ', '_') + '.html'
#			c = open('alert_' + mail_title.replace(' ', '_') + '.html', 'w')
#			print owt
#			c.write(owt)
#			c.close()
#			owt = ''
#			Cmds.append(xCmd)
#	else:
#		mail_title = row[0]
#		mail_to = row[1]
#		cc_to = row[2]
#		id = row[3]
#		owt = owt + row[4] +'\n\n'
#		
#c = open('mail_stuff.cmd', 'w')
#c.write('\n'.join(Cmds))
#c.close()
		