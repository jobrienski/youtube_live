# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name,bad-continuation
"""
Livestream resources
--------------
"""

import logging

from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_restplus import Resource

from liveapi.extensions import redis_store
from .schemas import api

log = logging.getLogger(__name__)


# @api.route('/query/with/apikey')
# class QueryByUrlWithApiKey:
#     @api.expect()
#     @api.doc("Execute a query with api key")
#     def post(self):


@api.route('/<string:display_name>')
@api.param('display_name','The display name')
@api.response(500,"Decoding error")
@api.response(403,"Unauthorized")
@api.response(200,"json")
class TrackByDisplayName(Resource):
    '''
    I can't figure out a way to search livechat messages by user
    because there doesn't seem to be a way to associate the user.
    Hack is to store the display name  TODO: track by channel id
    '''

    @api.doc('Set the tracking flag on this display name.')
    @jwt_required
    def get(self,display_name):
        '''
        Returns:
            json     '''
        identity = get_jwt_identity()
        track_key = f'tracking-{identity}'

        tracking = redis_store.get(track_key)  # array
        if tracking and type(tracking)!=dict:
            api.abort(500,"Decoding error")
        elif not tracking:
            tracking = [display_name]

        tracking.append(display_name)

        redis_store.set(track_key,tracking)

        return {"message":f"Tracking the person named {display_name}"}
