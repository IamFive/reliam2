# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from reliam_tests import BasicTestCase

class TestRecipients(BasicTestCase):
    """ """

    formdata = dict(
        email='iampurse@vip.qq.com'
    )

    def post(self):
        to_post = self.formdata.copy()
        return self.request('post', self.bp_recipients_path, data=to_post)


    def test_post(self):
        recipient = self.post()
        self.assertEqual(recipient['email'], self.formdata['email'])
        

    def test_put(self):
        # post a recipient first
        recipient = self.post()
        recipient['email'] = 'xmufive@gmail.com'
 
        modified = self.request('put', self.bp_recipients_path + recipient['_id'], data=recipient)
        self.assertEqual(modified['_id'], recipient['_id'])
        self.assertEqual(modified['email'], 'xmufive@gmail.com')



    def test_delete(self):
        response = self.request('delete', self.bp_recipients_path, return_response=True)
        self.assert405(response)
 
        recipient = self.post()
        self.request('delete', self.bp_recipients_path + recipient['_id'])
 
        # then we try to get the recipient
        response = self.request('get', self.bp_recipients_path + recipient['_id'], return_response=True)
        self.assert404(response)
        self.assert_failed_result(response, 404)
 
 
    def test_get_list(self):
        # post questions
        self.post()
        self.post()
        self.post()
        recipient = self.post()
        where = {
            'id': recipient['_id'],
        }
        self.get_list(self.bp_recipients_path, where=where, expect_size=1)
        paper_list = self.get_list(self.bp_recipients_path,)
 
        # we delete one
        self.request('delete', self.bp_recipients_path + recipient['_id'])
        self.get_list(self.bp_recipients_path, where=where, expect_size=0)
        # left one
        self.get_list(self.bp_recipients_path, expect_size=len(paper_list) - 1)
 
 
    def test_get(self):
        recipient = self.post()
        result = self.request('get', self.bp_recipients_path + recipient['_id'])
        assert isinstance(result, dict)
        self.assertEqual(result['_id'], recipient['_id'])
        
    def test_get_zip(self):
        zip = self.request('get', self.bp_recipients_path + 'zip')


if __name__ == "__main__":
    unittest.main()
