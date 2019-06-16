#!/usr/bin/env python
# 
# Kijiji Search and Email Agent - Step II - Exclusions application
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

# Confirm there is a search database
		
try:
	inSearch = sqlite3.connect('kijiji_searches.db3')
	cursor = inSearch.cursor()
	sql = "select results.*, exclusions.phrase from results left join exclusions on results.search_id = exclusions.search_id where results.is_ok = 'Y' and exclusions.phrase > ''"
	cursor.execute(sql)
	all_rows = cursor.fetchall()
	del cursor
	inSearch.close()
except:
	print('database kijiji_searches must be created.')
	time.sleep(10)
	exit()

print(str(len(all_rows)) + ' records to be evaluated for this filter.\n')

for row in all_rows:
	rowID = row[0]
	searchID = row[1]
	searchText = row[3].lower()
	searchExclude = row[5].lower()
	
	terms = searchExclude.strip().split(' ')
	
	base = 0
	OK = True
	
	#print('Examining : ' + searchText
	#print('\n'
	
	print('Excluding : ' + ', '.join(terms))
	print('\n')
	
	
	base = 0
	x = []
	for term in terms:
		q = searchText[base:].find(term)
		#if base > 0:
		#	if searchText[base:base+q].find('.') >=0:
		#		q = -1
		x.append(q - len(term) + 1)
		if (searchText[base:].find(term)) > 0:
			base = base + q
	
	bad = True
	
	if x[0] < 0:
		bad = False
	
	x.pop(0)
	for xTerm in x:
		if xTerm < 0:
			bad = False
		if xTerm > 10:
			bad = False
	
	if bad == True:
		#print('*** suspending this record for filter violations ***'
		OK = False
	
	if OK == False:
		out = sqlite3.connect('kijiji_searches.db3')
		cur = out.cursor()
		sql = "update results set is_ok = 'X' where id = " + str(int(float(rowID)))
		try:
			cur.execute(sql)
			out.commit()
		except:
			print("Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1])
			print(sql)
		del cur
		out.close()
		
# Clean up the out_text field

m = open('chk_files_sql.sql', 'r')
all_sql = m.read().split('\n')
m.close()

inSearch = sqlite3.connect(WrkDir+'/kijiji_searches.db3')
cursor = inSearch.cursor()

for sql in all_sql:
	cursor.execute(sql)
	inSearch.commit()

del cursor
del inSearch

