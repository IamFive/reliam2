# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from reliam_tests import BasicTestCase
from bson.objectid import ObjectId
from reliam.models import Campaign

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
        
        
    
    def test_bind_question(self):

        # use a mock or something other way to do this?
        # or we initial data by manually?
        formdata = dict(
            title='This is a sample Template',
            subject=["email sample"],
            fromaddr=['from@from.com'],
            html='This is html content',
            text='This is text content',
            tokens=[
                dict(name='token1', values=['v1', 'v2']),
                dict(name='token2', values=['v11', 'v22'])
            ]
        )

        t1 = self.request('post', self.bp_template_path, data=formdata)
        t2 = self.request('post', self.bp_template_path, data=formdata)

        # post a campaign first
        campaign = self.post()

        # we add a tpl
        manage_t_base = self.bp_campaigns_path + campaign.get('_id') + '/tpls/'
        mange_t_url = manage_t_base + t1['_id']
        campaign = self.request('post', mange_t_url)


        # check whether the tpl is in the set
        get = Campaign.objects.get(id=campaign.get('_id'))
        self.assertListEqual([str(t.id) for t in get.templates],
                             [t1.get('_id')])

        # add tpl again
        self.request('post', mange_t_url)
 
        mange_t2_url = manage_t_base + t2['_id']
        self.request('post', mange_t2_url)
 
        # check whether the question revision set is really "set"
        get = Campaign.objects.get(id=campaign.get('_id'))
        self.assertListEqual([str(t.id) for t in get.templates],
                             [t1.get('_id'), t2.get('_id')])
 
 
        # remove question
        paper = self.request('delete', mange_t_url)
        get = Campaign.objects.get(id=paper.get('_id'))
        self.assertListEqual([str(t.id) for t in get.templates],
                             [t2.get('_id')])


if __name__ == "__main__":
    unittest.main()
