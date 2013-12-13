# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#

import unittest
from reliam_tests import BasicTestCase
import os
import datetime

class Test(BasicTestCase):
        
#     def test_listdir(self):
#         ftp_path = self._app.config.get('FTP_PATH')
#         ftp_folder = os.path.abspath(os.path.join(ftp_path, 'initial@abc.com'))
#         
#         files = os.listdir(ftp_folder)
#         
#         for root, _, files in os.walk(ftp_folder):
# #             print root, files
#             for f in files:
#                 abs = os.path.abspath(os.path.join(root, f))
#                 stats = os.stat(abs)
#                 print os.path.basename(abs)
#                 
#                 
#     def test_palindromes(self):
#         
#         words = {"radar", "apple", "hello", "evitative"}
#         for word in words:
#             reversed_word = word[::-1]
#             if reversed_word == word:
#                 print True
#             else:
#                 print False
                
    def zeon_day_of_week(self):
        day = 17
        month = 11
        year = 2013
        
        total_days = (13 / 2 + 1) * 21 + 13 / 2 * 22
        print total_days
        

def xy(x, y):
    
    if x == 0 or y == 0:
        return 1
    return xy(x - 1, y) + xy(x, y - 1)
    
            
        
if __name__ == "__main__":
    x = 2
    y = 1
    print xy(x, y)

    
    
    
    
#     day = 3
#     month = 1
#     year = 1900
#     
#     start_year = 1900
#     
#     days_per_year = 13 * 21 + 13 / 2
#     year_diff = year - 1900
#     days_for_years = (year_diff) * days_per_year - year_diff / 5
#     days_for_2013 = month * 21 + month / 2 + day - 1
#     
#     total_days = days_for_years + days_for_2013
#     
#     print total_days
#     
#     offset = total_days - total_days / 7 * 7
#     
#     print offset
#     
#     day_name = ['Monday', 'Tuesday', 'Wednesday',
#                 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     print day_name[offset]
    
    
