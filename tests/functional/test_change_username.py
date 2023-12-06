from tests.conftest import app, create_test_user


def test_change_username_authenticated_user_valid_input():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changeusername', data={
            'newUserName': 'new_test_user'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b'user name changed' in response.data


def test_change_username_authenticated_user_same_username():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changeusername', data={
            'newUserName': 'test_user'
        })

    assert response.status_code == 200
    assert b'this is your username' in response.data


def test_change_username_authenticated_user_taken_username():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_user('new_test_user', 'new_test_user@example.com', 'password456')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changeusername', data={
            'newUserName': 'new_test_user'
        })

    assert response.status_code == 200
    assert b'This username is already taken.' in response.data


def test_change_username_authenticated_user_invalid_ascii():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changeusername', data={
            'newUserName': 'юзернейм'
        })

    assert response.status_code == 200
    assert b'username does not fit ascii charecters' in response.data


def test_change_username_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/changeusername', follow_redirects=True)

    assert response.status_code == 200
    assert b'/' in response.data
