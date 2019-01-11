from flask_restplus import reqparse

youtube_search_params = reqparse.RequestParser()
youtube_search_params.add_argument('search',type=str,help='Search string')
youtube_search_params.add_argument('max',type=int,help='Max results')

ytlc = reqparse.RequestParser()
ytlc.add_argument('nextToken', type=str, default=None, help='Next page Token')


