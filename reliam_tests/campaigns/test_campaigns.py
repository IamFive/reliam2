# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from reliam_tests import BasicTestCase

class TestCampaigns(BasicTestCase):
    """ """


#     title = StringField(required=True)
#     fromaddr = StringField(required=True)
#     html = StringField(required=True)
#     text = StringField(required=True)
#     tokens = ListField(EmbeddedDocumentField(Token, default=Token()))

    formdata = dict(
        title='This is a sample campaigns',
        fromaddr='from@from.com',
        html='This is html content',
        text='This is text content',
    )

    def post(self):
        to_post = self.formdata.copy()
        return self.request('post', self.bp_campaigns_path, data=to_post)


    def test_post(self):
        campaign = self.post()
        self.assertEqual(campaign['title'], self.formdata['title'])
        self.assertEqual(campaign['fromaddr'], self.formdata['fromaddr'])
        self.assertEqual(campaign['html'], self.formdata['html'])


#     def test_put(self):
#         # post a campaign first
#         campaign = self.post()
# 
#         campaign['name'] = 'Changed name'
#         campaign['timezone'] = '2'
# 
#         modified = self.request('put', self.bp_campaigns_path + campaign['_id'], data=campaign)
#         self.assertEqual(modified['_id'], campaign['_id'])
#         self.assertEqual(modified['name'], 'Changed name')
#         self.assertEqual(modified['timezone'], 2)



#     def test_delete(self):
#         response = self.request('delete', self.bp_campaigns_path, return_response=True)
#         self.assert405(response)
# 
#         campaign = self.post()
#         self.request('delete', self.bp_campaigns_path + campaign['_id'])
# 
#         # then we try to get the campaign
#         response = self.request('get', self.bp_campaigns_path + campaign['_id'], return_response=True)
#         self.assert404(response)
#         self.assert_failed_result(response, 404)
# 
# 
#     def test_get_list(self):
#         # post two questions
#         self.post()
#         campaign = self.post()
#         where = {
#             'id': campaign['_id'],
#         }
#         self.get_list(self.bp_campaigns_path, where=where, expect_size=1)
#         paper_list = self.get_list(self.bp_campaigns_path,)
# 
#         # we delete one
#         self.request('delete', self.bp_campaigns_path + campaign['_id'])
#         self.get_list(self.bp_campaigns_path, where=where, expect_size=0)
#         # left one
#         self.get_list(self.bp_campaigns_path, expect_size=len(paper_list) - 1)
# 
# 
# 
#     def test_get(self):
#         campaign = self.post()
#         result = self.request('get', self.bp_campaigns_path + campaign['_id'])
#         assert isinstance(result, dict)
#         self.assertEqual(result['_id'], campaign['_id'])


if __name__ == "__main__":
    unittest.main()
