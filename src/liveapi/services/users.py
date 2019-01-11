from liveapi.extensions import db,cache
from liveapi.models import User
from .transactions import managedtrans


class UserService:
    @staticmethod
    @managedtrans()
    def save_user(google_id:str, username:str, name:str, avatar=None)->User:
        '''
        Args:
            google_id ():
            username ():
            name ():
            avatar ():

        Returns: User
        '''

        user = User(google_id=google_id, name=name, username=username, avatar=avatar)
        db.session.add(user)
        return user

    # @cache.memoize()
    @classmethod
    @managedtrans()     # postgresql rolls back without commit on read
    def find_by_id(cls, id):
        return User.query.filter(User.id==id).first()

    @classmethod
    @managedtrans()
    def find_by_google_id(cls, google_id):
        return User.query.filter(User.google_id == google_id).first()

    @classmethod
    @managedtrans()
    def find_by_username(cls, username):
        return User.query.filter(User.username==username).first()
