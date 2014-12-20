# -*- coding: utf-8 -*-

import datetime
import os
import urllib.request
import re

def getUrlList(url):

    ret = []

    baseUrl = re.findall('(http://.+?)/',url)[0]

    httpRequest = urllib.request.Request(url)

    httpResponse = urllib.request.urlopen(httpRequest)

    html = httpResponse.read().decode('utf-8').split('>')

    for h in html:

        #find link for pdf like <a href='*.pdf'>*</a>
        u = re.findall('<a href="(.+\.pdf)"', h)

        if len(u) > 0:

            ret.append(baseUrl + u[0])

    return ret

def downloadFiles_exe(url, downloadPath):

    try:
    
        urllib.request.urlretrieve(url,downloadPath)

        print('[ok] %s' % url)

    except:

        print('[ng] %s' % url)
    
    return

def downloadFiles(url, downloadDir):

    print('[start] %s' % url)

    ul = getUrlList(url)

    for u in ul:

        f = re.findall('http://.+/(.+\.pdf)',u)[0]

        downloadFiles_exe(u, os.path.join(downloadDir, f))

    return

def main(argv):

    if len(argv) == 3:

        urlList = argv[1]

        downloadDir = argv[2]

    else:

        f = open('win.ini','r')

        s = f.read().split('\n')

        urlList = s[0]

        downloadDir = s[1]

        f.close()        

    today = datetime.datetime.today().strftime('%Y%m%d')

    #./dl/yyyyMMdd/
    os.mkdir(os.path.join(downloadDir, today))

    for line in open(urlList,'r'):

        #tag \t url
        l = line.split('\t')

        os.mkdir(os.path.join(downloadDir, today, l[0]))

        downloadFiles(l[1], os.path.join(downloadDir, today, l[0]))

    print(os.path.join(downloadDir, today))

    return

if __name__ == "__main__":

    import sys

    #python3 donwloadFiles.py ../etc/urlList.tsv ../dl/
    main(sys.argv)
