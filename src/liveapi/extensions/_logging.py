# encoding: utf-8
"""
Logging adapter
---------------
"""
import logging


class Logging(object):
    """
    This is a helper extension, which adjusts logging configuration for the
    application.
    """

    def __init__(self,app=None,config=None):
        if app and config:
            self.init_app(app,config)

    def init_app(self,app,config):
        """
        Common Flask interface to initialize the logging according to the
        application configuration.
        """
        # Replacing default logger handlers with beautiful (muay linda) colored logs
        for handler in list(app.logger.handlers):
            app.logger.removeHandler(handler)
        app.logger.propagate = True

        if app.debug:
            app.logger.setLevel(logging.DEBUG)

        sqla_logger = logging.getLogger('sqlalchemy.engine.base.Engine')
        for hdlr in list(sqla_logger.handlers):
            sqla_logger.removeHandler(hdlr)
        sqla_logger.addHandler(logging.NullHandler())

        logging.basicConfig()
        logger = logging.getLogger()
        logging_level = logging.getLevelName(config.LOG_LEVEL or 'DEBUG')

        logger.setLevel(logging_level)

        try:
            import colorlog
        except ImportError:
            pass
        else:
            formatter = colorlog.ColoredFormatter(
                (
                    '%(asctime)s '
                    '[%(log_color)s%(levelname)s%(reset)s] '
                    '[%(cyan)s%(name)s%(reset)s] '
                    '%(message_log_color)s%(message)s'
                ),
                reset=True,
                log_colors={
                    'DEBUG':   'bold_cyan',
                    'INFO':    'bold_green',
                    'WARNING': 'bold_yellow',
                    'ERROR':   'bold_red',
                    'CRITICAL':'bold_red,bg_white',
                },
                secondary_log_colors={
                    'message':{
                        'DEBUG':   'white',
                        'INFO':    'bold_white',
                        'WARNING': 'bold_yellow',
                        'ERROR':   'bold_red',
                        'CRITICAL':'bold_red',
                    },
                },
                style='%'
            )

            for handler in logger.handlers:
                if isinstance(handler,logging.StreamHandler):
                    break
            else:
                handler = logging.StreamHandler()
                logger.addHandler(handler)
            handler.setFormatter(formatter)
