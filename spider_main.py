# -*- coding: utf-8 -*-
from configparser import ConfigParser
from urllib.parse import quote
import socket
import os
import math
import urllib.request
from bs4 import BeautifulSoup
import time
import spider_search_page
import spider_paper

if __name__ == '__main__':
    start = time.clock()
    cf = ConfigParser()
    cf.read("Config.conf", encoding='utf-8')
    keyword = cf.get('base', 'keyword')# 关键词
    maxpage = cf.getint('base', 'maxpage')# 最大页码
    searchlocation = cf.get('base', 'searchlocation') #搜索位置
    currentpage = cf.getint('base', 'currentpage')
    if os.path.exists('data-detail.txt') and currentpage == 0:
        print('存在输出文件，删除该文件')
        os.remove('data-detail.txt')

    #构造不同条件的关键词搜索
    values = {
           '全文': 'qw',
           '主题': 'theme',
           '篇名': 'title',
           '作者': 'author',
           '摘要':'abstract'
    }
    keywordval = str(values[searchlocation])+':'+str(keyword)
    index_url='http://search.cnki.com.cn/Search.aspx?q='+quote(keywordval)+'&rank=&cluster=&val=&p='#quote方法把汉字转换为encodeuri?
    print(index_url)

    #获取最大页数
    html = urllib.request.urlopen(index_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    pagesum_text = soup.find('span', class_='page-sum').get_text()
    maxpage = math.ceil(int(pagesum_text[7:-1]) / 15)
    #print(maxpage)
    cf = ConfigParser()
    cf.read("Config.conf", encoding='utf-8')
    cf.set('base', 'maxpage', str(maxpage))
    cf.write(open('Config.conf', 'w', encoding='utf-8'))

    for i in range(currentpage, maxpage):
        page_num=15
        page_str_num=i*page_num
        page_url=index_url+str(page_str_num)
        print(page_url)
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                spider_search_page.get_paper_url(page_url)
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
        cf.set('base', 'currentpage', str(i))
        cf.write(open("Config.conf", "w", encoding='utf-8'))
    spider_paper.spider_paper()# spider_paper补全文章信息
    end = time.clock()
    print ('Running time: %s Seconds'%(end-start))
