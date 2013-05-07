#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2

def login():
    url = "https://pacer.login.uscourts.gov/cgi-bin/check-pacer-passwd.pl"

    values = {
                'loginid': 'ru0673',
                'passwd': 'xw215165',
                'client': '',
                'faction': 'Login',
                'appurl': 'https://pcl.uscourts.gov/search',
                'court_id': '',
              }

    header = {
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4',
            #'Cache-Control': 'max-age=0',
            #'Connection': 'keep-alive',
            #'Content-Length': '109',
            #'Content-Type': 'application/x-www-form-urlencoded',
            #'Host': 'pacer.login.uscourts.gov',
            #'Origin': 'https://pacer.login.uscourts.gov',
            #'Referer': 'https://pacer.login.uscourts.gov/cgi-bin/login.pl?appurl=https://pcl.uscourts.gov/search',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
            'Cookie': 'PacerClientCode=""; PacerPref="receipt=Y"',
            }

    req = urllib2.Request(url, urllib.urlencode(values), header)
    res = urllib2.urlopen(req)

    print res.info().getheader('Set-Cookie')
    
if __name__ == "__main__":
    print login()

