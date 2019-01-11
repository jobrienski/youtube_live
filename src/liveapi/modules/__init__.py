# -*- coding: utf-8 -*-
"""
API Module: all the API endpoints be here
=========================================
"""

def init_app(app, **kwargs)->None:
    """ Init modules in the `BaseConfig.ENABLED_MODULES`. Since the modules are REST API endpoints,
    each module's init will add itself to the api namespace.

    Args:
        app (Flask): Flask app
        **kwargs (dict): Additional args that can be passed generically to modules init_app
    """
    # from importlib import import_module
    #
    # for module_name in app.config['ENABLED_MODULES']:
    #     import_module('.%s' % module_name, package=__name__).init_app(app, **kwargs)
    from . import api
    api.init_app(app)
