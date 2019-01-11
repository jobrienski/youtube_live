from os import path
from flask import Flask


def create_application(
        name: str,
        config_type: str,
        instance_relative=True,
        instance_path=None,
        iscelery=False,
        **kwargs
):
    """ Create the flask (or celery) app.
        - Set up config
        - Configure extensions
        - Configure template filters
        - Configure 404 handler
    Args:
        name(str): package name
        instance_path(str): absolute path to instance folder (used for testing right now)
        config_type (str):
        iscelery (bool):

    Returns: app

    """
    # import threading
    # threading.stack_size(2*1024*1024)

    if not name:
        raise ValueError("Name required")

    if not config_type:
        raise ValueError("config_type required")

    if instance_path and not instance_relative:
        raise ValueError("Instance Relative and instance path should be both set.")

    tconfig = get_config(config_type)

    app = Flask(
        name,
        instance_relative_config=instance_relative,
        instance_path=instance_path,
        static_folder=tconfig.STATIC_ROOT,
        **kwargs
    )
    config_app(app,tconfig,iscelery=iscelery)
    configure_extensions(app,tconfig)
    configure_modules(app)

    # proxy fix
    if app.config['IS_PROXIED'] and not iscelery:
        from werkzeug.contrib.fixers import ProxyFix
        from flask import send_from_directory
        import os
        print("Proxying...")
        app.wsgi_app = ProxyFix(app.wsgi_app)
        #
        # @app.route('/static/<path:path>')
        # def static_file(path):
        #     static_folder = os.path.join(os.getcwd(), 'static')
        #     return send_from_directory(static_folder, path)

    return app


def get_config(config_name) -> object:
    # settings in dot file will override BaseConfig settings
    from .util import fromenv,setenv
    from baseconfig import config

    if not fromenv("FLASK_ENV"):
        setenv("FLASK_ENV",config_name)

    tconfig = config[config_name]
    tconfig.init()

    return tconfig


def config_app(app,tconfig,iscelery=False):
    """ Set up config for app, add healthcheck,
    Args:
        app (object): the flask app
        config_name (str): 'development', 'staging', 'production'
        iscelery (bool):

    Returns: config object
    """
    tconfig.init_app(app)


def configure_extensions(app,tconfig):
    from liveapi import extensions

    extensions.init_app(app,tconfig)


def configure_modules(app):
    from liveapi import modules
    modules.init_app(app)


def configure_logging(app,tconfig,iscelery=False):
    """Configure file(info) and email(error) logging."""

    import logging
    import sys

    # from logging.handlers import SMTPHandler
    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    FORMAT = "[%(filename)20s:%(lineno)-s:%(funcName)20s() ] %(message)s"
    logging_level = logging.getLevelName(tconfig.LOG_LEVEL or "DEBUG")
    app.logger.setLevel(logging_level)
    root_logger = logging.getLogger(__name__)
    root_logger.setLevel(logging_level)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(logging.Formatter(FORMAT))
    root_logger.addHandler(stderr_handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    logging.getLogger("flask_cors").level = logging.DEBUG

    #
    # if not app.debug and not config_name == '':
    #     info_log = os.path.join( app.config[ 'LOG_FOLDER' ], 'info.log' )
    #     info_file_handler = \
    #         logging.handlers.RotatingFileHandler(
    #             info_log, maxBytes=100000, backupCount=10 )
    #     info_file_handler.setLevel( logging.INFO )
    #     info_file_handler.setFormatter( logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s '
    #         '[in %(pathname)s:%(lineno)d]' )
    #     )
    #     app.logger.addHandler( info_file_handler )
    # else:

    # bug snag integration
    # import bugsnag
    # from bugsnag.handlers import BugsnagHandler
    # # below caused problems
    # # if iscelery:
    # #     from bugsnag.celery import connect_failure_handler
    # #     connect_failure_handler()
    #
    # bugsnag.configure(
    #     api_key=tconfig.BUGSNAG_API_KEY,
    #     project_root=app.instance_path
    # )
    # handler = BugsnagHandler()
    # handler.setLevel(logging.ERROR)
    # root_logger.addHandler(handler)
    # app.logger.addHandler(handler)

    # FORMAT = "[%(filename)20s:%(lineno)-s:%(funcName)20s() ] %(message)s"
    # logging.basicConfig( level=logging.DEBUG, format=FORMAT )
    logging.getLogger("werkzeug").setLevel(logging_level)
    logging.getLogger("celery").setLevel(logging_level)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Testing
    # app.logger.info("testing info.")
    # app.logger.warn("testing warn.")
    # app.logger.error("testing error.")
    # if not app.debug:
    #     mail_handler = SMTPHandler( app.config[ 'MAIL_SERVER' ],
    #                                 app.config[ 'MAIL_USERNAME' ],
    #                                 app.config[ 'ADMINS' ],
    #                                 'Your Application Failed!',
    #                                 (app.config[ 'MAIL_USERNAME' ],
    #                                  app.config[ 'MAIL_PASSWORD' ]) )
    #     mail_handler.setLevel( logging.ERROR )
    #     mail_handler.setFormatter( logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s '
    #         '[in %(pathname)s:%(lineno)d]' )
    #     )
    #     app.logger.addHandler( mail_handler )
