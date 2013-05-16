#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from time import sleep
from subprocess import call
import csv


def download_by_company(browser, company):
    browser.get('https://pacer.login.uscourts.gov/cgi-bin/login.pl?appurl=https://pcl.uscourts.gov/search')
        
    elem = browser.find_element_by_id('loginid')
    elem.send_keys('ru0673')
    elem = browser.find_element_by_id('passwd')
    elem.send_keys('xw215165')
    elem = browser.find_element_by_id('submit')
    elem.send_keys(Keys.RETURN)


    elem = browser.find_element_by_id('li_cv')
    elem.click()
    elem = browser.find_element_by_id('cstext')
    if elem.text == 'Advanced Search':
        elem.click()
    elem = browser.find_element_by_xpath("//input[contains(@value, 'Select nature of suit')]")
    elem.click()
    elem.send_keys('830')
    elem.send_keys(Keys.RETURN)
    elem = browser.find_element_by_id('date_filed_start')
    elem.send_keys('01/01/2000')
    elem = browser.find_element_by_id('date_filed_end')
    elem.send_keys('12/31/2010')
    elem = browser.find_element_by_id('party')
    elem.send_keys(company)
    elem = browser.find_element_by_id('submit')
    elem.click()


    elem = browser.find_element_by_xpath('//*[@id="dl_div"]/img')
    elem.click()
    sleep(3)
    browser.execute_script('dlOptions();')
    elem = browser.find_element_by_xpath('//*[@id="dl_sel"]/span[3]/input[3]')
    elem.click()
    elem = browser.find_element_by_id('dl_yes')
    elem.click()

    sleep(30)
    clean_and_sort(company, browser)

def clean_and_sort(company, browser):
    company_name = company.replace(' ', '_').replace('.', '_').replace('-', '_').replace('&', '_').replace("'", "_")
    call("mv /home/chawu/Downloads/ru0673_uspci.csv /home/chawu/Downloads/patents_original/"+company_name+".csv", shell=True)

    query_length = len(company.split(' '))
    rows = []
    stats = {}
    first_line = True
    with open('/home/chawu/Downloads/patents_original/'+company_name+'.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if first_line:
                first_line = False
                continue

            if query_length <= 1:
                items = [i.lower() for i in row[0].split(' ')]
                if company.lower() not in items:
                    continue
            
            if row[3] not in stats.keys():
                stats[row[3]] = 1
            else:
                stats[row[3]] = stats[row[3]] + 1

            rows.append('\t'.join(add_case_property(row, company, browser)))

    output = open('/home/chawu/Downloads/patents_clean/'+company_name+'.csv', 'w')
    output.write('\n'.join(rows))
    output.close()

    call("sort -t'\t' -k 1,1 -k 4,4 /home/chawu/Downloads/patents_clean/"+company_name+".csv >/home/chawu/Downloads/patents_sorted/"+company_name+".csv", shell=True)
    
    stats_file = open('/home/chawu/Downloads/patents_stats/'+company_name+'.csv', 'w')
    for key, value in stats.iteritems():
        stats_file.write( company + '\t' + key + '\t' + str(value) + '\n' )
    stats_file.close()

def add_case_property(row, company, browser):
    print row[15].replace('iqquerymenu', 'qrySummary')
    browser.get(row[15].replace('iqquerymenu', 'qrySummary'))
    try:
        elem = browser.find_element_by_xpath('//*[@id="cmecfMainContent"]/table[2]')
        if elem.text.lower().find('defendant: '+company.lower()) != -1:
            row.append('Defendant')
        elif elem.text.lower().find('plaintiff: '+company.lower()) != -1:
            row.append('Plaintiff')
        else:
            row.append('None')
    except:
        row.append('None')

    print row
    return row


if __name__ == '__main__':
    browser = webdriver.Chrome()

    company_list = open('unique_companylist.txt').read().split('\n')
    print len(company_list)
    print company_list

    for company in company_list:
        if company == '':
            continue
        download_by_company(browser, company)
    
    browser.close()
    call("pkill chromedriver", shell=True)


