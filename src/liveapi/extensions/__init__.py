# -*- coding: utf-8 -*-
"""
Extensions: Here be all the extensions used in the app
------------------------------------------------------
"""

from flask_bcrypt import Bcrypt
from flask_session import Session

# This is for hashing passwords
bcrypt = Bcrypt()

# pretty, pretty colored logging: muay linda
from ._logging import Logging

logging = Logging()

# cross origin resources allowed
from flask_cors import CORS

cross_origin_resource_sharing = CORS()

# ahh yeahh - Flask SQLAlchemy in the hizzouse.
from ._flask_sqlalchemy import SQLAlchemy
from liveapi.models_base import DeclarativeBase

db = SQLAlchemy(model_class=DeclarativeBase)

# flask caching
# TODO: redundant - added redis store before
from flask_caching import Cache

cache = Cache()

# redis store
from ._redis_store import _RedisStore as RedisStore

redis_store = RedisStore()

# session
session = Session()

# JWT
from ._flask_jwt import _jwt as jwt

# Redis For token blacklist
from ._token_store import (_BLStore as BLStore,_GoogleTokenStore as GoogleTokenStore)

blacklist_store = BLStore(redis_store)
google_store = GoogleTokenStore(redis_store)

# Google auth helper
from ._google_oauth2 import _goog_auth_helper as goog_auth_helper


# utils
# from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
# force_auto_coercion()
# force_instant_defaults()


def init_app(app,tconfig) -> None:
    """ Init extensions - loop through all these guys and call their init_app methods.
    This is the factory method.
    Notes: I think it's best for api to be last.
    Args:
        app (Flask):
        tconfig (BaseConfig object from `baseconfig.py`): DevelopmentConfig or
        ProductionConfig
        or TestingConfig
    """
    # logging,
    for extension in (
            bcrypt,  # TODO: cryptophy the oauth2 tokens
            cache,
            cross_origin_resource_sharing,
            db,
            jwt,
            redis_store,
            session,
            blacklist_store,
            google_store,  # TODO: expirations
            goog_auth_helper
    ):
        # if extension == logging:
        #     extension.init_app(app, tconfig)
        # else:
        extension.init_app(app)
