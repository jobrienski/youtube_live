# -*- coding: utf-8 -*-
"""
liveapi API app
===================
"""
from baseconfig import get_current_flask_env
from .factories import create_application

name = __name__     # import module name

config_type = get_current_flask_env()
app = create_application( name, config_type=config_type, instance_relative=True )
