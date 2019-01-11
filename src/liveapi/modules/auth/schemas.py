from flask_restplus import Namespace,fields


class AuthDto:
    api = Namespace('auth',description="Authentication")
    jwt_token_model = api.model('jwt_token_model',{
        'access_token': fields.String(required=True,description='JWT Access Token'),
        'refresh_token':fields.String(required=False,description='JWT Refresh Token')
    })
