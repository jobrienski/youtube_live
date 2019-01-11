from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


class GoogleOAuth2Ext:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.token_uri = None
        self.flow_config = None
        self.scopes = None
        self.callback_url = None
        self.api_key = None

    def set_app_credentials(self,client_id,client_secret,callback_url,scopes=None,
                            api_key=None,token_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.scopes = scopes
        self.api_key = api_key
        self.token_uri = token_uri

    def user_credentials_from_tokens(self,access_token,refresh_token=None,scopes=None):
        """
        Args:
            access_token ():
            refresh_token ():
            scopes ():

        Returns:
        """
        return Credentials(
            access_token,
            refresh_token=refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=scopes)

    def get_authorized_session(self,credentials):
        return AuthorizedSession(credentials)

    def get_client_simple(self,token,refresh_token=None,scopes=None):
        return self.get_authorized_session(
            self.user_credentials_from_tokens(token,refresh_token,scopes=scopes))

    def get_client_api_key(self,short_name,version):
        return build(short_name,developerKey=self.api_key,version=version)

    def get_flow(self,state=None):
        flow = Flow.from_client_config(self.flow_config,
                                       scopes=self.scopes,
                                       state=state)
        flow.redirect_uri = self.callback_url
        return flow

    def get_redir_url(self,flow):
        return flow.authorization_url(access_type='offline',prompt='consent')

    # call after routes set up
    def init_app(self,app):
        client_id = app.config['GOOGLE_CLIENT_ID']
        app_id = app.config['GOOGLE_APP_ID']
        secret = app.config['GOOGLE_CLIENT_SECRET']
        callback_url = app.config['GOOGLE_CALLBACK_URL']
        scopes = app.config["GOOGLE_SCOPES"]
        api_key = app.config["GOOGLE_API_KEY"]

        token_uri = "https://accounts.google.com/o/oauth2/token"
        self.flow_config = {
            "web":{
                "client_id":                  f"{client_id}",
                "project_id":                 f"{app_id}",
                "auth_uri":                   "https://accounts.google.com/o/oauth2/auth",
                "token_uri":                  f"{token_uri}",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1"
                                              "/certs",
                "client_secret":              f"{secret}",
                "redirect_uris":              [
                    f"{callback_url}"
                ]
            }
        }

        self.set_app_credentials(client_id,secret,callback_url,
                                 token_uri=token_uri,api_key=api_key,
                                 scopes=scopes)


_goog_auth_helper = GoogleOAuth2Ext()
