# -*- coding: utf-8 -*-
import socket

from bs4 import BeautifulSoup
import urllib
import requests
import time
import xlwt
from configparser import ConfigParser

def spider_paper():
    start = time.clock()
    # f=urllib2.urlopen(url, timeout=5).read()
    # soup=BeautifulSoup(html)
    # tags=soup.find_all('a')
    file = open("data-detail.txt", encoding='utf8')
    cf = ConfigParser()
    cf.read("Config.conf", encoding='utf-8')
    keyword = cf.get('base', 'keyword')# 关键词

# 写入Excel
    wb = xlwt.Workbook("data_out.xls")
    sheet = wb.add_sheet("data-out")
    sheet.write(0, 0, '下载网址')
    sheet.write(0, 1, '标题')
    sheet.write(0, 2, '来源')
    sheet.write(0, 3, '引用')
    sheet.write(0, 4, '作者')
    sheet.write(0, 5, '作者单位')
    sheet.write(0, 6, '关键词')
    sheet.write(0, 7, '摘要')
    sheet.write(0, 8, '共引文献')

    lines = file.readlines()
    txt_num = 1
    lin_num = 1
    paper_list = []
    for line in lines:
        object = line.split('\t')
        paper_url = object[0]
        if paper_url in paper_list:
            continue
        paper_list.append(paper_url)
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                html = urllib.request.urlopen(paper_url).read()
                soup = BeautifulSoup(html, 'html.parser')
                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
            except socket.error:
                attempts += 1
                print("第"+str(attempts)+"次重试！！")
                if attempts == 50:
                    break
            except urllib.error:
                attempts += 1
                print("第"+str(attempts)+"次重试！！")
                if attempts == 50:
                    break
        title = soup.find_all('div', style="text-align:center; width:740px; font-size: 28px;color: #0000a0; font-weight:bold; font-family:'宋体';")
        abstract = soup.find_all('div', style='text-align:left;word-break:break-all')
        author = soup.find_all('div', style='text-align:center; width:740px; height:30px;')

        #获取作者名字
        for item in author:
            author = item.get_text()
        # print(item)
        #获取摘要信息
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

        ifreferen = soup.find_all('td', class_='b14', rowspan='2')
        ref = ''
        for i in range(len(ifreferen)):
            if ('【共引文献】' in ifreferen[i].get_text()):
                referenceList = soup.find_all('div', id='div_Ref')  # 共引文献列表
                if len(referenceList) == 0:
                    referenceList = soup.find_all('div', class_='div_Ref')
                referenceList = referenceList[i]
                for tdref in referenceList.find_all('td', width='676'):
                    refitem = tdref.a.get("href")
                    refitem = refitem.strip()
                    print(refitem)
                    ref = ref + refitem + ' ,'
        # 获取作者单位，处理字符串匹配
        authorUnitScope = soup.find('div', style='text-align:left;', class_='xx_font')
        author_unit = ''
        author_unit_text = authorUnitScope.get_text()
        # print(author_unit_text)
        if '【作者单位】：' in author_unit_text:
            auindex = author_unit_text.find('【作者单位】：', 0)
        else:
            auindex = author_unit_text.find('【学位授予单位】：', 0)
        for k in range(auindex, len(author_unit_text)):
            if author_unit_text[k] == '\n' or author_unit_text[k] == '\t' or author_unit_text[k] == '\r' or \
                        author_unit_text[k] == '】':
                continue
            if author_unit_text[k] == ' ' and author_unit_text[k + 1] == ' ':
                continue
            if author_unit_text[k] != '【':
                author_unit = author_unit + author_unit_text[k]
            if author_unit_text[k] == '【' and k != auindex:
                break
        # 获取关键字
        key_word = ''
        kwindex = author_unit_text.find('【关键词】：', 0)
        for k in range(kwindex, len(author_unit_text)):
            if author_unit_text[k] == '\n' or author_unit_text[k] == '\t' or author_unit_text[k] == '\r' or \
                                author_unit_text[k] == '】':
                continue
            if author_unit_text[k] == ' ' and author_unit_text[k + 1] == ' ':
                continue
            if author_unit_text[k] != '【':
                key_word = key_word + author_unit_text[k]
            if author_unit_text[k] == '【' and k != kwindex:
                break
        # print(author_unit)
        # print(key_word)
        line = line.strip('\n')
        line = line + '\t' + str(author) + '\t' + str(author_unit) + '\t'+ str(key_word) + '\t'+ str(tstr) + '\t' + str(ref) + '\n'
        outstring = line.split('\t')
        for i in range(len(outstring)):
            sheet.write(lin_num, i, outstring[i])
        print('写入第'+str(lin_num)+'行')
        lin_num += 1
        wb.save('data_out_'+str(keyword)+'.xls')

    file.close()
    end = time.clock()
    print('Running time: %s Seconds' % (end - start))
