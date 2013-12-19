# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#
from flask_login import current_user
from flask.globals import current_app
import os
from reliam.common.tools.utils import random_str


def get_ftp_base(user=None):
    ''' get ftp base path for current user '''
    if not user:
        user = current_user.get()
    ftp_path = current_app.config.get('FTP_PATH')
    ftp_folder = os.path.abspath(os.path.join(ftp_path, user.email))
    print ftp_folder
    return ftp_folder

def get_ftp_path(relpath, user=None):
    return os.path.abspath(os.path.join(get_ftp_base(user), relpath))


def get_zip_base(user=None):
    ''' get zip base path for current user '''
    if not user:
        user = current_user.get()
    ftp_path = current_app.config.get('USERFILES_PATH')
    ftp_folder = os.path.abspath(os.path.join(ftp_path, user.email))
    return ftp_folder

def get_zip_path(relpath, user=None):
    return os.path.abspath(os.path.join(get_zip_base(user), relpath)) 
