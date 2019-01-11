from flask_jwt_extended import (jwt_refresh_token_required,get_jwt_identity,
                                create_access_token,get_jti,jwt_required,
                                get_raw_jwt)
from flask_restplus import Resource

from .schemas import AuthDto
from ...extensions import blacklist_store

api = AuthDto.api
_token_model = AuthDto.jwt_token_model


@api.route('/refresh', methods=['POST'])
@api.response(201, 'Refreshed baby')
@api.response(403, 'Unauthorized')
class AuthTokenRefresh(Resource):
    # TODO: You can currently refresh after logging out - is that right?
    @api.doc("Refresh token must be in X-API-KEY")
    @jwt_refresh_token_required
    def post(self):
        '''

        Returns:
            new access token
        '''
        current_user = get_jwt_identity()
        if not current_user:
            api.abort(403)
        access_token = create_access_token(identity=current_user)
        access_jti = get_jti(encoded_token=access_token)
        blacklist_store.set(access_jti,
                            'false')  # TODO: make sure jti is always same based on
        # identity

        return access_token

@api.doc("Check the current token")
@api.response(200, "Token is valid")
@api.response(403, "Unauthorized or blacklisted token")
@api.route("/authorized")
class Authorized(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']

        blacklist = blacklist_store.get(jti)
        if blacklist and blacklist == 'true':
            api.abort(403)

        return "valid"

@api.doc("Logout the current user.")
@api.route("/logout", methods=['DELETE'])
class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        if jti:
            blacklist_store.set(jti, 'true')
        return {"msg":"Access token revoked"}, 200



# callback_model = api.model('auth_redirect_code', {
#     'code':        fields.String(required=True, description='The authorization token'),
#     'scope':       fields.String(required=True, description='Requested scope'),
#     'sessionState':fields.String(required=False, description='State'),  # TODO: fix
#     'prompt':      fields.String(required=False, description='Prompt')
# })
#
#
# @api.route('/google/callback')
# @api.param('<string:code>', description='Authorization code', _in='query')
# class GoogleOauthRedirect(Resource):
#     """
#         Google callback
#     """
#     @api.doc('Callback')
#     def get(self, code):
#         # get the post data
#         flow, auth_url = Flow.from_client_config(app.config['GOOGLE_CONFIG'])
#         flow.fetch_token(code=code)
#         credentials = flow.credentials
#         return redirect(auth_url)
#
#
# @api.route('/logout')
# class LogoutAPI(Resource):
#     """
#     Logout Resource
#     """
#     @api.doc('logout a user')
#     def post(self):
#         # get auth token
#         auth_header = request.headers.get('Authorization')
#         return Auth.logout_user(data=auth_header)
