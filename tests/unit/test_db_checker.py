from sqlite3 import OperationalError

from dbChecker import (
    COMMENTS_DB, POSTS_DB, USERS_DB, commentsTable, dbFolder, postsTable, sqlite3, usersTable
)


def test_db_folder_not_found(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message')
    dbFolder()
    mock_message.assert_called_with("2", 'Folder: "/db" CREATED')
    mock_message.call_args_list


def test_users_table_operational_exception(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message',
                                side_effect=[None, None, OperationalError, None, None])
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')
    
    usersTable()

    mock_message.assert_called_with('2', 'TABLE: "Users" CREATED')
    mock_open.assert_called_with(USERS_DB, 'x')
    mock_sqlite_connect.assert_called_with(USERS_DB)


def test_users_table_not_found(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message')
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')

    usersTable()
    mock_message.assert_called_with("6", 'TABLE: "Users" FOUND')
    mock_open.assert_called_with(USERS_DB, 'x')
    mock_sqlite_connect.assert_called_with(USERS_DB)


def test_posts_table_not_found(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message')
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')

    postsTable()
    mock_message.assert_called_with('6', 'TABLE: "Posts" FOUND')
    mock_open.assert_called_with(POSTS_DB, 'x')
    mock_sqlite_connect.assert_called_with(POSTS_DB)


def test_posts_table_operational_exception(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message',
                                side_effect=[None, None, OperationalError, None, None])
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')

    postsTable()
    mock_message.assert_called_with('2', 'TABLE: "Posts" CREATED')
    mock_open.assert_called_with(POSTS_DB, 'x')
    mock_sqlite_connect.assert_called_with(POSTS_DB)


def test_comments_table_not_found(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message')
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')

    commentsTable()
    mock_message.assert_called_with('6', 'TABLE: "Comments" FOUND')
    mock_open.assert_called_with(COMMENTS_DB, 'x')
    mock_sqlite_connect.assert_called_with(COMMENTS_DB)


def test_comments_table_operational_exception(mocker):
    mocker.patch('dbChecker.exists', return_value=False)
    mocker.patch('dbChecker.mkdir')
    mock_message = mocker.patch('dbChecker.message',
                                side_effect=[None, None, OperationalError, None, None])
    mock_open = mocker.patch('builtins.open')
    mock_sqlite_connect = mocker.patch.object(sqlite3, 'connect')
    mocker.patch.object(sqlite3, 'Cursor')

    commentsTable()
    mock_message.assert_called_with("2", 'TABLE: "Comments" CREATED')
    mock_open.assert_called_with(COMMENTS_DB, 'x')
    mock_sqlite_connect.assert_called_with(COMMENTS_DB)
