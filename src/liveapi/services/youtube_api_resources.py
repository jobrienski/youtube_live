import json
import logging

import urllib3
from box import Box
from googleapiclient.discovery import build


class Scopes:
    YOUTUBE_READONLY = "https://www.googleapis.com/auth/streams.readonly"


class YoutubeReadOnlyService:
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

class Fields:
    GOOGLE_VIDEO_LIVE_CHAT = "items(liveStreamingDetails)"
    GOOGLE_CHAT_LIST = "items(authorDetails(channelId,displayName,isChatModerator,isChatOwner,isChatSponsor,profileImageUrl),id,snippet(authorChannelId,publishedAt,superChatDetails/userComment,textMessageDetails)),nextPageToken,pollingIntervalMillis"


class Endpoints:
    GOOGLE_PROFILE = 'https://www.googleapis.com/userinfo/v2/me'  # Profile
    GOOGLE_PLUS = 'https://www.googleapis.com/auth/plus.me'  # Know who you are on google
    GOOGLE_LIVE_CHAT_MESSAGES = "https://www.googleapis.com/streams/v3/liveChat/messages"
    GOOGLE_BROADCASTS = "https://www.googleapis.com/streams/v3/liveBroadcasts"
    GOOGLE_VIDEO_LIVE_CHAT = "https://www.googleapis.com/youtube/v3/videos?part" \
                                "=liveStreamingDetails&id={}&fields={}&key={}"
    GOOGLE_LIVE_CHAT_LIST = "https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={" \
                            "}&part=snippet%2CauthorDetails&fields={}&key={}"
    GOOGLE_CHANNEL_FOR_USERNAME="https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={}&fields=items(id%2CtopicDetails)&key={}"

    GOOGLE_CHANNEL_BY_CHANNEL_ID ="https://www.googleapis.com/youtube/v3/channels?part=snippet,contentOwnerDetails&id={}&key={}"


class GoogleResourceBuilder:
    @staticmethod
    def build(sclass, credentials=None, scopes=None):
        '''
        Args:
            sclass (Class): service class
            credentials (Credentials): oauth creds

        Returns:
            googleapiclient.discovery.Resource
        '''
        if not scopes and sclass.API_SCOPES:
            credentials.scopes = sclass.API_SCOPES

        return build(sclass.API_SERVICE_NAME,sclass.API_VERSION,credentials=credentials)

    @staticmethod
    def build_readonly(sclass, developer_key):
        return build(sclass.API_SERVICE_NAME, sclass.API_VERSION, developerKey=developer_key)

    @staticmethod
    def build_youtube_readonly(developer_key):
        return GoogleResourceBuilder.build_readonly(YoutubeReadOnlyService, developer_key=developer_key)


class Requestor:
    manager = urllib3.PoolManager()

    class Responder:
        def __init__(self, payload):
            self.payload = payload

        def value(self):
            return self.payload

        def to_json(self):
            '''

            Args:
                payload ():

            Returns:
            Raises: json.JSONDecodeError
            '''
            self.payload = json.loads(self.payload.decode("utf-8"))
            return self

        def to_box(self):
            self.payload = Box(self.payload,default_box=True,default_box_attr=None)
            return self


    @classmethod
    def get_data(cls,url):
        '''

        Args:
            url ():

        Returns: Responder
        Raises: urllib3.exceptions.HTTPError
        '''
        try:
            r = cls.manager.request('GET',url)
            return cls.Responder(r.data)
        except urllib3.exceptions.HTTPError as exc:
            logging.error(exc)
            raise (exc)