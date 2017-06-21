from db import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.dialects import sqlite
from sqlalchemy.sql.functions import current_timestamp


class AlertTypes(object):
    MONTHLY_BILL = 1


class UserAlert(DeclarativeBase):
    __tablename__ = 'user_alerts'
    id = Column(sqlite.INTEGER, primary_key=True)
    uuid = Column(sqlite.VARCHAR(36))
    alert_type = Column(sqlite.INTEGER, nullable=False,
                        default=AlertTypes.MONTHLY_BILL)
    content = Column(sqlite.TEXT, nullable=False, default='')
    created = Column(sqlite.TIMESTAMP(), default=current_timestamp())
