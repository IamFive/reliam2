# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-14
#
from string import lower

class Gender(object):
    M = 'M'
    F = 'F'
    U = 'U'
    choices = (M, F, U)


class Boolean(object):
    YES = '1'
    NO = '0'
    choices = (YES, NO)
    
    
class Currency(object):
    
    USD = ('USD', 'USD')
    CAD = ('CAD', 'CAD')
    
    choices = (USD, CAD)
    
class FileType(object):
    
    ZIP = 'zip'
    TXT = 'txt'
    CSV = 'csv'
    
    @staticmethod
    def is_zip(ext):
        return lower(ext) == FileType.ZIP
        
    
    choices = (ZIP, TXT, CSV)
