# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
import json

from flask.blueprints import Blueprint
from flask.globals import g, request

from reliam.common.interceptors import no_auth_required
from reliam.common.orm import PaginateHelper
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Template, TemplateForm, Token
from flask_login import current_user
from reliam.common.exceptions import FriendlyException


bp_template = Blueprint('template', __name__)


#===============================================================================
# @bp_template.route('/', methods=['POST'])
# @smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
# @no_auth_required()
# def create_template():    
#     # we dont need wtf-form any more, 
#     # from 0.8.1 on, mongoengine supports from_json directly
#     template = Template.from_json(request.data)
#     template.save()
#     return template
#===============================================================================


def save_or_update(template, formdata=None):
    formjson = json.loads(request.data)
    tokens = [Token.from_json(json.dumps(token)) 
                for token in formjson.pop('tokens')]
    
    template_form = TemplateForm(g.formdata)
    if not template_form.validate():
        raise FriendlyException(100, template_form.errors)
    
    template_form.populate_obj(template)
    # TODO need to validate tokens
    template.tokens = tokens
    template.save()
    
    return template


@bp_template.route('/', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def create_template():
    return save_or_update(Template())


@bp_template.route('/<template_id>', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_template(template_id):
    template = Template.objects.get_or_404(id=template_id,
                                           created_by=current_user.id)
    return save_or_update(template)


@bp_template.route('/<template_id>', methods=['DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def delete_template(template_id):
    template = Template.objects.get_or_404(id=template_id,
                                           created_by=current_user.id)
    template.delete()
    return True


@bp_template.route('/', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_template_list():
    paginate = Template.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE,
        where=PaginateHelper.owner_mixin_filter()
    )
    return paginate


@bp_template.route('/<template_id>', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_template(template_id):
    template = Template.objects.get_or_404(id=template_id,
                                           created_by=current_user.id)
    return template


@bp_template.route('/<template_id>/tokens', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_token(template_id):
    ''' blueprint for update token '''
    
    template = Template.objects.get_or_404(id=template_id,
                                           created_by=current_user.id)
    
    formjson = json.loads(request.data)
    tokens = [Token.from_json(json.dumps(token))
                for token in formjson.pop('tokens')]
    
    template.tokens = tokens
    template.save()
    
    return True
