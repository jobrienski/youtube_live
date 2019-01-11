# coding: utf-8

import datetime as dt
import enum

from sqlalchemy import Column,DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql import expression

DeclarativeBase = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow,'postgresql')
def pg_utcnow(element,compiler,**kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Base(DeclarativeBase):
    __abstract__ = True

    created_on = Column(DateTime,nullable=False,default=dt.datetime.utcnow(),
                        server_default=utcnow())
    updated_on = Column(DateTime,nullable=False,onupdate=dt.datetime.utcnow(),
                        default=dt.datetime.utcnow(),
                        server_onupdate=utcnow())

    @staticmethod
    def wrap_in_dict(cls,instance: object,columns: list,list_column: str,list_data: list):
        wrapper = dict()
        for column in columns:
            if hasattr(instance,column):
                wrapper[column] = getattr(instance,column)
        wrapper[list_column] = list_data

        return wrapper


class OwnerMixin:
    @hybrid_method
    def check_owner(self,user):
        created_by = getattr(self,'created_by',False)

        if not created_by:
            return False

        return created_by==user


class SupervisorMixin:
    @hybrid_method
    def check_supervisor(self,user):
        created_by = getattr(self,'created_by',False)

        if not created_by or not created_by.manager:
            return False

        return created_by.manager==user


class OwnerSupervisorCheckMixin(OwnerMixin,SupervisorMixin):
    pass


class StaticRolesEnum(enum.Enum):
    # pylint: disable=missing-docstring,unsubscriptable-object
    INTERNAL = (0x8000,"Internal")
    ADMIN = (0x4000,"Admin")
    REGULAR_USER = (0x2000,"Regular User")
    ACTIVE = (0x1000,"Active Account")

    @property
    def mask(self):
        return self.value[0]

    @property
    def title(self):
        return self.value[1]


def _get_is_static_role_property(role_name,static_role):
    """
    A helper function that aims to provide a property getter and setter
    for static roles.

    Args:
        role_name (str)
        static_role (int) - a bit mask for a specific role

    Returns:
        property_method (property) - preconfigured getter and setter property
        for accessing role.
    """

    @property
    def _is_static_role_property(self):
        if self.static_roles is None:
            self.static_roles = 0
        return self.has_static_role(static_role)

    @_is_static_role_property.setter
    def _is_static_role_property(self,value):
        if self.static_roles is None:
            self.static_roles = 0
        if value:
            self.set_static_role(static_role)
        else:
            self.unset_static_role(static_role)

    _is_static_role_property.fget.__name__ = role_name
    return _is_static_role_property
