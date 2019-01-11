import os
from flask.helpers import get_debug_flag
from liveapi.util import fromenv

# This is for the base REST url
# blah.streamlabs.com/api/v1 or /api/v2 and then the REST url
# blah.streamlabs.com/api/v1/users
API_VERSION = "1"
URL_PREFIX = f'/api/v{API_VERSION}'

# This variable determines the config that gets loaded.
CURRENT_FLASK_ENV = None


def get_current_flask_env(default='development'):
    global CURRENT_FLASK_ENV
    if CURRENT_FLASK_ENV is None:
        CURRENT_FLASK_ENV = fromenv('FLASK_ENV',default=default)
    return CURRENT_FLASK_ENV


class BaseConfig(object):
    """Base configuration.
    """
    import uuid
    SECRET_KEY = fromenv('SECRET_KEY') or str(uuid.uuid4())
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
    LOG_FOLDER = os.path.join(APP_ROOT,"../..","logs")
    TESTING = False
    DEBUG = True
    FLASK_PY_CONFIG = "development.py"
    FLASK_DEBUG = DEBUG or get_debug_flag()
    SSL_DISABLED = True
    BETTER_EXCEPTIONS = True
    SERVER_NAME = "tasq.ngrok.io"
    #BASE_URL = f"http://${SERVER_NAME}"

    ## Override these
    SQLALCHEMY_DATABASE_URI = None
    LOG_LEVEL = "DEBUG"

    DB_NAME = None

    PORT = 5000

    ## Secret
    GOOGLE_CLIENT_ID = None
    GOOGLE_CLIENT_SECRET = None
    GOOGLE_APP_ID = None
    GOOGLE_SCOPES = ["https://www.googleapis.com/auth/userinfo.profile",
                     "https://www.googleapis.com/auth/userinfo.email",
                     "https://www.googleapis.com/auth/plus.me"]
    GOOGLE_CONFIG = None  # set up in extension

    # JWT
    JWT_SECRET_KEY = None

    # Docker
    IS_DOCKER = False
    IS_PROXIED = False  # is behind nginx proxy (affects proxy fix)

    ## Optional override
    FLASK_SLOW_DB_QUERY_TIME = 1.0
    TEMPLATE_CACHE_TIMEOUT = 24 * 60 * 60
    TEMPLATES_AUTO_RELOAD = False
    SSL_DISABLE = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = False
    # solves problems with cached query results
    # SQLALCHEMY_EXPIRE_ON_COMMIT = False
    # Important in case uncaught exception, otherwise
    # worker won't be able to do any more queries
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask
    DEBUG_TB_ENABLED = False
    PROPAGATE_EXCEPTIONS = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    ## End optional override

    # Expirations

    # swagger doc
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_UI_JSONEDITOR = True
    STATIC_ROOT = os.path.join(APP_ROOT,'static')
    REVERSE_PROXY_SETUP = os.getenv('IS_PROXIED',False)

    SCHEME = "http"

    # Enabled modules: note `api` must be last in list
    # in order for the other endpoints to register correctly.
    ENABLED_MODULES = (
        'auth',
        'user',
        'api',
    )

    SWAGGER_UI_OAUTH_CLIENT_ID = 'documentation'
    SWAGGER_UI_OAUTH_REALM = "Authentication for server documentation"
    SWAGGER_UI_OAUTH_APP_NAME = "Auth server documentation"
    CSRF_ENABLED = True

    # cors (for swagger doc for now)
    ALLOW_CORS = True
    CORS_PATH = None

    @classmethod
    def init(cls):
        if cls.DEBUG:
            cls.FLASK_DEBUG = True

    @classmethod
    def init_app(cls,app):
        app.config.from_object(cls)
        app.config.from_pyfile(cls.FLASK_PY_CONFIG)
        if not app.config['SQLALCHEMY_DATABASE_URI']:
            cls.DB_PATH = os.path.join(cls.APP_ROOT,"..",'dev.sqlite3')
            cls.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}?check_same_thread=false'.format(
                cls.DB_PATH)
            app.config['SQLALCHEMY_DATABASE_URI'] = cls.SQLALCHEMY_DATABASE_URI
        cls.GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
        cls.GOOGLE_APP_ID = app.config['GOOGLE_APP_ID']
        cls.GOOGLE_SCOPES = app.config['GOOGLE_SCOPES']
        cls.GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
        cls.PORT = app.config['PORT']
        cls.SSL_DISABLED = app.config['SSL_DISABLED']
        #cls.SCHEME = app.config['SCHEME']
        #cls.set_base_url()
        #app.config['BASE_URL'] = cls.BASE_URL  # I don't trust url_for _external

    @classmethod
    def set_base_url(cls):
        cls.BASE_URL = f"{cls.SCHEME}://{cls.SERVER_NAME}"


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_PY_CONFIG = "development.py"
    ALLOW_CORS = True
    CORS_PATH = "*"

    @classmethod
    def init(cls):
        super().init()
        cls.CURRENT_FLASK_ENV = "development"

    @classmethod
    def init_app(cls,app):
        super().init_app(app)
        app.testing = False
        app.debug = True


class IntegrationConfig(BaseConfig):
    TESTING = False
    IS_PROXIED = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_PY_CONFIG = "integration.py"
    ALLOW_CORS = True
    CORS_PATH = "/api/*"
    SSL_DISABLE = True

    @classmethod
    def init(cls):
        super().init()
        cls.CURRENT_FLASK_ENV = "integration"

    @classmethod
    def init_app(cls,app):
        super().init_app(app)
        app.testing = False
        app.debug = True


class ProductionConfig(BaseConfig):
    """Production configuration."""
    FLASK_DEBUG = False
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SSL_DISABLE = False
    SQLALCHEMY_RECORD_QUERIES = False
    IS_PROXIED = False
    TEMPLATES_AUTO_RELOAD = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_PY_CONFIG = "production.py"

    @classmethod
    def init(cls):
        super().init()
        cls.CURRENT_FLASK_ENV = 'production'


## Docker configs

class DevelopmentConfigDocker(DevelopmentConfig):
    IS_DOCKER = True
    IS_PROXIED = True
    FLASK_PY_CONFIG = "development-docker.py"


class ProductionConfigDocker(ProductionConfig):
    FLASK_PY_CONFIG = "production-docker.py"
    IS_DOCKER = True
    IS_PROXIED = True


class IntegrationConfigDocker(IntegrationConfig):
    FLASK_PY_CONFIG = "integration-docker.py"
    IS_DOCKER = True
    IS_PROXIED = True


class TestingConfig(BaseConfig):
    """Test configuration."""
    TESTING = True
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_PY_CONFIG = "testing.py"
    WTF_CSRF_ENABLED = False  # Allows form testing
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid

    # rounds"

    @classmethod
    def init(cls):
        super().init()

    @classmethod
    def init_app(cls,app):
        super().init_app(app)
        app.testing = True


config = {
    'development':       DevelopmentConfig,
    'development-docker':DevelopmentConfigDocker,
    'integration':       IntegrationConfig,
    'integration-docker':IntegrationConfigDocker,
    'testing':           TestingConfig,
    'production':        ProductionConfig,
    'production-docker': ProductionConfigDocker,
    'default':           DevelopmentConfig
}

# This variable is pulled in on to other modules to get config values
# example: from ..config import current_config as config
current_config = config[get_current_flask_env()]
API_VERSION = "1"
