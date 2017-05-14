# -*- coding: utf-8 -*-
import socket

from bs4 import BeautifulSoup
import urllib
import time
import xlwt

def spider_paper():
    start = time.clock()
    # f=urllib2.urlopen(url, timeout=5).read()
    # soup=BeautifulSoup(html)
    # tags=soup.find_all('a')
    file = open("data-detail.txt", encoding='utf8')

# 写入Excel
    wb = xlwt.Workbook("data_out.xls")
    sheet = wb.add_sheet("data-out")
    sheet.write(0, 0, '下载网址')
    sheet.write(0, 1, '标题')
    sheet.write(0, 2, '来源')
    sheet.write(0, 3, '引用')
    sheet.write(0, 4, '作者')
    sheet.write(0, 5, '摘要')
    sheet.write(0, 6, '参考文献')

    lines = file.readlines()
    txt_num = 1
    lin_num = 1
    for line in lines:
        object = line.split('\t')
        # file_name = './data/out_' + str(txt_num) + '.txt'
        file_name = './data/out.txt'
        paper_url = object[0]
        attempts = 0
        success = False
        while attempts < 20 and not success:
            try:
                html = urllib.request.urlopen(paper_url).read()
                soup = BeautifulSoup(html, 'html.parser')
                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
            except:
                attempts += 1
                print("第"+str(attempts)+"次重试！！")
                if attempts == 10:
                    break

        title = soup.find_all('div', style="text-align:center; width:740px; font-size: 28px;color: #0000a0; font-weight:bold; font-family:'宋体';")
        abstract = soup.find_all('div', style="text-align:left;word-break:break-all")
        author = soup.findAll('div', style='text-align:center; width:740px; height:30px;')
        for item in author:
            author = item.get_text()
        # print(item)
        #fuck = open(file_name, 'a', encoding='utf-8')
        tmp = ''
        for thing in abstract:
            a = thing.strings
            for string in a:
                tmp = tmp + string
            txt_num += 1
        result = tmp.split(' ')
        tstr = ''
        for t in result:
            test = t.split('\n')
            # print(test)
            if test != '\t' and test != '\n' and test != '\r' and test != '':
                for i in test:
                    if len(i) > 1:
                        item = i.split('\r')
                        for j in item:
                            object = j.split('\t')
                            for k in object:
                                tstr += k

        #参考文献
        ifreferen = soup.find_all('td', class_='b14', rowspan='2')
        ref = ''
        for i in range(len(ifreferen)):
            if ('【参考文献】' in ifreferen[i].get_text()):
                referenceList = soup.find_all('div', id='div_Ref')  # 参考文献列表
                if len(referenceList) == 0:
                    referenceList = soup.find_all('div', class_='div_Ref')
                referenceList = referenceList[i]
                for tdref in referenceList.find_all('td', width='676'):
                    # refitem = tdref.findAll('a', target="_blank")
                    refitem = tdref.a.get("href")
                    refitem = refitem.strip()
                    #print(refitem)
                    ref = ref + refitem + ' ,'

        line = line.strip('\n')
        line = line + '\t' + str(author) + '\t' + str(tstr) + '\t' + str(ref) + '\n'
        #print(line)
        outstring = line.split('\t')
        for i in range(len(outstring)):
            sheet.write(lin_num, i, outstring[i])
        print('写入第'+str(lin_num)+'行')
        lin_num += 1
        wb.save('data_out.xls')
        #fuck.write(line)
        #fuck.close()
    file.close()
    end = time.clock()
    print('Running time: %s Seconds' % (end - start))
