import sys
from liveapi.factories import create_application
from liveapi.extensions import db
from flask_testing import TestCase


class TestBase(TestCase):
    def create_app(self):
        return create_application('testing')


class TestApplicationBase(TestBase):
    # SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        super().tearDown()
        db.session.remove()
        db.drop_all()
