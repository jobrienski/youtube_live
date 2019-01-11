# -*- coding: utf-8 -*-

from urllib.parse import quote_plus

from flask import current_app as app

from liveapi.services.youtube_api_resources import (Fields,Endpoints,Requestor,
                                                      GoogleResourceBuilder)


class YoutubeChatService:

    @staticmethod
    def livechat_resource_from_video_id(video_id):
        """

        Args:
            video_id ():

        Returns: json
        Raises: urllib3.exceptions.HTTPError, json.JSONDecodeError

        """
        url = Endpoints.GOOGLE_VIDEO_LIVE_CHAT.format(quote_plus(video_id),
                                                      quote_plus(Fields.GOOGLE_VIDEO_LIVE_CHAT),
                                                      quote_plus(app.config['GOOGLE_API_KEY']))
        bdata = Requestor.get_data(url).to_json().to_box().value()

        if not len(bdata["items"]):
            return None

        return bdata["items"][0].liveStreamingDetails

    @staticmethod
    def livechat_messages(livechat_id, next_page_token=None):
        """

        Args:
            livechat_id ():


        Returns: String
        Raises: urllib3.exceptions.HTTPError, json.JSONDecodeError

        """
        url = Endpoints.GOOGLE_LIVE_CHAT_LIST.format(quote_plus(livechat_id),
                                                     quote_plus(Fields.GOOGLE_CHAT_LIST),
                                                     quote_plus(app.config['GOOGLE_API_KEY']))
        if next_page_token:
            url = f"{url}&pageToken={next_page_token}"
        print(livechat_id)
        print(next_page_token)
        print(url)
        return Requestor.get_data(url).to_json().value()

    @staticmethod
    def channel_id_for_display_name(display_name):
        """

        Args:
            username ():


        Returns: String
        Raises: urllib3.exceptions.HTTPError, json.JSONDecodeError

        """
        url = Endpoints.GOOGLE_CHANNEL_FOR_USERNAME.format(quote_plus(display_name),
                                                           quote_plus(app.config['GOOGLE_API_KEY']))
        result = Requestor.get_data(url).to_json().to_box().value()

        if not len(result["items"]):
            return None

        return result["items"][0].id

    @staticmethod
    def channel_info_by_id(channel_id):
        """

        Args:
            channel_id ():


        Returns: json
        Raises: urllib3.exceptions.HTTPError, json.JSONDecodeError

        """
        url = Endpoints.GOOGLE_CHANNEL_BY_CHANNEL_ID.format(quote_plus(channel_id),
                                                            quote_plus(
                                                                app.config['GOOGLE_API_KEY']))
        result = Requestor.get_data(url).to_json().to_box().value()

        if not len(result["items"]):
            return None

        return result["items"][0]


class YoutubeLivestreamService:
    @staticmethod
    def get_livestreams(developer_key, search_key="fortnite", max_results=10):
        youtube = GoogleResourceBuilder.build_youtube_readonly(developer_key)
        # Call the search.list method to retrieve results matching the specified
        # query term.

        args = dict(part='id,snippet',
                    maxResults=max_results,
                    relevanceLanguage="en",
                    safeSearch="moderate",
                    eventType="live",
                    type="video",
                    q=search_key,
                    videoEmbeddable="true",
                    order="relevance",
                    fields="items(id(videoId),snippet(channelId,description,liveBroadcastContent,thumbnails/default,title))")

        videos = []
        list_response = youtube.search().list(**args).execute()
        for item in list_response.get('items',[]):
            keep = { "video_id": item['id']['videoId'],
                     "title": item['snippet']['title'],
                     "thumbnail": item['snippet']['thumbnails']['default'],
                     "channel_id": item['snippet']['channelId'], #optional
                     "description": item['snippet']['description']
            }

            videos.append(keep)

        return videos
