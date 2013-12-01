# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from flask.globals import g, current_app
from flask_login import current_user

from reliam.common.exceptions import FriendlyException
from reliam.common.orm import PaginateHelper, PaginationMixin
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Recipient, RecipientForm, RecipientZip
import os
import datetime
from reliam.common.tools.humansize import size


bp_recipients = Blueprint('recipients', __name__)


def get_ftp_base():
    ''' get ftp base path for current user '''
    user = current_user.get()
    ftp_path = current_app.config.get('FTP_PATH')
    ftp_folder = os.path.abspath(os.path.join(ftp_path, user.email))
    return ftp_folder


def save_or_update(recipient, formdata=None):
    recipient_form = RecipientForm(formdata or g.formdata)
    recipient_form.populate_obj(recipient)
    
    if not recipient_form.validate():
        raise FriendlyException(100, recipient_form.errors)
    
    recipient.save()
    return recipient


@bp_recipients.route('/', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def create_recipient():
    return save_or_update(Recipient())


@bp_recipients.route('/<recipient_id>', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_recipient(recipient_id):
    recipient = Recipient.objects.get_or_404(id=recipient_id,
                                           created_by=str(current_user.id))
    return save_or_update(recipient)


@bp_recipients.route('/<recipient_id>', methods=['DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def delete_recipient(recipient_id):
    recipient = Recipient.objects.get_or_404(id=recipient_id,
                                           created_by=current_user.id)
    recipient.delete()
    return True


@bp_recipients.route('/', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_recipient_list():
    paginate = Recipient.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE,
        where=PaginateHelper.owner_mixin_filter()
    )
    return paginate


@bp_recipients.route('/<recipient_id>', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_recipient(recipient_id):
    recipient = Recipient.objects.get_or_404(id=recipient_id,
                                           created_by=current_user.id)
    return recipient



@bp_recipients.route('/zips', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_zip_list():
    paginate = Recipient.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE,
        where=PaginateHelper.owner_mixin_filter()
    )
    return paginate


@bp_recipients.route('/ftps', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_ftp_list():
    ''' get all ftp files'''
    list_ = []
    ftp_folder = get_ftp_base()
    legal_recipient_fileext = current_app.config.get('LEGAL_RECIPIENT_FILE_EXT')
    for root, _, files in os.walk(ftp_folder):
        for f in files:
            abspath = os.path.abspath(os.path.join(root, f))
            relpath = os.path.relpath(abspath, ftp_folder)
            ext = abspath.split('.')[-1]
            if ext in legal_recipient_fileext:
                stats = os.stat(abspath)
                filestats = dict(name=f, relpath=relpath, size="{0:.1S}".format(size(stats.st_size)),
                                 _mtime=stats.st_mtime, ext=ext,
                                 mtime=datetime.datetime.fromtimestamp(stats.st_mtime))
                list_.append(filestats)
            
    list_.sort(key=lambda f:f.get('_mtime'), reverse=True)
    return PaginationMixin.from_list(list_)
    
