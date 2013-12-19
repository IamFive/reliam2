# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-6-16
#

#===============================================================================
# [uwsgi]
# # Variables
# base = /var/www/hive
# app = run_hive
# # Generic Config
# plugins-dir=/usr/lib/uwsgi/plugins
# plugins = http,python
# #home = %(base)/venv
# pythonpath = %(base)
# chown-socket = www-data
# socket=/tmp/uwsgi.hive.socket
# chown-socket = www-data
# module = %(app):application
# callable = app
# logto = /var/log/uwsgi/%n.log
#===============================================================================


__test__ = False

from reliam.common.app import startup_app
from reliam.common.tools.env import ResourceLoader
import os

os.environ.setdefault(ResourceLoader.ENV_VAR_NAME,
                      '/home/www-data/reliam2/resources/prod')
application = startup_app()
