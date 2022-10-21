import sqlite3

class SQLiteContextManager:
    """Context manager for SQLite db, that handles
    db open / closing connection.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection = None
    
    def __enter__(self):
        """Establish connection with db and return cursor to be used
        to execute queries.
        """
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit queries and close db connection.
        """
        self.connection.commit()
        self.connection.close()