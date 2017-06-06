#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup as bs
import sys
from multiprocessing import Process, Queue, Pool, Manager
import datetime
import time



def proxy_spider(queue, lock, proxy_type="http"):
	print "proxy_spider process start"
	headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
	base_url = {}
	base_url["http"] = "http://www.xicidaili.com/nn/"
	base_url["https"] = "http://www.xicidaili.com/wn/"
	base_url["qq"] = "http://www.xicidaili.com/qq/"
	for i in range(1, 20):
		url = base_url[proxy_type] + str(i)
		#print url
		r = requests.get(url=url, headers=headers)
		soup = bs(r.content, 'lxml')
		datas = soup.find_all(name='tr', attrs={'class':re.compile('|[^odd]')})

		for data in datas:
			soup_proxy_content = bs(str(data), 'lxml')
			soup_proxys = soup_proxy_content.find_all(name='td')
			ip = str(soup_proxys[1].string)
			port = str(soup_proxys[2].string)
			types = str(soup_proxys[5].string)
			#proxy_check(ip, port, types)
			lock.acquire()
			queue.put([ip, port, types])
			lock.release()
		time.sleep(1)

def proxy_check(queue, stop_flag):
	print "proxy_check process start"
	while True:
		try:
			if stop_flag:
				break
			if not queue.empty():
				ip, port, types = queue.get()
				proxy = {}
				proxy[types.lower()] = '%s:%s' % (ip, port)
				print proxy

				r = requests.get('http://1212.ip138.com/ic.asp', proxies=proxy, timeout=6)
				ip_content = re.findall(r'\[(.*?)\]', r.text)[0]
				if ip == ip_content:
					print types.lower(), ip + ":" + port + ' is ok!'
					file = open("proxies.txt", "w")
					file.write(types.lower(), ip + ":" + port + '\n')
					file.flush()
					file.close()

		except Exception, e:
			#print e
			pass

def stop(stop_flag):
	while True:
		exit = raw_input()
		if "stop" == exit:
			stop_flag = True
			break
		time.sleep(1)


#proxy_type = sys.argv[1]
#proxy_spider(proxy_type)


if __name__ == "__main__":
	#多线程之间要想通过Queue进行通信，必须要通过multiprocessiong的manager
	manager = Manager()
	queue = manager.Queue()
	lock = manager.Lock()
	p = Pool()
	stop_flag = False

	proxy_spider_process = p.apply_async(proxy_spider, args=(queue, lock, "http"))
	proxy_check_process = p.apply_async(proxy_check, args=(queue, stop_flag))
	stop_process = p.apply_async(stop, args=(stop_flag, ))
	p.close()
	p.join()

	print
	print 'done'