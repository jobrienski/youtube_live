# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name,bad-continuation
"""
Livestream resources
--------------
"""

import logging

from flask import current_app as app
from flask_restplus import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from liveapi.services.youtube import YoutubeLiveStreamService,YoutubeChatService
from .params import youtube_search_params, ytlc
from .schemas import api,model_chat_messages,model_chat_details

log = logging.getLogger(__name__)


@api.route('/live')
@api.response(404,'No live videos found')
class YoutubeLiveSearch(Resource):
    @api.expect(youtube_search_params)
    def get(self):
        '''
        Search for live videos
        '''
        args = youtube_search_params.parse_args()

        return YoutubeLiveStreamService.get_livestreams(app.config['GOOGLE_API_KEY'],args['search'],
                                                        args['max'])


@api.route('/videos/<string:video_id>/live_chat')
@api.param('video_id','The video id')
@api.response(404,'Video not found or live chat unavailable')
@api.response(200,"json")
class LiveChatFromVideo(Resource):
    @api.marshal_with(model_chat_details,skip_none=True)
    @jwt_required
    def get(self,video_id):
        '''
        Get live chat resource information from video ID
        '''
        result = YoutubeChatService.livechat_resource_from_video_id(video_id)
        if not result:
            api.abort(404,"Live chat resource not found")
        return result


@api.route('/live_chats/<string:chat_id>/messages')
@api.param('chat_id','The chat id')
@api.response(404,'Live chat unavailable')
@api.response(403,'Not authorized')
@api.response(200,"json")
class LiveChatMessages(Resource):
    @api.doc('Get chat messages.')
    @api.expect(ytlc)
    @api.marshal_with(model_chat_messages,skip_none=True)
    @jwt_required
    def post(self,chat_id):
        '''
        Get Live Chat messages
        '''
        # disable tracking
        # identity = get_jwt_identity()
        # track_list = redis_store.get(f'tracking-{identity}')
        args = ytlc.parse_args()
        npt = args.get("nextToken", None)

        result = YoutubeChatService.livechat_messages(chat_id, next_page_token=npt)
        if not result   :
            api.abort(404,"No messages")

        return result


@api.route('/channel/<string:channel_id>')
@api.param('channel_id','Channel id')
@api.response(404,"Channel not found")
@api.response(200,"json")
class ChannelInfoByChannelId(Resource):
    @api.doc('Get channel info for channel id.',params={'channel_id':'Channel id- always email'})
    def get(self,channel_id):
        '''
        Get Channel information
        '''
        channel_info = YoutubeChatService.channel_info_by_id(channel_id)
        if not channel_info:
            api.abort(404,"Channel not found")

        return channel_info
