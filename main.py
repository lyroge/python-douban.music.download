#! /usr/bin/python2.7
# -- coding:utf-8 --

import os, re
import urllib,threading

#匹配音乐url

#{"name":"给他一瓶可乐",
# "url":"aHR0cDovL21yMy5kb3ViYW4uY29tLzIwMTIxMTE1MTUzOC9hODk3NmY2MTJjZGY3YmMyMWFkYjkyYWI3ZmFmY2E1Ny92aWV3L211c2ljaWFubXAzL21wMy94MTM3MDQyNzkubXAz",
# "cover":"http:\/\/img3.douban.com\/view\/site\/small\/public\/197604b046aae66.jpg",
# "isDemo":false,
# "rawUrl":"http:\/\/mr3.douban.com\/201211151538\/a8976f612cdf7bc21adb92ab7fafca57\/view\/musicianmp3\/mp3\/x13704279.mp3",
# "id":"294349"}

#(?:.+?) nocare things
reg=re.compile('{"name":"(.+?)" (?:.+?) "rawUrl":"(.+?)" (?: ,.+? )}', re.I | re.X)

#音乐下载线程类
class downloader(threading.Thread):
        def __init__(self, url, name):
                threading.Thread.__init__(self)
                self.url=url
                self.name=name

        def run(self):
                print 'downloading from %s' % self.url
                urllib.urlretrieve(self.url, self.name.decode('utf8'))

#线程数组
threads=[]

#多线程下载文件
def main(websiteurl):
        response=urllib.urlopen(websiteurl)
        text=response.read()

        groups=re.finditer(reg, text)
        for g in groups:
                name=g.group(1).strip() + ".mp3"
                path=g.group(2).replace('\\', '')
                t=downloader(path, name)
                threads.append(t)


if __name__ == '__main__':
        main("http://site.douban.com/huazhou/")
        for t in threads:
                t.start()
        for t in threads:
                t.join()
