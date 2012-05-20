#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import sys

debug = True

if __name__=="__main__":

    # 引数
    opts = [sys.argv[1], sys.argv[2]]
    
    linenum=0

    x=[]
    y=[]

    yearstr=""
    monthstr=""

    graphtitle=""

    if opts[0]=="all": graphtitle=u"すべて"
    elif opts[0]=="shokuhi": graphtitle=u"食費"
    elif opts[0]=="gaishokuhi": graphtitle=u"外食費"

    for line in sys.stdin:
        if linenum == 0:
            linenum += 1
            continue
        items = line.split(",")
        if monthstr == "":
            yearstr = items[0][0:4]
            monthstr = items[0][5:7]
        timestamp = datetime.datetime.strptime(items[0],'%Y-%m-%d')
        cumcost = items[2]

        x.append(timestamp)
        y.append(cumcost)

        if debug:
            print line,
        linenum += 1

    # データをセット
    # for debug
    if debug:
        print x
        print y
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,opts[1])

    prop = fm.FontProperties(fname='/Users/kazuhiro/Library/Fonts/ipag00303/ipag.ttf')

    # グラフのフォーマットの設定
    days = mdates.DayLocator()  # every day
    daysFmt = mdates.DateFormatter('%d')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    ax.grid(True)
    size='18'
    plt.title(unicode(yearstr)+u"年"+unicode(monthstr)+u"月 "+graphtitle,size=size,fontproperties=prop)
    plt.xlabel(u"日付",size=size,fontproperties=prop)
    plt.ylabel(u"金額[円]",size=size,fontproperties=prop)
    fig.autofmt_xdate()

    # x軸（日付）表示範囲の設定
    xmin = datetime.datetime(year=int(yearstr),month=int(monthstr),day=1)
#    print monthstr # for debug
    # xmaxはの計算。対象の月の1ヶ月進めて１日引く。
    if monthstr == "12": # 12月のときの計算
        xmax = datetime.datetime(year=int(yearstr)+1,month=1,day=1)-datetime.timedelta(days=1)
    else: # 12月以外
        xmax = datetime.datetime(year=int(yearstr),month=int(monthstr)+1,day=1)-datetime.timedelta(days=1) # 対象の月の1ヶ月進めて１日引く。
        
#    xmax = datetime.datetime(year=int(yearstr),month=int(monthstr),day=1)-datetime.timedelta(days=1) # ??
    if debug:
        print xmin
        print xmax
    plt.xlim(xmin,xmax)

    # 保存
    outfile="kakeibo"+"-"+opts[0]+"-"+yearstr+"-"+monthstr+".png"
    print "saved: "+outfile
    plt.savefig(outfile)

    # 表示
#    plt.show()
