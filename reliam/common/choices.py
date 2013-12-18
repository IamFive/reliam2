# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

METHOD = ('GET', 'POST', 'PUT', 'DELTE', 'ANY')

class Gender(object):
    M = ('M', 'Male')
    F = ('F', 'Female')
    U = ('U', 'Unknown')
    choices = (M, F, U)

class DataSource(object):
    GETCLEVER = 'GetClever'
    SYSTEM = 'System'
    choices = (GETCLEVER, SYSTEM)
    

class Status(object):
    INVALID = 0
    VALID = 1
    choices = (VALID, INVALID)


class ZipFileStatus(object):
    
    Unused = (2, 'Unused')
    Importing = (3, 'Importing')
    Imported = (4, 'Imported')
    Failed = (5, 'Failed')
    
    choices = (Unused, Importing, Imported, Failed)
    
    
class ImportStatus(object):
    
    Queued = (2, 'Queued')
    Importing = (3, 'Importing')
    Finished = (4, 'Finished')
    Failed = (5, 'Failed')
    
    choices = (Queued, Importing, Finished, Failed)
    
    
class Ext(object):
    ZIP = 'zip'
    TXT = 'txt'
    
    @staticmethod
    def isZip(ext):
        return Ext.ZIP 
