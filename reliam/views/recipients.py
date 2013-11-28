# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from flask.globals import g
from flask_login import current_user

from reliam.common.exceptions import FriendlyException
from reliam.common.orm import PaginateHelper
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Recipient, RecipientForm


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
