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
        
    def test_listdir(self):
        ftp_path = self._app.config.get('FTP_PATH')
        ftp_folder = os.path.abspath(os.path.join(ftp_path, 'initial@abc.com'))
        
        files = os.listdir(ftp_folder)
        
        for root, _, files in os.walk(ftp_folder):
#             print root, files
            for f in files:
                abs = os.path.abspath(os.path.join(root, f))
                stats = os.stat(abs)
                print os.path.basename(abs)
            
        
if __name__ == "__main__":
    unittest.main()
