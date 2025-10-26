from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event as sql_event
from sqlalchemy.engine import Engine

from webapp.event import Event as Event
from webapp.helpers import GameStatus, WinningPlayerNum, GamePosition

db = SQLAlchemy()


# Instruct SQLAlchemy to enforce FK constraints:
@sql_event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()