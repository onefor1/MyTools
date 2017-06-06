#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup as bs

def proxy_spider():
	headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
	base_url = "http://www.xicidaili.com/nn/"
	for i in range(1, 100):
		url = base_url + str(i)
		r = requests.get(url=url, headers=headers)
		soup = bs(r.content, 'lxml')
		datas = soup.find_all(name='tr', attrs={'class':re.compile('|[^odd]')})

		for data in datas:
			soup_proxy_content = bs(str(data), 'lxml')
			soup_proxys = soup_proxy_content.find_all(name='td')
			ip = str(soup_proxys[1].string)
			port = str(soup_proxys[2].string)
			types = str(soup_proxys[5].string)
			proxy_check(ip, port, types)

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
			#print proxy
			print types.lower(), ip+":"+port
		'''

	except Exception, e:
		#print e
		pass

print "start"
proxy_spider()