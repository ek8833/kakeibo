#!/usr/local/bin/python
# --encoding: utf-8

import sys
import re

def getRstData(infile):
	result2 = {} # key: 日付, value: 日付ごとの合計
	year, month, day = "", "", ""
	counter = 0
	for line in open(infile,'r'):
		line = line.strip()
		
		# 空行は読み飛ばす。
		if(not line): continue

		print "\n"
		
		# 日付行をみつける。
		m = re.search('# (\d{4})-(\d{1,2})-(\d{1,2})',line)
		# 日付行をみつけた場合
		if m:
			print line.strip(),
		# 日付行でない場合の処理
		else:
#			print " - "+line.strip(),
			print line.strip(),
	
if __name__=="__main__":
	infile = sys.argv[1]
#	print "infile: "+infile
	
	rstdata=getRstData(infile)
