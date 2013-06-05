#! /usr/bin/python2.7
# -- coding:utf-8 --

import os, re, sys, time
import urllib,urllib2,threading

#设置豆瓣下载器的urlopener
class doubanURLopener(urllib.FancyURLopener):
        version="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"
#urllib._urlopener = doubanURLopener()

#匹配音乐url
#{"name":"给他一瓶可乐",
# "url":"aHR0cDovL21yMy5kb3ViYW4uY29tLzIwMTIxMTE1MTUzOC9hODk3NmY2MTJjZGY3YmMyMWFkYjkyYWI3ZmFmY2E1Ny92aWV3L211c2ljaWFubXAzL21wMy94MTM3MDQyNzkubXAz",
# "cover":"http:\/\/img3.douban.com\/view\/site\/small\/public\/197604b046aae66.jpg",
# "isDemo":false,
# "rawUrl":"http:\/\/mr3.douban.com\/201211151538\/a8976f612cdf7bc21adb92ab7fafca57\/view\/musicianmp3\/mp3\/x13704279.mp3",
# "id":"294349"}

#(?:.+?) nocare things
reg=re.compile('{"name":"(.+?)"(?:.+?)"rawUrl":"(.+?)"(?:,.+?)}', re.I | re.X)


f=open('log.txt', 'w+')

#音乐下载线程类
class downloader(threading.Thread):
        def __init__(self, url, name):
                f.write(url + '\r\n')
                threading.Thread.__init__(self)
                self.url=url
                self.name=name

        def run(self):
                print 'downloading from %s' % self.url
                try:
                    urllib.urlretrieve(self.url, self.name.decode('utf8'))
                except Exception as e:
                    f.write('url:' + self.url + '\r\n' + str(e) + '\r\n')

#线程数组
threads=[]

#多线程下载文件
def main(websiteurl):
        #response=urllib.urlopen(websiteurl)
        req=urllib2.Request(websiteurl)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4")
        req.add_header("cookie", "bid=hellodouban")
        response=urllib2.urlopen(req)
        text=response.read()
        groups=re.finditer(reg, text)
        for g in groups:
                name=g.group(1).strip() + ".mp3"
                path=g.group(2).replace('\\', '')
                t=downloader(path, name)
                threads.append(t)


if __name__ == '__main__':
        args=sys.argv
        if len(args)<2:
                print u'没有指定小站路径，请指定。如：http://site.douban.com/huazhou/'
                sys.exit()

        main(args[1])

        for t in threads:
                t.start()
        	time.sleep(1)
		f.flush()
        for t in threads:
                t.join()
