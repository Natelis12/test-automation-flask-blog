import os

import pytest

from dbChecker import COMMENTS_DB, POSTS_DB, USERS_DB
from helpers import exists, message, sqlite3


@pytest.fixture(scope='function', autouse=True)
def truncate_databases():
    # Truncate the databases before running tests
    truncate_database(USERS_DB)
    truncate_database(COMMENTS_DB)
    truncate_database(POSTS_DB)

    # Run the tests
    yield

    # Truncate the databases after running tests
    truncate_database(USERS_DB)
    truncate_database(COMMENTS_DB)
    truncate_database(POSTS_DB)


def truncate_database(db_path):
    if exists(db_path):
        message("6", f'DATABASE: "{db_path}" FOUND')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        table_name = os.path.splitext(os.path.basename(db_path))[0]

        cursor.execute(f"DELETE FROM {table_name};")
        connection.commit()

        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
        result = cursor.fetchone()

        connection.close()
        assert result is None, f'Data in DATABASE: "{db_path}" NOT TRUNCATED'

        message("6", f'Tables in DATABASE: "{db_path}" TRUNCATED')
    else:
        message("1", f'DATABASE: "{db_path}" NOT FOUND')
        assert False, f'DATABASE: "{db_path}" NOT FOUND'
