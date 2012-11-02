#! /usr/bin/python2.7
# -- coding:utf-8 --

import os, urllib,urllib2, thread,threading
import re

#匹配音乐url
reg=re.compile('{"name":"(.+?)".+?"rawUrl":"(.+?)",.+?}', re.I)


class downloader(threading.Thread):
        def __init__(self, url, name):
                threading.Thread.__init__(self)
                self.url=url
                self.name=name

        def run(self):
                print 'downloading from %s' % self.url
                urllib.urlretrieve(self.url, self.name)

threads=[]

#多线程下载文件
def main(url):
        response=urllib.urlopen(url)
        text=response.read()
        groups=re.finditer(reg, text)
        for g in groups:
                name=g.group(1).strip() + ".mp3"
                path=g.group(2).replace('\\', '')
                t=downloader(path, name)
                                                                                                                                                      5,1          顶端
if __name__ == '__main__':
        main("http://site.douban.com/huazhou/")
        for t in threads:
                t.join()
