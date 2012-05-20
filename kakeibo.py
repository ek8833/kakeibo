#!/usr/local/bin/python
# --encoding: utf-8

import sys
import re
import codecs
import datetime
from dateutil.relativedelta import relativedelta

def loadEvernoteData(infile,mode=0): # 0: ALl, 1: shokuhi, 2: gaishokuhi
	if mode==0:
		result,result2,logline=loadAllData(infile)
		return result2,logline
	elif mode==1:
		print "Load Shokuhi Data"
		result=loadFilteredData(infile,u"食費")
		return result
	elif mode==2:
		print "Load Gaishokuhi Data"
		result=loadFilteredData(infile,u"外食費")
		return result
	else:
		print "Error Mode: "+mode

def loadFilteredData(infile,keyword=u""):
	print "loadFilteredData"
	result2 = {} # key: 日付, value: 日付ごとの合計
	year, month, day = "", "", ""
	counter = 0
	for line in open(infile,'r'):
		line = line.strip()
		
		# 空行は読み飛ばす。
		if(not line): continue
		
		# 日付行をみつける。
		m = re.search('# (\d{4})-(\d{1,2})-(\d{1,2})',line)
		# 日付をみつけたら代入する。
		if m:
			year = unicode(m.group(1))
			month = unicode(m.group(2))
			day = unicode(m.group(3))
			d=datetime.datetime(int(year),int(month),int(day))
#			print line, m.group(1), m.group(2), m.group(3)
		# 日付行でない場合の処理。
		else:
#			print year+"-"+month+"-"+day,
#			print line
			# 分割 -> かかったお金, 分類, 備考
			items = line.split(",")
#			print "items: ", items
			cost = unicode(items[0])
#			print cost
			# "+1000"などの表記はINなのでとばす。
			mm = re.match('\+',cost)
			if mm: continue
			
			category = unicode(items[1],'utf-8')
#			if not category==u"食費":
			if not category==keyword: # キーワードにマッチしていなかったらとばす
				continue
#			print "category: "+category
#			print "match!"
			
			# 備考がない場合は空文字列とする。
			if(len(items) <= 2):
				representation = ""
			else:
				representation = items[2]

#			print "representation: "+representation
			# 出力文字列を設定
			outline = year+u"-"+month+u"-"+day+u", "+unicode(line,'utf-8')
			
			keyOfDay = d # d: datetime形式
			result2[keyOfDay] = result2.setdefault(keyOfDay,0) + int(cost)
#			print outline
		counter+=1
		
	return result2
	

def loadAllData(infile):
	print "loadAllData"
	result = {}
	result2 = {} # key: 日付, value: 日付ごとの合計
	year, month, day = "", "", ""
	counter = 0
	logline = [] # for log
	for line in open(infile,'r'):
		line = line.strip()
		
		# 空行は読み飛ばす。
		if(not line): continue
		
		# 日付行をみつける。
		m = re.search('# (\d{4})-(\d{1,2})-(\d{1,2})',line)
		# 日付をみつけたら代入する。
		if m:
			year = unicode(m.group(1))
			month = unicode(m.group(2))
			day = unicode(m.group(3))
			d=datetime.datetime(int(year),int(month),int(day))
#			print line, m.group(1), m.group(2), m.group(3)
		# 日付行でない場合の処理。
		else:
#			print year+"-"+month+"-"+day,
#			print line
			# 分割 -> かかったお金, 分類, 備考
			items = line.split(",")
#			print items
			cost = unicode(items[0])
			print cost
			# "+1000"などの表記はINなのでとばす。
			mm = re.match('\+',cost)
			if mm: continue
			
			category = items[1]
			
			# 備考がない場合は空文字列とする。
			if(len(items) <= 2):
				representation = ""
			else:
				representation = items[2]
			
			# 出力文字列を設定	
