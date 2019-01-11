
from liveapi.extensions import db, cache
from .users import UserService
from .transactions import managedtrans
from liveapi.models import Chatterbox


class TrackService:

    @staticmethod
    @managedtrans()
    @cache.memoize()
    def set_tracking(identity, display_name, channel_id=None):
        user = UserService.find_by_google_id(identity)
        if not user:
            raise Exception("Identity user not found")

        if channel_id:
            chatterbox = user.tracked_fools.first(Chatterbox.channel_id == channel_id)
        else:
            chatterbox = user.tracked_fools.first(Chatterbox.display_name == display_name)

        if  not chatterbox:
            chatterbox = Chatterbox(display_name=display_name, channel_id=channel_id, tracker_id=user.id)

        db.session.add(chatterbox)

        return chatterbox   # for caching

    @staticmethod
    def update_tracking_from_message(identity, message):
        '''

        Args:
            identity ():
            message (model_chat_messages):

        Returns:

        '''
        pass
