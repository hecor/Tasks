#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

if __name__ == '__main__':
    company_info = {}
    with open('./unique_companylist_2.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            company_info[row[0]] = [row[1], row[2]]

    for company in company_info.keys():
        rows = []
        company_name = company.replace(' ', '_').replace('.', '_').replace('-', '_').replace('&', '_').replace("'", "_")
        with open('/home/chawu/Downloads/patents_sorted/'+company_name+'.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                row.extend( company_info[company] )
                rows.append('\t'.join(row))

        expand_file = open('/home/chawu/Downloads/patents_expand/'+company_name+'.csv', 'w')
        expand_file.write('\n'.join(rows))
        expand_file.write('\n')
        expand_file.close()


