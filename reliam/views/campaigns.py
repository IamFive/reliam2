# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from flask.globals import g, request, current_app

from reliam.common.exceptions import FriendlyException
from reliam.common.orm import PaginateHelper
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Campaign, CampaignForm, Template
from flask_login import current_user
from reliam import error_code


bp_campaigns = Blueprint('campaigns', __name__)

'''
    now, I didn't add any op validation, 
    will add when requirement is more clear
'''


def save_or_update(campaign, formdata=None):
    campaign_form = CampaignForm(formdata or g.formdata)
    campaign_form.populate_obj(campaign)
    
    if not campaign_form.validate():
        raise FriendlyException(100, campaign_form.errors)
    
    campaign.save()
    return campaign


@bp_campaigns.route('/', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def create_campaign():
    return save_or_update(Campaign())


@bp_campaigns.route('/<campaign_id>', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id,
                                           created_by=str(current_user.id))
    return save_or_update(campaign)


@bp_campaigns.route('/<campaign_id>', methods=['DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def delete_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id,
                                           created_by=current_user.id)
    campaign.delete()
    return True


@bp_campaigns.route('/', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_campaign_list():
    paginate = Campaign.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE,
        where=PaginateHelper.owner_mixin_filter()
    )
    return paginate


@bp_campaigns.route('/<campaign_id>', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id,
                                           created_by=current_user.id)
    return campaign



@bp_campaigns.route('/<campaign_id>/tpls/<tpl_id>', methods=['POST', 'DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def add_tpl(campaign_id, tpl_id):
    '''
    '''
    campaign = Campaign.objects.get_or_404(id=campaign_id,
                                           created_by=current_user.id)
    
    try:
        template = Template.objects.get_or_404(id=tpl_id,
                                           created_by=current_user.id)
    except Exception, e:
        msg = "Error occurs when manage tpl for campaign: {}"
        current_app.logger.warn(msg.format(e.message))
        raise FriendlyException.fec(error_code.INVALID_PARAM, 'tpl_id')
    else:
        if request.method == "POST":
            campaign.update(add_to_set__templates=template)
            return campaign
        elif request.method == "DELETE":
            campaign.update(pull__templates=template)
            return campaign
