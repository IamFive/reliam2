# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#

import datetime
import os
import unittest
from reliam_tests import BasicTestCase
import csv
import zipfile


class TestCSV(BasicTestCase):
    
    def parse(self, filename):
        with open(filename, 'rb') as csvfile:
            try:
                dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=[',', ';'])
            except:
                dialect = None
                
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            for line in reader:
                print line
                
                
    def test_parse_csv(self):
        self.parse('aa.csv')
     
#     def test_parse_csv(self):
#         sniffer = csv.Sniffer()
#         dialect = sniffer.sniff('quarter,dime,nickel,penny', delimiters=';,')
#         reader = csv.reader(['quarter,dime,nickel,penny'], None)
#         for line in reader:
#             print line
         
    def test_parse_csv2(self):
          
        samples = [
            'quarter, dime, nickel, penny',
            'quarter,dime,nickel,penny',
            'quarter;dime;nickel;penny',
            '"quarter";"dime";"nickel";"penny"',
            '"quarter"|"dime"|"nickel"|"penny"',
        ]
          
        sniffer = csv.Sniffer()
        for sample in samples:
            dialect = sniffer.sniff(sample, delimiters=",\t :;")
            reader = csv.reader([sample, ], dialect)
            for line in reader:
                print line
    
    #===========================================================================
    # def test_unzip(self):
    #     zipfile.ZipFile("us-500.zip").extractall("us-500")
    #===========================================================================
        
            
if __name__ == "__main__":
    unittest.main()
