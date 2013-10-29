# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-14
#
from flask_mongoengine.wtf.orm import model_form
from reliam.common.orm import BaseModel
from reliam.constants import DEFAULT_FORM_EXCLUDE
from mongoengine.fields import (StringField, DateTimeField, IntField,
    ReferenceField, ListField, EmbeddedDocumentField, EmailField, URLField,
    FloatField)
import datetime
from mongoengine.document import EmbeddedDocument


class Stats(EmbeddedDocument):
    
    open = IntField(default=0)
    click = IntField(default=0)
    conversion = IntField(default=0)
    revenue = IntField(default=0)
    unsubscribe = IntField(default=0)
    complaint = IntField(default=0)
    
    meta = {
        'allow_inheritance': False
    }
    

class StatableModel(BaseModel):
    ''' basic model for statable documents '''
    stats = EmbeddedDocumentField(Stats, default=Stats)
    meta = {'abstract': True}
    

class User(BaseModel):
    """ user mongo model """

    email = EmailField(required=True, unique=True)
    password = StringField(max_length=16, required=True)

    # used when validate email
    verify_code = StringField(max_length=6)


    last_login_on = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance' : False
    }
    
    
class Token(EmbeddedDocument):

    name = StringField()
    values = ListField(StringField())
    
    meta = {
        'allow_inheritance': False
    }
    
    def __init__(self, *args, **kwargs):
        super(EmbeddedDocument, self).__init__(*args, **kwargs)
        
#     @staticmethod
#     def fromjson(jsonform):
#         t = Token()
#         t.name = jsonform['name']
#         t.values = jsonform['values']
#         return t
    
        
class Template(StatableModel):
    
    title = StringField(required=True)
    subject = StringField(required=True)
    fromaddr = StringField(required=True)
    html = StringField(required=True)
    text = StringField(required=True)
    tokens = ListField(EmbeddedDocumentField(Token, default=Token), default=[])
        
    

class Campaign(StatableModel):
    ''' Mongo Engine Model for campaigns '''
    
    #===========================================================================
    #  TODO : Need re design 
    #===========================================================================
    
    ###Campaign###
    #email, campaign, delivery, network, url, template, subject, from, html, text
    
    # from wireframes, those properties will be set from frontend
    title = StringField(required=True)
    fromaddr = StringField(required=True)
    html = StringField(required=True)
    text = StringField(required=True)
    tokens = ListField(EmbeddedDocumentField(Token, default=Token))
    
    
    meta = {
        'allow_inheritance' : False
    }

    
class Network(BaseModel):
    '''  '''
    
    title = StringField(required=True)
    campaign_id = ReferenceField(Campaign)
    link_mask = StringField(required=True)
    unsub_mask = StringField(required=True)
    
    meta = {
        'allow_inheritance' : False
    }
    

user_form_exclude = list(DEFAULT_FORM_EXCLUDE)
user_form_exclude.extend(('last_login_on', 'verify_code'))
UserForm = model_form(User, exclude=user_form_exclude)

tpl_form_exclude = list(DEFAULT_FORM_EXCLUDE) + ['tokens',]
TemplateForm = model_form(Template, exclude=tpl_form_exclude)

CampaignForm = model_form(Campaign, exclude=DEFAULT_FORM_EXCLUDE)
