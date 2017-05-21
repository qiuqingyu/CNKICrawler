from bs4 import BeautifulSoup
import urllib
import urllib.request
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

page_num=15

def get_paper_url(page_url):
    html = urllib.request.urlopen(page_url).read()
    soup = BeautifulSoup(html,'html.parser')

    f = open('data-detail.txt','a+', encoding='utf-8')
    all = soup.find_all('div', class_='wz_content')
    for string in all:
        item = string.find('a', target='_blank')#文章标题与链接
        href = item.get('href')# 获取文章url
        title = item.get_text() # 获取文章标题
        year_count = string.find('span', class_='year-count')#获取文章出处与引用次数
        #year_count = year_count.get_text()
        publish = ''
        reference = ''
        for item in year_count:
            item = item.string
            item = item.replace('\n','')
            item = item.replace('\r', '')
            if '被引次数' in item:
                reference = item# 获取被引次数
            elif '年' in item: # 获取文章出处
                publish = item
            #print(publish)
            #print(reference)
        #print(year_count)
        f.write(href + '\t' + title + '\t' + publish + '\t' + reference +'\n')
    f.close()
