# -*- coding: utf-8 -*-

import json
from operator import itemgetter


class _TokenStore:
    def __init__(self,redis_store):
        self.redis_store = redis_store

    def set(self,key,value,expiry=None):
        self.redis_store.set(key,value,expiry=expiry)

    def get(self,key):
        return self.redis_store.get(key)


class _GoogleTokenStore(_TokenStore):
    def __init__(self,redis_store):
        super().__init__(redis_store)

    # TODO: set refresh to expire after 30 days and check
    def set_tokens(self,google_id,access_token,refresh_token):
        super().set(google_id,json.dumps({"token":access_token,"refresh_token":refresh_token}))

    def get_tokens(self,google_id) -> (str,str):
        """
        Gets client oauth from redis
        Args:
            google_id ():

        Returns: Tuple(str, str)
        Raises: Exception if not found

        """
        stored = super().get(google_id)
        if stored:
            creds = json.loads(stored)
            return itemgetter("token","refresh_token")(creds)
        else:
            raise Exception("Not found")  # TODO: not found exception

    def init_app(self,app):
        pass


class _BLStore(_TokenStore):
    def __init__(self,redis_store):
        super().__init__(redis_store)
        self.access_expires = None
        self.refresh_expires = None

    def setup_expirations(self,access_expires,refresh_expires):
        self.access_expires = access_expires
        self.refresh_expires = refresh_expires

    def set(self,jti,str_revoked,refresh=False):
        expiry = (self.refresh_expires if refresh else self.access_expires) * 1.2
        super().set(jti,str_revoked,expiry=expiry)

    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    def init_app(self,app):
        app.config['JWT_BLACKLIST_ENABLED'] = True
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

        self.setup_expirations(app.config['JWT_ACCESS_TOKEN_EXPIRES'],
                               app.config['JWT_REFRESH_TOKEN_EXPIRES'])
