#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re
from bs4 import BeautifulSoup

def getPatentInfo(url):
    print url

    patent_info = {}
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')


    # get patent id and issue_date
    id_item = soup.find('td', text='United States Patent ').find_next_sibling('td')
    patent_id = id_item.text.strip()
    patent_info['patent_id'] = patent_id

    issue_date_item = id_item.parent.find_next_sibling('tr').find_all('td')[1]
    patent_info['issue_date'] = issue_date_item.text.strip()

    # get abstract
    try:
        abstract_item = soup.find('center', text='Abstract').find_next_sibling('p')
        abstract = abstract_item.text.strip()
        patent_info['abstract'] = abstract
    except AttributeError:
        patent_info['abstract'] = ''

    # get Inventors information
    inventor_item = soup.find('th', text='Inventors:').find_next_sibling('td')
    patent_info['inventor'] = inventor_item.text.strip()

    try:
        assignee_item = soup.find('th', text='Assignee:').find_next_sibling('td')
        assignee = assignee_item.text
        patent_info['company'] = assignee[ : assignee.find('(') ].strip(' \n')
        patent_info['company_loc'] = assignee[ assignee.find('(')+1 : -1 ].strip().replace('\n', '')
    except AttributeError:
        patent_info['company'] = ''
        patent_info['company_loc'] = ''
    
    filed_item = soup.find('th', text=re.compile('Filed:')).find_next_sibling('td')
    patent_info['file_date'] = filed_item.text.strip()
        
    # get Class information
    us_class = soup.find('td', text='Current U.S. Class:').find_next_sibling('td')
    patent_info['us_class'] = us_class.text.replace(' ', '')#.split(';')
    int_class = soup.find('td', text='Current International Class: ').find_next_sibling('td')
    patent_info['int_class'] = int_class.text.strip()
    try:
        field_search = soup.find('td', text='Field of Search: ').find_next_sibling('td')
        patent_info['field_search'] = field_search.text.strip()#.split(',')
    except AttributeError:
        patent_info['field_search'] = ''


    # get citation information
    citations = []
    citation_inventors = []
    center = soup.find('center', text='U.S. Patent Documents')
    if center:
        citation_table = center.find_next_sibling('table')
        all_tr = citation_table.find_all('tr')
        for i in range(1, len(all_tr)-1):
            tds = all_tr[i]('td')
            citation_id = tds[0].text.strip()
            citation_date = tds[1].text.strip()
            citation_author = tds[2].text.strip()
            citations.append((patent_id, 0, citation_id, citation_date, citation_author))
            citation_inventors += get_citation_info( citation_id )['inventors']

    # get Foreign Patent Documents
    center = soup.find('center', text='Foreign Patent Documents')
    if center:
        foreign_citataion_table = center.find_next_sibling('table')
        all_tr = foreign_citataion_table.find_all('tr')
        for i in range(1, len(all_tr)-1):
            tds = all_tr[i]('td')
            citation_id = tds[1].text.strip()
            citation_date = tds[3].text.strip()
            citation_author = tds[5].text.strip()
            citations.append((patent_id, 1, citation_id, citation_date, citation_author))

    patent_info['citations'] = citations
    patent_info['citation_inventors'] = citation_inventors

    # get other references
    other_references = ""
    center = soup.find('center', text='Other References')
    if center:
        other_references_table = center.find_next_sibling('tr')
        text = other_references_table.text
        other_references = text#.split('\n')

    patent_info['other_references'] = other_references


    print patent_info

    return patent_info


def get_citation_info(citation_id):
    citation_info = {}
    inventors = []

    # get Inventors information
    try:
        url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&p=1&f=G&l=50&d=PTXT&S1={0}.PN.&OS=PN/{0}&RS=PN/{0}'.format(citation_id)

        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')

        inventor_item = soup.find('th', text='Inventors:').find_next_sibling('td')
        inventor_text = inventor_item.text.strip().split('),')

#        html = html[ html.find('Inventors:') : ]
#        html = html[ html.find('<b>') : ]
#        html = html[ : html.find('</td>')-1 ]
#        html = html.replace('<b>', '')
#        html = html.replace('</b>', '')
#        inventor_text = html.split(')')

        for text in inventor_text:
            index = text.find('(')
            if index != -1:
                inventors.append( (citation_id, text[:index-1], text[index+1:]) )
    except:
        pass

    citation_info['inventors'] = inventors

    return citation_info


if __name__ == '__main__':
    print get_citation_info('4774664')





