from flask_jwt_extended import JWTManager

_jwt = JWTManager()


def init_app(app):
    _jwt.init_app(app)
