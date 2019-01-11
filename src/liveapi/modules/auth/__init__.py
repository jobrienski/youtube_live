# # encoding: utf-8
# """
# Auth module
# ===========
# """
# from liveapi.extensions.api import api_v1
# from liveapi.models.user import User
#
# def init_app(app, **kwargs):
#     # pylint: disable=unused-argument
#     """
#     Init auth module.
#     """
#
#     # Touch underlying modules
#     from . import views, resources  # pylint: disable=unused-variable
#
#     # Mount authentication routes
#     app.register_blueprint(views.auth_blueprint)
#     api_v1.add_namespace(resources.api)
