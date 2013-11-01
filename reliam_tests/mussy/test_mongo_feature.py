# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#

import json
import unittest

from reliam.models import Campaign, Template
from reliam_tests import BasicTestCase


class Test(BasicTestCase):

    def test_add_2_set_for_single_doc(self):
        
        tpl = dict(
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
        
        t1 = Template.from_json(json.dumps(tpl))
        t1.save()
        
        c1 = Campaign.from_json(json.dumps(dict(title='Test title')))
        c1.save()
        c1.update(add_to_set__templates=t1)
        print c1


if __name__ == "__main__":
    unittest.main()
