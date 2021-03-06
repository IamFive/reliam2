# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#

import json
import unittest

from reliam.models import Campaign, Template, Recipient, RecipientZip, \
    ImportTask
from reliam_tests import BasicTestCase
from mongoengine.document import Document
from mongoengine.fields import StringField, ListField


class Test(BasicTestCase):

#     def test_add_2_set_for_single_doc(self):
#         
#         tpl = dict(
#             title='This is a sample Template',
#             subject=["email sample"],
#             fromaddr=['from@from.com'],
#             html='This is html content',
#             text='This is text content',
#             tokens=[
#                 dict(name='token1', values=['v1', 'v2']),
#                 dict(name='token2', values=['v11', 'v22'])
#             ]
#         )
#         
#         t1 = Template.from_json(json.dumps(tpl))
#         t1.save()
#         
#         c1 = Campaign.from_json(json.dumps(dict(title='Test title')))
#         c1.save()
#         c1.update(add_to_set__templates=t1)
#         print c1
        
        
    def test_dict_field(self):
        r = Recipient()
        r.email = 'xmufive@gmail.com'
        r.props = dict(token1='t1', token2=222)
        r.save()
        
        token1 = r.props.get('token1')
        token2 = r.props.get('token2')
        print r.props
        
    def test_insert_zip(self):
        zip = RecipientZip()
        zip.name = 'test.txt'
        zip.path = 'path'
        zip.save()
        
    def test_listfield(self):
        ''' '''
        it = ImportTask(email_col_index=0, tokens=['aa', 'bb', ''])
        it2 = ImportTask(email_col_index=0, tokens=['aa', 'dd', ''])
        
        it.save()
        it2.save()
        
        objs = ImportTask.objects(tokens='aa').distinct('tokens')
        result = []
        result.extend(objs)
        result.append('email')
        print result
        
    def test_refrence(self):
        rz = RecipientZip()
        rz.save()
        it = ImportTask(email_col_index=0, tokens=['aa', 'bb', ''], zip=str(rz.id))
        it.save()
        
        print it.zip
        
    def test_get_tags(self):
        ImportTask(email_col_index=0, tags=['aa', 'bb']).save()
        ImportTask(email_col_index=0, tags=['aa', 'cc']).save()
        ImportTask(email_col_index=0, tags=['cc', 'dd']).save()
        
        
        tag_freqs = ImportTask.objects(tags__contains='a').item_frequencies('tags', normalize=True)
        
        from operator import itemgetter
        top_tags = sorted(tag_freqs.items(), key=itemgetter(1), reverse=True)[:2]
        print top_tags
        
    def test_filter_tags(self):
        class Post(Document):
            title = StringField()
            tags = ListField(StringField())
        
#         post1 = Post(title='Fun with MongoEngine', tags=['mongodb', 'mongoengine']).save()
#         post2 = Post(title='Loving Mongo', tags=['mongodb']).save()
#         post2 = Post(title='Loving Mongo', tags=['mongodb']).save()
#         post2 = Post(title='Loving Mongo', tags=['mongo2']).save()
        
        posts = Post.objects(tags__contains='mongodb').item_frequencies('tags')
        print posts
        
        
if __name__ == "__main__":
    unittest.main()
