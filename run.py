#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PatentXMLParser import *
from Writer import *
import sqlite3, datetime

if __name__ == '__main__':
    print datetime.datetime.now()
    database_filename = './patent_info.db'
#    create_database( database_filename )
#    conn = pypyodbc.win_connect_mdb(database_filename)
    conn = sqlite3.connect( database_filename )
    c = conn.cursor()
    
    f = open('ipgb20120103.xml')
    xmls = f.read().split('<?xml version="1.0" encoding="UTF-8"?>')
    print 'patent number:', len(xmls)
    for xml in xmls:
        if xml != "":
            patent_info = parsePatentInfoFromXML(xml)
            write_to_database( c, patent_info )

    conn.commit()
    conn.close()
    print datetime.datetime.now()

