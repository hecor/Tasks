#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PatentXMLParser import *
import sqlite3

def create_database(cursor):
    cursor.execute(u"""create table patent_info
                ( patent_number     varchar(16),
                  issue_date        varchar(16),
                  application_date  varchar(16),
                  classification    varchar(16),
                  PRIMARY KEY (patent_number)
                )"""
            )
    cursor.execute(u"""create table assignee_info
                ( patent_number     varchar(16),
                  assignee          varchar(32),
                  assignee_city     varchar(32),
                  assignee_state    varchar(16),
                  assignee_country  varchar(16),
                  PRIMARY KEY (patent_number, assignee)
                )"""
            )
    cursor.execute(u"""create table citation_info
                ( patent_number       varchar(16),
                  cited_patent_number varchar(16),
                  cited_date          varchar(16),
                  cited_country       varchar(16),
                  cited_by            varchar(32),
                  PRIMARY KEY (patent_number, cited_patent_number)
                )"""
            )
    
def write_to_database(cursor, patent_info):
    placeholder = ', '.join(['?']*4)
    cursor.execute("INSERT INTO patent_info values (" + placeholder + ")", 
                    ( patent_info['patent_number'], patent_info['issue_date'],
                      patent_info['application_date'], patent_info['classification'],
                      ) )
    placeholder = ', '.join(['?']*5)
    cursor.executemany("INSERT INTO assignee_info values (" + placeholder + ")", patent_info['assignees'] )
    placeholder = ', '.join(['?']*5)
    for citation in patent_info['citations']:
        try:
            cursor.execute("INSERT INTO citation_info values (" + placeholder + ")", citation)
        except sqlite3.IntegrityError:
            pass



if __name__ == '__main__':
    database_filename = './patent_info.db'
    create_database( database_filename )
#    conn = pypyodbc.win_connect_mdb(database_filename)
    conn = sqlite3.connect( database_filename )
    c = conn.cursor()
    
    patent_info = parsePatentInfoFromXML_2001(open('2001-2004.xml').read())
    write_to_database( c, patent_info )

    conn.commit()
    conn.close()


