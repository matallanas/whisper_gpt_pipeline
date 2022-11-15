"""Simple script to create a sqlite db with a single table
called 'videos'.
"""

import sqlite3

def create_db(db_path: str) -> None:
    """Create an sqlite db with a single table called 'videos'"""
    connection = sqlite3.connect(db_path)
    print(f"Created db successfully at '{db_path}'")
    connection.execute(
        '''
        CREATE TABLE VIDEO
        (ID INTEGER     PRIMARY KEY     AUTOINCREMENT,
        CHANNEL_NAME    CHAR(30)        NOT NULL,
        URL             TEXT            NOT NULL,
        TITLE           CHAR(100),
        DESCRIPTION     CHAR(5000),
        TRANSCRIPTION   TEXT,
        SEGMENTS        TEXT         
        )
        '''
    )
    print(f"'Video' table created successfully")

if __name__ == "__main__":
    create_db("video.db")