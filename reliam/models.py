# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-14
#
import datetime

from flask_mongoengine.wtf.orm import model_form
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import StringField, DateTimeField, IntField, \
    ReferenceField, ListField, EmbeddedDocumentField, EmailField, URLField, \
    FloatField, DynamicField, DictField, LongField

from reliam.choices import Currency, TransferStatus
from reliam.common.orm import BaseModel
from reliam.constants import DEFAULT_FORM_EXCLUDE


class Stats(EmbeddedDocument):
    
    sent = IntField(default=0)
    open = IntField(default=0)
    click = IntField(default=0)
    conversion = IntField(default=0)
    revenue = IntField(default=0)
    unsubscribe = IntField(default=0)
    complaint = IntField(default=0)
    epm = FloatField(default=0)
    
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
    
    
class Recipient(StatableModel):
    ''' recipient mongo model '''
    
    email = EmailField(required=True)
    props = DictField()
    
    
class RecipientZip(StatableModel):
    ''' recipient zip mongo model '''
    
    name = StringField()
    path = StringField()
    upload_on = DateTimeField()
    size = StringField()
    size_ = LongField()
    
    ext = StringField()  # force zip and txt?
    
    original_path = StringField()
    
    import_on = DateTimeField(default=datetime.datetime.now)
    line = IntField()
    
    md5 = StringField()
    
    status = IntField(default=TransferStatus.Unused[0],
                      choices=TransferStatus.choices)
    
    
    
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
    subjects = ListField(StringField(required=True))
    fromaddrs = ListField(StringField(required=True), required=True)
    html = StringField(required=True)
    text = StringField(required=True)
    tokens = ListField(EmbeddedDocumentField(Token, default=Token), default=[])
    

class Delivery(StatableModel):
    '''
    '''
    

class Campaign(StatableModel):
    ''' Mongo Engine Model for campaigns '''
    
    #===========================================================================
    #  TODO : Need re design 
    #===========================================================================
    
    ###Campaign###
    # email, campaign, delivery, network, url, template, subject, from, html, text
    
    # from wireframes, those properties will be set from frontend
    title = StringField(required=True)
    
    # a campaign will have several deliveries
    deliveries = ListField(ReferenceField(Delivery))
    
    # a campaign can use several tpls (in any delivery)
    templates = ListField(ReferenceField(Template))
    
    # maybe use a Enum?
    currency = StringField(default=Currency.USD[0], choices=Currency.choices)
    payout = FloatField()
    
    
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

RecipientForm = model_form(Recipient, exclude=DEFAULT_FORM_EXCLUDE)

tpl_form_exclude = list(DEFAULT_FORM_EXCLUDE) + ['tokens', ]
TemplateForm = model_form(Template, exclude=tpl_form_exclude)

campaign_form_exclude = list(DEFAULT_FORM_EXCLUDE) + ['deliveries', 'templates', 'payout']
CampaignForm = model_form(Campaign, exclude=campaign_form_exclude)
