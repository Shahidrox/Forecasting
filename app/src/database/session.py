import logging
import time
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.core import config
"""
This module provides a session object for interacting with the database.

The session object is created using SQLAlchemy's sessionmaker and is bound to the engine created using the DATABASE_URI from the config module.

The root logger is configured to output SQL statements.

Functions:
- before_cursor_execute: Event listener that prints a message before executing a SQL query.
- after_cursor_execute: Event listener that logs the execution time and the executed SQL query.

Attributes:
- engine: The SQLAlchemy engine object.
- Session: The sessionmaker object.
- session: The session object.

Example usage:
    # Create a new session
    session = session()

    # Execute a SQL query
    result = session.execute("SELECT * FROM users")

    # Commit the changes
    session.commit()
"""

engine = create_engine(config.DATABASE_URI, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Configure the root logger to output SQL statements
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@event.listens_for(engine, 'before_cursor_execute')
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print('-------------------------------QUERY START---------------------------')
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info['query_start_time'].pop(-1)
    logging.info(f"SQL Query executed in {total_time}s: {statement}")
    print('-------------------------------QUERY END---------------------------')
