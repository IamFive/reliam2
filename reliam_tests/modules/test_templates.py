# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from reliam_tests import BasicTestCase

class TestTemplates(BasicTestCase):
    """ """

    formdata = dict(
        title='This is a sample Template',
        subject=["email sample"],
        fromaddrs=['from@from.com'],
        html='This is html content',
        text='This is text content',
        tokens=[
            dict(name='token1', values=['v1', 'v2']),
            dict(name='token2', values=['v11', 'v22'])
        ],
        tokenss=[
            dict(name='token1', values=['v1', 'v2']),
            dict(name='token2', values=['v11', 'v22'])
        ]
    )

    def post(self):
        to_post = self.formdata.copy()
        return self.request('post', self.bp_template_path, data=to_post)


    def test_post(self):
        template = self.post()
        self.assertEqual(template['title'], self.formdata['title'])
        self.assertEqual(template['fromaddrs'], self.formdata['fromaddrs'])
        self.assertEqual(template['html'], self.formdata['html'])


    def test_put(self):
        # post a template first
        template = self.post()
        template['title'] = 'Changed title'
 
        modified = self.request('put', self.bp_template_path + template['_id'], data=template)
        self.assertEqual(modified['_id'], template['_id'])
        self.assertEqual(modified['title'], 'Changed title')



    def test_delete(self):
        response = self.request('delete', self.bp_template_path, return_response=True)
        self.assert405(response)
 
        template = self.post()
        self.request('delete', self.bp_template_path + template['_id'])
 
        # then we try to get the template
        response = self.request('get', self.bp_template_path + template['_id'], return_response=True)
        self.assert404(response)
 
 
    def test_get_list(self):
        # post two questions
        self.post()
        template = self.post()
        where = {
            'id': template['_id'],
        }
        self.get_list(self.bp_template_path, where=where, expect_size=1)
        template_list = self.get_list(self.bp_template_path,)
 
        # we delete one
        self.request('delete', self.bp_template_path + template['_id'])
        self.get_list(self.bp_template_path, where=where, expect_size=0)
        # left one
        self.get_list(self.bp_template_path, expect_size=len(template_list) - 1)
 
 
 
    def test_get(self):
        template = self.post()
        result = self.request('get', self.bp_template_path + template['_id'])
        assert isinstance(result, dict)
        self.assertEqual(result['_id'], template['_id'])
        self.assertEqual(result['title'], template['title'])
        
    
    def test_put_token(self):
        template = self.post()
        path = self.bp_template_path + template['_id'] + '/tokens'
        
        tokens = dict(tokens=[
            dict(name='token3', values=['v4']),
            dict(name='token4', values=['v44'])
        ])
        
        result = self.request('put', path, tokens)
        self.assertTrue(result)
        
        
        newtpl = self.request('get', self.bp_template_path + template['_id'])
        self.assertEqual(newtpl.get('tokens'), tokens.get('tokens'))
        
        

if __name__ == "__main__":
    unittest.main()
