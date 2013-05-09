#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
from httpc import *

curl = CurlHTTPC()

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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '109',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'pacer.login.uscourts.gov',
            'Origin': 'https://pacer.login.uscourts.gov',
            'Referer': 'https://pacer.login.uscourts.gov/cgi-bin/login.pl?appurl=https://pcl.uscourts.gov/search',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
            'Cookie': 'PacerClientCode=""; PacerPref="receipt=Y"',
            }

    res = curl.post(url, urllib.urlencode(values), header)

    return res['header']
    
def download():
    url = 'https://pcl.uscourts.gov/download'
    header = {
            'Cookie': 'PacerUser="ru067301368070812                                VgiExokw6Qs"; PacerSession="/qIrk65kOCHIr9VGIdnn5L1anzMXe4m2mo8xBRCKYExL5t20e9hRjX/NFYjVxTQQjV8hQJmau5VWfpBHmrOUlmv2i320gz+sX86VMgAoytE="; PacerClientCode=""; PacerPref="receipt=Y"; default_form="cvb"'
            }
    values = {
            'dl_fmt': 'csv',
            'rrrr': '%3Frid%3DsHAiRwk3F5PKqmAdTQD6hJZnbkvcdj2knXmfqLpc%26page%3D1',
            'rid': 'sHAiRwk3F5PKqmAdTQD6hJZnbkvcdj2knXmfqLpc',
            }
    res = curl.post(url, urllib.urlencode(values), header)
    return res

def query():
    url = 'https://pcl.uscourts.gov/dquery'
    header = {
            'Cookie': 'PacerUser="ru067301368070812                                VgiExokw6Qs"; PacerSession="/qIrk65kOCHIr9VGIdnn5L1anzMXe4m2mo8xBRCKYExL5t20e9hRjX/NFYjVxTQQjV8hQJmau5VWfpBHmrOUlmv2i320gz+sX86VMgAoytE="; PacerClientCode=""; PacerPref="receipt=Y"; default_form="cvb"'
            }
    values = {
            'case_no': '',
            'mdl_id': '',
            'stitle': '',
            'nos': '830',
            'date_filed_start': '01/01/2000',
            'date_filed_end': '12/31/2010',
            'date_term_start': '',
            'date_term_end': '',
            'date_dismiss_start': '',
            'date_dismiss_end': '',
            'date_discharge_start': '',
            'date_discharge_end': '',
            'party': 'Apple',
            'exact_party': 'exact_party',
            'ssn4': '',
            'ssn': '',
            'court_type': 'cv',
            'default_form': 'cvb',
            }
    res = curl.post(url, urllib.urlencode(values), header)
    return res



if __name__ == "__main__":
    print query()

