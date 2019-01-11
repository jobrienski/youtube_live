from flask_restplus import fields,Namespace


class UserDto:
    api = Namespace('users',description="Users")
    user = api.model('user',{
        'google_id':fields.String(required=True,description="google id"),
        "name":     fields.String(required=True,description="user's full name"),
        'username': fields.String(required=True,description='user username'),
        'avatar':   fields.String(description='Profile picture or avatar'),
    })
