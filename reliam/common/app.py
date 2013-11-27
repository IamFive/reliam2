# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#

from flask import Flask, render_template, request
from flask.globals import current_app, g
from flask.wrappers import Response
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from mongoengine.connection import get_db
from mongoengine.errors import ValidationError
from pymongo.errors import PyMongoError
from reliam import version_context_processor
from reliam.common import error_code
from reliam.common.exceptions import FriendlyException
from reliam.common.flask_login_ext import load_user
from reliam.common.interceptors import no_auth_required, setup_auth_interceptor, \
    setup_formdata_interceptor, setup_render_as_interceptor
from reliam.common.tools.env import ResourceLoader
from reliam.common.tools.utils import mkdirs
from reliam.common.web.context_processor import utility_processor
from reliam.common.web.renderer import smart_render, JsonResp, RenderFormat, \
    ContentType
from reliam.constants import ROOT, STATIC_URL_PATH

import json
import os
from reliam.common.middleware.crossdomain import CrossOriginResourceSharing
import re


app = None

def init_mongo_engine():
    app.mongo_db = MongoEngine(app)
    

def init_logger():

    log_format = app.config.get('LOG_FORMAT')
    if app.config.get('LOG_FORMAT'):
        app.debug_log_format = log_format

    # setup root log format - global filter.
    app.logger.setLevel(app.config.get('LOGGER_ROOT_LEVEL'))
    log_file_folder = app.config.get('FILE_LOG_HANDLER_FODLER')
    mkdirs(log_file_folder, is_folder=True)

    filename = os.path.join(log_file_folder, app.import_name + '.log')
    file_handler = TimedRotatingFileHandler(filename=filename, when="midnight",
                                            backupCount=10)
    file_handler.suffix = "%Y%m%d"
    file_handler.setLevel(app.config.get('FILE_LOG_HANDLER_LEVEL'))
    file_handler.setFormatter(Formatter(log_format))
    
    app.logger.addHandler(file_handler)


def init_bp_modules():
    """add blueprint modules.
    """
    global app

    from reliam.views.authorize import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/api/authorize')

    from reliam.views.profile import bp_profile
    app.register_blueprint(bp_profile, url_prefix='/api/profile')
    
    from reliam.views.campaigns import bp_campaigns
    app.register_blueprint(bp_campaigns, url_prefix='/api/campaigns')
    
    from reliam.views.templates import bp_template
    app.register_blueprint(bp_template, url_prefix='/api/templates')
 
#     from reliam.views.guides import bp_guide
#     app.register_blueprint(bp_guide, url_prefix='/api/guilds')

    @app.route('/api/version', methods=['GET'])
    @no_auth_required()
    @smart_render()
    def version_handler():
        from reliam import version
        return version()


def init_login_manager():
    login_manager = LoginManager()
    login_manager.setup_app(app)
    login_manager.user_callback = load_user
    login_manager.REMEMBER_COOKIE_DOMAIN = load_user
    

def init_jinja_env():
    app.context_processor(utility_processor)
    app.context_processor(version_context_processor)


def init_error_handler():


    def handler_ex(ex, status=400):

        status = ex.code if ex.code >= 400 and ex.code < 500 else 400

        if g.rformat == RenderFormat.HTML:
            return render_template('{}.html'.format(status), error=ex), status

        if isinstance(ex, FriendlyException) and len(ex.msg_list) == 1:
            message = ex.msg_list[0]
        else:
            message = ex.msg_list
        resp = json.dumps(JsonResp.make_failed_resp(ex.code, message))

        if g.rformat == RenderFormat.JSON:
            return Response(resp, mimetype=ContentType.JSON), status
        elif g.rformat == RenderFormat.JSONP:
            callback = request.args.get('callback', False)
            if callback:
                content = "{}({})".format(callback, resp)
                return Response(content, mimetype=ContentType.JSONP,
                                status=200)
            return Response(resp, mimetype=ContentType.JSON, status=200)


    @app.errorhandler(404)
    def page_not_found(error):
        ex = FriendlyException.fec(error_code.RESOURCE_NOT_EXIST)
        return handler_ex(ex, 404)

    @app.errorhandler(FriendlyException)
    def friendly_ex_handler(ex):
        status = ex.code if ex.code >= 400 and ex.code < 500 else 400
        return handler_ex(ex, status=status)

    @app.errorhandler(ValidationError)
    def form_validata_ex_handler(error, status=400):
        ex = FriendlyException(400, error.to_dict())
        return handler_ex(ex, status)

    @app.errorhandler(PyMongoError)
    def mongo_op_ex_handler(error, status=400):
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)

    @app.errorhandler(Exception)
    def exception_handler(error, status=400):
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)


def init_interceptors():
    setup_render_as_interceptor(app)
    setup_auth_interceptor(app)
    setup_formdata_interceptor(app)


def setup_flask_initial_options():

    static_folder = ResourceLoader.get().configs.get('STATIC_FOLDER')
    template_folder = ResourceLoader.get().configs.get('TEMPLATE_FOLDER')
    if not static_folder:
        static_folder = os.path.join(ROOT, 'static')

    if not template_folder:
        template_folder = os.path.join(ROOT, 'templates')

    options = dict(static_url_path=STATIC_URL_PATH)
    options['static_folder'] = static_folder
    options['template_folder'] = template_folder
    return options



def init_middlewares():
    allowed = (
        'http://127.0.0.1:9000/',
        'http://localhost:9000/',  # Exact String Compare
        re.compile("^http([s]*):\/\/localhost([\:\d]*)$"),  # Match a regex
    )
    
    # Add Access Control Header
    cors = CrossOriginResourceSharing(app)
    cors.set_allowed_origins(*allowed)


def startup_app():

    # initial settings first, or change to use confd like curupira?
    global app

    if not app:
        args = setup_flask_initial_options()
        app = Flask('Reliam', **args)

        app.config.update(ResourceLoader.get().configs)
        app.debug = app.config.get('DEBUG', False)

        init_logger()

        try:
            init_mongo_engine()
            init_jinja_env()
            init_error_handler()
            init_login_manager()
            init_interceptors()
            
            # middle ware is the same as interceptor indeed, :)
            init_middlewares()
            init_bp_modules()
            app.logger.info('Start success from ROOT [%s]', ROOT)
        except Exception, e:
            app.logger.error('Start Reliam faild!')
            app.logger.exception(e)
            raise e
        
    return app

def init_db():
    with current_app.app_context():
        folder_name = app.config.get('INIT_DATA_FOLDER_NAME')
        folder_path = ResourceLoader.get().get_resoure(folder_name).path
        if folder_path and os.path.isdir(folder_path):
            for data_file in os.listdir(folder_path):
                with open(folder_path + os.path.sep + data_file, 'r') as mqls:
                    get_db().eval(mqls.read())

def clear_db():
    with current_app.app_context():
        get_db().eval('db.dropDatabase()')
