#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

def parsePatentInfoFromXML_2005(xmlcontent):
    patent_info = {}
    root = BeautifulSoup(xmlcontent, 'xml')

    # Patent Number and Issue Date
    publication_reference = root.find('publication-reference')
    patent_info['patent_number'] = publication_reference.find('doc-number').text.strip()
    patent_info['issue_date'] = publication_reference.find('date').text.strip()

    # Application Date
    application_reference = root.find('application-reference')
    patent_info['application_date'] = application_reference.find('date').text.strip()

    # Classification
    classification_national = root.find('classification-national')
    patent_info['classification'] = classification_national.find('main-classification').text.strip()

    # Assignees info
    assignees_info = []
    try:
        assignees = root.find('assignees')
        if assignees is not None:
            assignees = assignees.find_all('assignee')
            for assignee in assignees:
                name = assignee.find('orgname').text.strip()
                city = assignee.find('city')
                if city is None:
                    city = ""
                else:
                    city = city.text.strip()
                state = assignee.find('state')
                if state is None:
                    state = ""
                else:
                    state = state.text.strip()
                country = assignee.find('country')
                if country is None:
                    country = ""
                else:
                    country = country.text.strip()

                assignees_info.append( (patent_info['patent_number'], name, city, state, country) )
    except:
        pass

    patent_info['assignees'] = assignees_info
        
    # citation information
    citations_info = []
    try:
        citations = root.find('references-cited').find_all('citation')
        for citation in citations:
            number = citation.find('doc-number').text.strip()
            country = citation.find('country')
            if country is None:
                country = ""
            else:
                country = country.text.strip()
            date = citation.find('date')
            if date is None:
                date = ""
            else:
                date = date.text.strip()
            category = citation.find('category')
            if category is None:
                category = ""
            else:
                category = category.text.strip()

            citations_info.append( (patent_info['patent_number'], number, date, country, category) )
    except:
        pass

    patent_info['citations'] = citations_info

    return patent_info

def parsePatentInfoFromXML_2001(xmlcontent):
    patent_info = {}
    root = BeautifulSoup(xmlcontent, 'xml')

    # Patent Number and Issue Date
    patent_info['patent_number'] = root.find('B110').text.strip()
    patent_info['issue_date'] = root.find('B140').text.strip()

    # Application Date
    patent_info['application_date'] = root.find('B220').text.strip()

    # Classification
    patent_info['classification'] = root.find('B521').text.strip()

    # Assignees info
    assignees_info = []
    try:
        assignees = root.find_all('B731')
        if assignees is not None:
            for assignee in assignees:
                name = assignee.find('NAM').text.strip()
                city = assignee.find('CITY')
                if city is None:
                    city = ""
                else:
                    city = city.text.strip()
                state = assignee.find('STATE')
                if state is None:
                    state = ""
                else:
                    state = state.text.strip()
                country = assignee.find('CTRY')
                if country is None:
                    country = ""
                else:
                    country = country.text.strip()

                assignees_info.append( (patent_info['patent_number'], name, city, state, country) )
    except:
        pass

    patent_info['assignees'] = assignees_info
     
    # citation information
    citations_info = []
    try:
        citations = root.find_all('B561')
        for citation in citations:
            number = citation.find('DNUM').text.strip()
            country = citation.find('country')
            if country is None:
                country = ""
            else:
                country = country.text.strip()
            date = citation.find('DATE')
            if date is None:
                date = ""
            else:
                date = date.text.strip()
            category = citation.find(re.compile("^CITED-BY"))
            if category is None:
                category = ""
            else:
                category = category.name

            citations_info.append( (patent_info['patent_number'], number, date, country, category) )
    except:
        pass

    patent_info['citations'] = citations_info

    return patent_info



if __name__ == '__main__':
    for xml in open('data/pgb20010102.sgml').read().split('</PATDOC>'):
        print parsePatentInfoFromXML_2001(xml)
    





