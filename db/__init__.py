"""
    Create tables by running this as main.
    For now db is put in this dir "file.db"
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlite3 import dbapi2 as sqlite
from sqlalchemy.ext.declarative import declarative_base
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "file.db")
_engine = create_engine('sqlite+pysqlite:///{}'.format(db_path), module=sqlite)
_session = sessionmaker()
_session.configure(bind=_engine)
DeclarativeBase = declarative_base()
DeclarativeBase.metadata.bind = _engine


def get_session():
    return _session()


def row2dict(row, columns=None):
    columns = columns or row.__table__.columns
    return dict((column.name, getattr(row, column.name)) for column in columns)


def row2dict_many(*rows):
    """
        Useful for joined table results. Overwrites subsequently named columns.
    """
    r = row2dict(rows[0])
    for row in rows[1:]:
        r.update(row2dict(row))
    return r


if __name__ == '__main__':
    from db.accounts import *
    from db.user_alerts import *
    DeclarativeBase.metadata.create_all(_engine)
