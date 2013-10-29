# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from flask.globals import g, request

from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE
from reliam.models import Campaign, CampaignForm


bp_campaign = Blueprint('campaign', __name__)


def save_or_update(campaign, formdata=None):
    campaign_form = CampaignForm(formdata or g.formdata)
    campaign_form.populate_obj(campaign)
    campaign.save()
    return campaign


@bp_campaign.route('/', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def create_campaign():
    return save_or_update(Campaign())


@bp_campaign.route('/<campaign_id>', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id)
    return save_or_update(campaign)


@bp_campaign.route('/<campaign_id>', methods=['DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def delete_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id)
    campaign.delete()
    return True


@bp_campaign.route('/', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_campaign_list():
    paginate = Campaign.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE
    )
    return paginate


@bp_campaign.route('/<campaign_id>', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_campaign(campaign_id):
    campaign = Campaign.objects.get_or_404(id=campaign_id)
    return campaign
