# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from reliam_tests import BasicTestCase
from bson.objectid import ObjectId

class TestCampaigns(BasicTestCase):
    """ """

    formdata = dict(
        title='This is a sample campaigns',
        currency='CAD'
    )

    def post(self):
        to_post = self.formdata.copy()
        return self.request('post', self.bp_campaigns_path, data=to_post)


    def test_post(self):
        campaign = self.post()
        self.assertEqual(campaign['title'], self.formdata['title'])
        self.assertEqual(campaign['currency'], self.formdata['currency'])
        
        
    def test_post_with_tpls(self):
        ''' should be ignored '''
        to_post = self.formdata.copy()
        to_post['templates'] = [str(ObjectId())]
        campaign = self.request('post', self.bp_campaigns_path, data=to_post)
        self.assertEqual(campaign['templates'], []);


    def test_put(self):
        # post a campaign first
        campaign = self.post()
        campaign['title'] = 'Changed name'
 
        modified = self.request('put', self.bp_campaigns_path + campaign['_id'], data=campaign)
        self.assertEqual(modified['_id'], campaign['_id'])
        self.assertEqual(modified['title'], 'Changed name')



    def test_delete(self):
        response = self.request('delete', self.bp_campaigns_path, return_response=True)
        self.assert405(response)
 
        campaign = self.post()
        self.request('delete', self.bp_campaigns_path + campaign['_id'])
 
        # then we try to get the campaign
        response = self.request('get', self.bp_campaigns_path + campaign['_id'], return_response=True)
        self.assert404(response)
        self.assert_failed_result(response, 404)
 
 
    def test_get_list(self):
        # post questions
        self.post()
        self.post()
        self.post()
        campaign = self.post()
        where = {
            'id': campaign['_id'],
        }
        self.get_list(self.bp_campaigns_path, where=where, expect_size=1)
        paper_list = self.get_list(self.bp_campaigns_path,)
 
        # we delete one
        self.request('delete', self.bp_campaigns_path + campaign['_id'])
        self.get_list(self.bp_campaigns_path, where=where, expect_size=0)
        # left one
        self.get_list(self.bp_campaigns_path, expect_size=len(paper_list) - 1)
 
 
 
    def test_get(self):
        campaign = self.post()
        result = self.request('get', self.bp_campaigns_path + campaign['_id'])
        assert isinstance(result, dict)
        self.assertEqual(result['_id'], campaign['_id'])


if __name__ == "__main__":
    unittest.main()
