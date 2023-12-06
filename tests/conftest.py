import os

import pytest

from app import app
from dbChecker import COMMENTS_DB, POSTS_DB, USERS_DB
from helpers import exists, message, sha256_crypt, sqlite3

app.config['TESTING'] = True


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


def create_test_user(user_name, email, password, role=None):
    connection = sqlite3.connect(USERS_DB)
    cursor = connection.cursor()
    hashed_password = sha256_crypt.hash(password)
    cursor.execute(
        'INSERT INTO users (userName, email, password, role) VALUES (?, ?, ?, ?)',
        (user_name, email, hashed_password, role)
    )
    connection.commit()
    connection.close()


def login_user(client, username, password):
    form_data = {
        'userName': username,
        'password': password
    }
    return client.post('/login/redirect=test', data=form_data)


def create_test_post(post_id, title, tags, content, author, views, date, time):
    connection = sqlite3.connect(POSTS_DB)
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO posts (id, title, tags, content, author, views, date, time) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (post_id, title, tags, content, author, views, date, time)
    )
    connection.commit()
    connection.close()


def create_test_comment(comment_id, content, user_name, date, time):
    connection = sqlite3.connect(COMMENTS_DB)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO comments (id, post, comment, user, date, time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (comment_id, 1, content, user_name, date, time)
    )

    connection.commit()
    connection.close()
