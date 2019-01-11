#!/usr/bin/env python

import os
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from liveapi import app
from liveapi.extensions import db
from liveapi.models import User, Chatterbox, Comment, ChatMessageThread

print(app.config['SQLALCHEMY_DATABASE_URI'])

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app,db=db,User=User,Chatterbox=Chatterbox,ChatMessageThread=ChatMessageThread,
                Comment=Comment)


@manager.command
def drop_tables():
    db.drop_all()


@manager.command
def run():
    with app.app_context():
        from flask_migrate import migrate as _migrate,upgrade as _upgrade
        # _migrate()  # this doesn't work - program exits
        # _upgrade()
        cert = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl_keys/cert.pem')
        key = cert.replace("cert","key")
        app.run(ssl_context=(cert,key))


@manager.command
def test():
    """Runs the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests',pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__=='__main__':
    manager.run()
