from flask_restplus import fields,Model,Namespace

api = Namespace('ytlive',description="Youtube service")

'''
  {
   "id": "LCC.Cg8KDQoLOWx5V0c3YzFEQlkSRQoaQ01LaGlKVDAtTjBDRlJFRlpBb2RldUlQclESJ0NLRE4tb1AwLU4wQ0ZjNUNTQUFkQ2VNT3dnMTUzOTA3MjYxMTI3Nw",
   "snippet": {
    "authorChannelId": "UC9IIJHe70pezRpyMen0Mq6A",
    "textMessageDetails": {
     "messageText": "hola"
    }
   },
   "authorDetails": {
    "channelId": "UC9IIJHe70pezRpyMen0Mq6A",
    "displayName": "Jossue Leonel Pereyra Barrionuevo",
    "isChatOwner": false,
    "isChatSponsor": false,
    "isChatModerator": false
   }
  },
'''
field_author_details = api.model("AuthorDetails",{
    "channelId":fields.String(),
    "name":     fields.String(attribute='displayName'),
    "owner":    fields.Boolean(attribute='isChatOwner'),
    "moderator":fields.Boolean(attribute='isChatModerator'),
    "sponsor":  fields.Boolean(attribute='isChatSponsor')
})

field_snippet_chat_messages = api.model("Snippet",{
    "timestamp":fields.DateTime(attribute="publishedAt"),
    "message":  fields.String(attribute="textMessageDetails.messageText")
})

field_chat_messages = api.model("ChatMessage",{
    "id": fields.String(),
    "snippet":      fields.Nested(field_snippet_chat_messages),
    "authorDetails":fields.Nested(field_author_details)
})

model_chat_details = api.model("ItemChatDetails",{
    "start":  fields.DateTime(attribute="actualStartTime"),
    "viewers":fields.Integer(attribute="concurrentViewers"),
    "chat_id":fields.String(attribute="activeLiveChatId")
})

model_chat_messages = api.model("ChatDetailsList",{
    "nextPageToken":        fields.String,
    "pollingIntervalMillis":fields.Integer,
    'items':                fields.List(fields.Nested(field_chat_messages))
})

# GET https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=YouTubeDev&fields=items(
# id%2CtopicDetails)&key={YOUR_API_KEY}
# items: [{ "id"
model_channel_id_for_username = api.model("ChannelIdDisplayName",{
    "display_name":fields.String,
    "id":          fields.String
})
