# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#

from flask.blueprints import Blueprint
from flask_login import current_user

from reliam.common.interceptors import no_auth_required
from reliam.common.web.renderer import smart_render
from reliam.constants import DEFAULT_RENDER_EXCLUDE


bp_profile = Blueprint('profile', __name__)

exclude = list(DEFAULT_RENDER_EXCLUDE)
exclude.extend(('password', 'verify_code'))

@bp_profile.route('/me', methods=['GET'])
@smart_render(exclude=exclude)
@no_auth_required()
def me():
    """ get logined user detail info """
    result = dict(has_login=False)
    if current_user.is_authenticated():
        result.update(dict(has_login=True,user=current_user.get()))
    return result


