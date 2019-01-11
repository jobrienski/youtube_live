# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name,bad-continuation
"""
User resources
--------------
"""

import logging

from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_restplus import Resource

from ...services.users import UserService
from .schemas import UserDto

log = logging.getLogger( __name__ )
api = UserDto.api
_user = UserDto.user


@api.route('/me')
@api.response(404, 'Not logged in or signed up')
class UserMe(Resource):
    @api.doc('The currently logged in user.')
    @api.marshal_with(_user)
    @jwt_required
    def get(self):
        '''
        Get currently logged in user by jwt identity
        Returns:
            json
        '''
        google_id = get_jwt_identity()
        if not google_id:
            api.abort(404)
        user = UserService.find_by_google_id(google_id)
        if not user:
            api.abort(500, "Database error - try logging in again.")

        return user


@api.route('/<string:google_id>')
@api.param('google_id', 'The google profile id')
@api.response(404, 'User not found.')
class UserByGoogleId(Resource):
    @api.doc('Find a user by google profile id', params={'google_id': 'The google profile id'})
    @api.marshal_with(_user)
    def get(self, google_id):
        """get a user given its identifier"""
        user = UserService.find_by_google_id(google_id)

        if not user:
            api.abort(404)
        else:
            return user

@api.route('/by_username/<string:username>')
@api.param('username', 'The Username- always email')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('Find a user by username', params={'username': 'Username - always email'})
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its identifier"""
        user = UserService.find_by_username(username)
        if not user:
            api.abort(404)
        else:
            return user
