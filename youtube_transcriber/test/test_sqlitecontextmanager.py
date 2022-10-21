import os
from sqlite3 import Cursor

from youtube_transcriber.storing.sqlitecontextmanager import SQLiteContextManager

def test_sqlite_context_manager_init():
    sqlite_context_manager = SQLiteContextManager("dummyinit.db")
    assert type(sqlite_context_manager) == SQLiteContextManager
    
def test_enter_context_manager():
    with SQLiteContextManager("dummy.db") as cursor:
        assert type(cursor) == Cursor
    os.remove("dummy.db")