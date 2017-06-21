from db import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.dialects import sqlite
from sqlalchemy.sql.functions import current_timestamp


class Account(DeclarativeBase):
    __tablename__ = 'accounts'
    id = Column(sqlite.INTEGER, primary_key=True)
    uuid = Column(sqlite.VARCHAR(36))
    name = Column(sqlite.VARCHAR(128), nullable=False)
    email = Column(sqlite.VARCHAR(255), nullable=False, unique=True)
    address = Column(sqlite.VARCHAR(128), nullable=False)
    city = Column(sqlite.VARCHAR(128), nullable=False)
    state = Column(sqlite.CHAR(2), nullable=False)
    zip = Column(sqlite.CHAR(9), nullable=False)
    created = Column(sqlite.TIMESTAMP, default=current_timestamp())

    def __repr__(self):
        return ("<User(name='%s', email='%s', created='%s'>"
                % (self.name, self.email, self.created))

    def __str__(self):
        return self.__repr__()


class AccountAudit(DeclarativeBase):
    __tablename__ = 'account_audit'
    id = Column(sqlite.INTEGER, primary_key=True)
    account_id = Column(sqlite.INTEGER, nullable=False)
    name = Column(sqlite.VARCHAR(128), nullable=False)
    email = Column(sqlite.VARCHAR(255), nullable=False)
    address = Column(sqlite.VARCHAR(128), nullable=False)
    city = Column(sqlite.VARCHAR(128), nullable=False)
    state = Column(sqlite.CHAR(2), nullable=False)
    zip = Column(sqlite.CHAR(9), nullable=False)
    source = Column(sqlite.VARCHAR(128), nullable=False)
    created = Column(sqlite.TIMESTAMP, default=current_timestamp())

    def __repr__(self):
        return ("<User(name='%s', email='%s', source='%s'>"
                % (self.name, self.email, self.source))

    def __str__(self):
        return self.__repr__()


class AccountBill(DeclarativeBase):
    __tablename__ = 'account_bills'
    id = Column(sqlite.INTEGER, primary_key=True)
    account_id = Column(sqlite.INTEGER, nullable=False)
    processed = Column(sqlite.BOOLEAN, nullable=False, default=0)
    amount = Column(sqlite.FLOAT, nullable=False)
    month = Column(sqlite.CHAR(2), nullable=False)
    year = Column(sqlite.CHAR(4), nullable=False)
    created = Column(sqlite.TIMESTAMP, default=current_timestamp())
