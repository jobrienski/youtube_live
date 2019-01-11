# -*- coding: utf-8 -*-
import json
import os


def mapenvvar(value,cast: type):
    """ Map environmental variable to type
    Args:
        value (any):
        cast (type):

    Returns: value of that type or value if can't convert

    """
    if value is None:
        return None
    if cast and cast!=bool:
        try:
            return cast(value)
        except ValueError:
            return value
    elif cast==bool:
        if value.lower()=="true" or value=="1":
            return True
        elif value.lower()=="false" or value=="0":
            return False


def fromenv(key,cast: type = None,default=None):
    """ Get value from environment, optional cast
    Args:
        key (any):
        cast (Optional[type]):

    Returns: any

    """
    value = os.environ.get(key,default=default)
    if cast:
        value = mapenvvar(value,cast)
    return value


def setenv(key,value) -> None:
    """ Set environmental variable
    Args:
        key (str):
        value (str):
    """
    os.environ[key] = value


def credentials_to_dict(credentials):
    return {
        'token':        credentials.token,
        'refresh_token':credentials.refresh_token,
        'token_uri':    credentials.token_uri,
        'client_id':    credentials.client_id,
        'client_secret':credentials.client_secret,
        'scopes':       credentials.scopes}


def unsetenv(key):
    del os.environ[key]


def pretty_json(output):
    return json.dumps(output,indent=4)

def get_base_url(url):
    return os.path.dirname(url).rsplit('/', 1)[0]