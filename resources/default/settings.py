# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

import os
from reliam.constants import ROOT, STATIC_URL_PATH

#------------- Application setting here. ---------------------

DEBUG = False
CSRF_ENABLED = False
WTF_CSRF_ENABLED = False
SECRET_KEY = 'SimpleKEy'

MEDIA_URL_PATH = '/m'
MEDIA_FOLDER = os.path.join(ROOT, 'medias')

INIT_DATA_FOLDER_NAME = 'init-mqls'

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'reliam'

LOGGER_ROOT_LEVEL = 'DEBUG'
FILE_LOG_HANDLER_FODLER = os.path.join(ROOT, 'logs')
FILE_LOG_HANDLER_LEVEL = 'DEBUG'
LOG_FORMAT = (
    '[%(asctime)s] %(levelname)s *%(pathname)s:%(lineno)d* : %(message)s'
)


RAW_RESOURCE_PATH = [MEDIA_URL_PATH, STATIC_URL_PATH]
RAW_RESOURCE_ENDWITH = ['.css', '.js', '.jpg', '.ico', '.png']

# when deploy, should remove
STATIC_FOLDER = r'E:\git\prophet\app'
# STATIC_FOLDER = r'E:\git\prophet\dist'

LEGAL_RECIPIENT_FILE_EXT = ['zip', 'txt', 'csv']

FTP_PATH = r'E:\git\reliam2\nfs\ftp'
USERFILES_PATH = r'E:\git\reliam2\nfs\userfiles'


#===============================================================================
# Celery
#===============================================================================
BROKER_URL = 'mongodb://{}:{}/celery'.format(MONGODB_HOST, MONGODB_PORT)


#===============================================================================
# Celery beat configuration part
#===============================================================================
#===============================================================================
# from datetime import timedelta
# CELERYBEAT_SCHEDULE = {
#    'Update Task Status': {
#        'task': 'test_task',
#        'schedule': timedelta(seconds=15),
#    },
# }
# CELERY_TIMEZONE = 'UTC'
# CELERY_IMPORTS = ('reliam.tasks',)
#===============================================================================

#
# CELERYD_LOG_FILE = os.path.join(ROOT, 'logs', 'celeryd.log')
