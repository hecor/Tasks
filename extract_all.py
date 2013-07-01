#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re, os
from bs4 import BeautifulSoup
from PatentXMLParser import *
from Writer import *
import sqlite3, datetime

parse_function_map = { '2005':parsePatentInfoFromXML_2005, '2001':parsePatentInfoFromXML_2001 }
split_string_map = {'2005':'<?xml version="1.0" encoding="UTF-8"?>', '2001':'</PATDOC>'}

def parseXMLfile(cursor, filename, format_version):
    print 'parse xml file', filename
    f = open(filename)
    xmls = f.read().split(split_string_map[format_version])
    print 'patent number:', len(xmls)
    for xml in xmls:
        if xml != "":
            try:
                patent_info = parse_function_map[format_version](xml)
                write_to_database(cursor, patent_info)
            except:
                pass


conn = sqlite3.connect('./patent_info.db')
c = conn.cursor()
#create_database(c)

url = 'http://www.google.com/googlebooks/uspto-patents-grants-biblio.html'
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')

if_start = False

#for i in range(2012, 2013):
#    print 'Parse year ', i
#    one_year_links = soup.find_all('a', text=re.compile("ipgb"+str(i)))
#    for link in one_year_links:
#        if link['href'].find('ipgb20121211') != -1:
#            if_start = True
#        if if_start:
#            print link['href']
#            os.system('wget --directory-prefix=data ' + link['href'])
#            tt = link.text.strip()
#            os.system('unzip -d data/ data/'+tt)
#            parseXMLfile(c, 'data/'+tt[ : tt.find('_')]+'.xml', '2005')
#            conn.commit()

for i in range(2002, 2005):
    print 'Parse year ', i
    one_year_links = soup.find_all('a', text=re.compile("pgb"+str(i)))
    for link in one_year_links:
        if link['href'].find('pgb20040511') != -1:
            if_start = True
        if if_start:
            print link['href']
            os.system('wget --directory-prefix=data ' + link['href'])
            tt = link.text.strip()
            os.system('unzip -d data/ data/'+tt)
            parseXMLfile(c, 'data/'+tt[ : tt.find('_')]+'.xml', '2001')
            conn.commit()

conn.close()

