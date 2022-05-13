import os.path
import sqlite3

import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from __main__ import config_container

from hapyka.utils.logger import get_logger

if os.name == 'nt':
    db_path = "C:\\tmp\\hapyka.sqlite"
else:
    db_path = config_container.get("database_path")

logger = get_logger()

if db_path is None:
    logger.error("Cannot start with None database. Check your configuration.")
    exit(1)

if not os.path.exists(db_path):
    logger.info("Database does not exist. Creating...")
    conn = sqlite3.connect(db_path)
    conn.commit()
    conn.close()


engine = None
Base = None
session_generator = None
path = ""


def initialize():
    global engine, Base, session_generator
    try:
        logger.info("Initializing database {}...".format(db_path))
        engine = create_engine('sqlite:///{}'.format(db_path))
        Base = declarative_base()
        session_generator = scoped_session(sessionmaker(bind=engine.execution_options(isolation_level='AUTOCOMMIT'), future=True))
        import hapyka.database.models
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")
    except Exception as e:
        logger.error("Could not initialize: {}".format(e.__class__.__name__))
        raise e


def get_session_factory():
    return session_generator


def get_connection():
    return engine.connect()


def get_raw_connection():
    return engine.raw_connection()


def get_session():
    return session_generator()


def get_transaction():
    session = get_session()
    try:
        session_transaction = session.begin()
    except sqlalchemy.exc.InvalidRequestError:
        session_transaction = session.begin_nested()
    if session_transaction is None:
        raise sqlalchemy.exc.InvalidRequestError("Could not create an sqlite session.")
    return session, session_transaction
