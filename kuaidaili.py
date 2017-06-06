#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup as bs
import time

def proxy_spider():
    try:
        headers = {
        	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        	"Cookie":"td_cookie=1007491179; sessionid=782bdac30c56d42d18134ec01c648f6a; channelid=0; sid=1493713993955445; _ga=GA1.2.99185331.1493257204; _gat=1; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1493257204,1493257206; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1493714508"
        }
        base_url = "http://www.kuaidaili.com/free/inha/"
        for i in range(1, 11):
            url = base_url + str(i) + '/'
            r = requests.get(url=url, headers=headers)
            #print r.content
            soup = bs(r.content, 'lxml')
            datas = soup.find_all(name='tr')

            for data in datas[1:]:
                soup_proxy_content = bs(str(data), 'lxml')
                soup_proxys = soup_proxy_content.find_all(name='td')
                ip = str(soup_proxys[0].string)
                port = str(soup_proxys[1].string)
                types = str(soup_proxys[3].string)
                proxy_check(ip, port, types)
           	time.sleep(1)
    except Exception,e:
        print e
        pass
        
def proxy_check(ip, port, types):
    proxy = {}
    proxy[types.lower()] = '%s:%s' % (ip, port)

    try:
        r = requests.get('http://1212.ip138.com/ic.asp', proxies=proxy, timeout=4)
        if r.status_code == 200:
        	print types.lower(), ip+":"+port
        '''
        ip_content = re.findall(r'\[(.*?)\]', r.text)[0]
        if ip == ip_content:
            print types.lower(), ip, port
        '''

    except Exception, e:
        #print e
        pass

print "start"
proxy_spider()