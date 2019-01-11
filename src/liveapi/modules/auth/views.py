# coding: utf-8
"""
OAuth2 and JWT
Exchange OAuth2 token for a JWT token
Store both in redis

TODO: logout
"""
import datetime as dt
from flask import Blueprint,request,session,abort,make_response,redirect, \
    current_app as app,jsonify
from flask_jwt_extended import (create_access_token,create_refresh_token,
                                get_jti)

from baseconfig import URL_PREFIX
from liveapi.extensions import blacklist_store,google_store,goog_auth_helper,jwt
from liveapi.services.youtube_api_resources import Endpoints
from ...services.users import UserService
from liveapi.util import get_base_url

auth_blueprint = Blueprint('auth',__name__,
                           url_prefix=f'{URL_PREFIX}/auth')  # pylint: disable=invalid-name


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = blacklist_store.get(jti)
    if entry is None:
        return True
    return entry=='true'


@auth_blueprint.route(f'/login',methods=['GET'])
def api_login():
    """
    Start oauth flow by redirecting to google oauth.
    Set state in session.
    # TODO: check if token in redis
    Redirects to google oauth
    """
    # save request url
    request_env = request.environ
    return_keys = request.args.get("return_keys",False)
    session['origin'] = request.headers.get('HTTP_REFERER','http://localhost:8080')
    session['return_keys'] = return_keys
    flow = goog_auth_helper.get_flow()
    auth_url,state = goog_auth_helper.get_redir_url(flow)
    session['state'] = state
    return redirect(auth_url)


@auth_blueprint.route('/oauth2callback',methods=['GET'])
def oauth2callback():
    '''
    Returns: json jwt access_token and refresh_token
    TODO: move io-bound operations to celery
    '''
    saved_state = session['state']
    arg_state = request.args.get("state")
    if not arg_state or arg_state!=saved_state:
        abort(400,"Wrong or missing state")
    code = request.args.get("code")

    # Convert the authorization token to an access token
    flow = goog_auth_helper.get_flow(state=saved_state)
    flow.fetch_token(code=code,authorization_response=request.url)

    # fix incompatibity between google libraries
    credentials = goog_auth_helper.user_credentials_from_tokens(flow.credentials.token,
                                                                flow.credentials.refresh_token)
    auth_session = goog_auth_helper.get_authorized_session(credentials)

    # fetch user profile
    profile = auth_session.get(Endpoints.GOOGLE_PROFILE).json()

    # the key to everything
    identity = profile['id']

    # store tokens in cache
    google_store.set_tokens(identity,credentials.token,credentials.refresh_token)

    # save user if user doesn't exist
    user = UserService.find_by_google_id(identity)
    if not user:  # TODO: check if token exists
        user = UserService.save_user(profile['id'],profile['email'],profile['name'],
                                     avatar=profile['picture'])

    # create jwt access and refresh tokens
    jwt_access_token = create_access_token(identity=identity)
    jwt_refresh_token = create_refresh_token(identity=identity)

    # store in blacklist - 'false' means not revoked - 'true' means revoked
    blacklist_store.set(get_jti(encoded_token=jwt_access_token),'false')
    blacklist_store.set(get_jti(encoded_token=jwt_refresh_token),
                        'false',refresh=True)

    # return the tokens in cookie
    access_expires = dt.datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    refresh_expires = dt.datetime.utcnow() + app.config['JWT_REFRESH_TOKEN_EXPIRES']
    origin = session.get('origin','http://localhost:8080')
    return_keys = session.get('return_keys',False)
    if return_keys:
        ret_json = {"access_token":jwt_access_token,"refresh_token":jwt_refresh_token}
        return jsonify(ret_json)

    response = make_response(redirect("http://tasq.us/"))
    response.set_cookie('access_token',jwt_access_token,expires=access_expires, domain="tasq.us")
    response.set_cookie('refresh_token',jwt_refresh_token,expires=refresh_expires)

    return response
