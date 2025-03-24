import os
import sys


def delete_sqlite_db(db_path):
    """Deletes the specified SQLite database file."""
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Database '{db_path}' has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting the database: {e}")
    else:
        print(f"Database '{db_path}' does not exist.")


# usage
delete_sqlite_db("streams.db")