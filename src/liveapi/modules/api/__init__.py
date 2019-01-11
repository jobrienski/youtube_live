"""
API for registering blueprints and namespace
-------------------------------------------
"""
import types

from flask_restplus import Api
from flask_restplus.apidoc import apidoc
from flask import Blueprint, url_for
from baseconfig import URL_PREFIX

authorizations = {
    'apikey':{
        'type':'apiKey',
        'in':  'header',
        'name':'X-API-KEY'
    }
}

api_v1_blueprint = Blueprint('api', __name__)
api_v1 = Api(  # pylint: disable=invalid-name
        api_v1_blueprint,
        authorizations=authorizations,
        security='apikey',
        version='1.0',
        title="StreamLabs Youtube Api",
        doc='/doc/',
        prefix=URL_PREFIX,
        description=
        f'<p>Youtube Live Streams api with authentication and authorization.</p> '
        f'<p>Swagger is wrong - the api has a prefix of {URL_PREFIX}.</p>'
        f'<p>To '
        f'get an api key, click on <a href="/api/v1/auth/login?return_keys=1" target="_blank">login ['
        f'opens in new tab]</a></p>'
        f'<p>To logout - go to <a href="/api/v1/auth/logout" target="_blank" method="delete">logout</a>, or click on the "authorize" button,'
        f'and click logout.'
        '<p>Athorize like this - Bearer the_api_key_you_got_from_login</p>'
        ,
)

# override help on 404
def new_help_on_404(self, message=None):
    return message if message else ""

api_v1._help_on_404 = types.MethodType(new_help_on_404, api_v1)


def init_app(app, **kwargs) -> None:
    """ Create /api/v1 blueprint and add it to the api extension,
    and add it to the Flask app.
    Args:
        app (Flask):
        **kwargs (dict): unused
    """
    from ..auth.resources import api as authapi
    from ..auth.views import auth_blueprint as auth_blueprint
    from ..user.resources import api as userapi
    from ..track.resources import api as trackapi
    from ..streams.resources import api as livestreams_api
    from ...extensions import jwt
    # pylint: disable=unused-argument

    # = Blueprint('api', __name__, url_prefix=URL_PREFIX)
    api_v1.add_namespace(authapi)
    api_v1.add_namespace(userapi)
    api_v1.add_namespace(livestreams_api)
    api_v1.add_namespace(trackapi)
    jwt._set_error_handler_callbacks(api_v1)
    app.register_blueprint(api_v1_blueprint)
    app.register_blueprint(auth_blueprint)

    @apidoc.add_app_template_global
    def swagger_static(filename):
        url = url_for('static', filename='static/{0}'.format(filename))
        return url
