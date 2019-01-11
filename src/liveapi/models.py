# coding: utf-8

from sqlalchemy import Boolean,Column,Integer,String, ForeignKey,UnicodeText
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from liveapi.models_base import Base,OwnerSupervisorCheckMixin

class User(Base,OwnerSupervisorCheckMixin):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    google_id = Column(String(100),nullable=False,unique=True,index=True)
    name = Column(String(128),nullable=False)
    username = Column(String(320),nullable=False,index=True,unique=True)
    avatar = Column(String(2048))
    tz = Column(String(128))
    static_roles = Column(Integer,default=0,nullable=False)
    tracking = relationship('Chatterbox',
                            primaryjoin='Chatterbox.tracker_id == User.id',
                            lazy='selectin')

    @aggregated('tracking',Column(Integer))
    def tracking_count(self):
        return func.count('1')

    is_deleted = Column(
        Boolean(name="is_deleted"),  # sql alchemy bug psql
        nullable=False,
        default=False,
        server_default=expression.false(),
    )

    def __repr__(self):
        return "<User '{}':'{}'>".format(self.google_id,self.username)

class Chatterbox(Base,OwnerSupervisorCheckMixin):
    __tablename__ = "chatterbox"
    id = Column(Integer,primary_key=True)
    display_name = Column(String(100),nullable=False,index=True)  # todo unicode
    channel_id = Column(String(100),nullable=True,index=True)
    tracker_id = Column(Integer,ForeignKey(User.id),nullable=True)


class ChatMessageThread(Base):
    __tablename__ = 'thread'
    id = Column(Integer,primary_key=True)
    youtube_message_id = Column(String(100))
    message = Column(UnicodeText)

    @aggregated('comments',Column(Integer))
    def comment_count(self):
        return func.count('1')

    comments = relationship(
        'Comment',
        backref=backref('thread', lazy=None)
    )


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer,primary_key=True)
    content = Column(UnicodeText)
    thread_id = Column(Integer,ForeignKey(ChatMessageThread.id))