#			outline = year+u"-"+month+u"-"+day+u", "+u", ".join(items)
#			outline = year+u"-"+month+u"-"+day+u", "+u", ".join(items)
#			outline = year+u"-"+month+u"-"+day+u", "+unicode(line,'utf-8')
#			outline = unicode(year)+u"-"+unicode(month)+u"-"+unicode(day)+u", "+unicode(line,'mbcs')
		#	outline = year+u"-"+month+u"-"+day+u", "+unicode(line,'mbcs')
			outline = year+u"-"+month+u"-"+day+u", "+unicode(line,'utf-8')
			
			result[counter] = outline
			#keyOfDay = unicode(d.strftime("%Y-%m-%d"))
			keyOfDay = d # d: datetime形式
#			result2[year+u"-"+month+u"-"+day] = result2.setdefault(year+u"-"+month+u"-"+day,0) + int(cost)
			result2[keyOfDay] = result2.setdefault(keyOfDay,0) + int(cost)
			print outline
			logline.append(outline)
		counter+=1
		
	return result,result2,logline

def outputData(infile):
#	data,data2 = loadEvernoteData(infile)
	data,data2=loadAllData(infile)
#	print data
	f = codecs.open('result.csv','w+','utf-8')
	f.write(u"日付,金額,分類,備考\n")
	if f:
		for key, value in data.items():
			f.write(value+u"\n")

	f = codecs.open('result2.csv','w+','utf-8')
	f.write(u"日付,金額,累積\n")
	cum=0
	if f:
		for key in sorted(data2.keys()):
			cum=cum+data2[key]
#			f.write(key+u","+unicode(str(data2[key]),'utf-8')+u","+unicode(str(cum),'utf-8')+u"\n")
			f.write(unicode(key.strftime("%Y-%m-%d"),'utf-8')+u","+unicode(str(data2[key]),'utf-8')+u","+unicode(str(cum),'utf-8')+u"\n")

	f = codecs.open('result3.csv','w+','utf-8')
	f.write(u"日付,金額,累積\n")
	cum=0
	if f:
		start=sorted(data2.keys())[0]
		end=sorted(data2.keys(),reverse=True)[0] + datetime.timedelta(days=1)
		key=start
		while not key==end:
			cum=cum+data2.setdefault(key,0)
			#f.write(key+u","+unicode(str(data2[key]),'utf-8')+u","+unicode(str(cum),'utf-8')+u"\n")
			#print key
			f.write(unicode(key.strftime("%Y-%m-%d"),'utf-8')+u","+unicode(str(data2.setdefault(key,0)),'utf-8')+u","+unicode(str(cum),'utf-8')+u"\n")
			key=key+datetime.timedelta(days=1)

def outputData(data,outfileName):
	f = codecs.open(outfileName,'w+','utf-8')
	f.write(u"日付,金額,累積\n")
	cum=0
	if f:
		start=sorted(data.keys())[0]
		end=sorted(data.keys(),reverse=True)[0] + datetime.timedelta(days=1)
		key=start
		while not key==end:
			cum=cum+data.setdefault(key,0)
			f.write(unicode(key.strftime("%Y-%m-%d"),'utf-8')+u","+unicode(str(data.setdefault(key,0)),'utf-8')+u","+unicode(str(cum),'utf-8')+u"\n")
			key=key+datetime.timedelta(days=1)
	print "output: "+outfileName
	
def drawGraph():
	pass

def outputLogData(data,fileName):
	print "outputLogData"
	f = codecs.open(fileName,'w+','utf-8')
	f.write(u"日付,金額,分類,詳細\n")
	print data
	for item in data:
		f.write(unicode(item))
		f.write("\n")
	print "wrote: ", fileName
	
	
if __name__=="__main__":
	infile = sys.argv[1]
	print "infile: "+infile
	
#	outputData(infile)

	all_data,logline=loadEvernoteData(infile,mode=0) # All
	outputLogData(logline,"log.txt")
	outputData(all_data,"all.csv")
	
	shokuhi_data=loadEvernoteData(infile,mode=1) # shokuhi
	outputData(shokuhi_data,"shokuhi.csv")

	gaishokuhi_data=loadEvernoteData(infile,mode=2) # gaishokuhi
	outputData(gaishokuhi_data,"gaishokuhi.csv")
	
