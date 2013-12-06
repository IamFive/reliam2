# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
import datetime
import hashlib
import os

from flask.blueprints import Blueprint
from flask.globals import g, current_app
from flask_login import current_user

from reliam.common.exceptions import FriendlyException
from reliam.common.orm import PaginateHelper, PaginationMixin
from reliam.common.tools.humansize import size
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Recipient, RecipientForm, RecipientZip
from reliam.projects import get_ftp_base, get_ftp_path, get_zip_path
from reliam import error_code
from shutil import copyfile
from reliam.common.tools.utils import random_file_name, mkdirs
from string import lower
import csv


bp_recipients = Blueprint('recipients', __name__)


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
            ext = lower(abspath.split('.')[-1])
            if ext in legal_recipient_fileext:
                stats = os.stat(abspath)
                filestats = dict(name=f, relpath=relpath, size="{0:.1S}".format(size(stats.st_size)),
                                 _mtime=stats.st_mtime, ext=ext,
                                 mtime=datetime.datetime.fromtimestamp(stats.st_mtime))
                list_.append(filestats)
            
    list_.sort(key=lambda f:f.get('_mtime'), reverse=True)
    return PaginationMixin.from_list(list_)


@bp_recipients.route('/ftps/transfer', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def transfer():
    ''' transfer ftp file to server '''
    relpath = g.formdata.get('relpath')
    ftppath = get_ftp_path(relpath)
    
    stats = os.stat(ftppath)
    md5 = hashlib.md5(open(ftppath, 'rb').read()).hexdigest()
    
    # TODO search md5 value on mongo-db
    exists = RecipientZip.objects(md5=md5, created_by=current_user.id).first()
    if exists:
        raise FriendlyException.fec(error_code.RECIPIENT_FILE_TRANSFERED);
    
    mtime = datetime.datetime.fromtimestamp(stats.st_mtime)
    name = os.path.basename(ftppath)
    size_ = stats.st_size
    ext = ftppath.split('.')[-1]
    
    # copy file, rename file with extra random string
    zipfile_name = random_file_name(name)
    zipfile_path = get_zip_path(zipfile_name)
    mkdirs(zipfile_path)
    copyfile(ftppath, zipfile_path)
    
    rz = RecipientZip(name=name, size_=size_, ext=ext, md5=md5,
                      upload_on=mtime, original_path=ftppath,
                      path=zipfile_name, size='{0:.1S}'.format(size(size_)))
    rz.save()
    return True
    
    

@bp_recipients.route('/zips', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_zip_list():
    paginate = RecipientZip.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE,
        where=PaginateHelper.owner_mixin_filter()
    )
    return paginate

@bp_recipients.route('/zips/<zip_id>/import', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_zip(zip_id):
    zip = RecipientZip.objects.get_or_404(id=zip_id,
                                          created_by=current_user.id)
    
    csv.reader()
    # TODO, need to analyse zip file
    
    
    return zip
