from tests.conftest import app, create_test_user


def test_change_password_authenticated_user_correct_password():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changepassword', data={
            'oldPassword': 'password123',
            'password': 'newpassword123',
            'passwordConfirm': 'newpassword123'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b'you need login with new password' in response.data


def test_change_password_authenticated_user_wrong_old_password():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changepassword', data={
            'oldPassword': 'wrongpassword',
            'password': 'newpassword123',
            'passwordConfirm': 'newpassword123'
        })

    assert response.status_code == 200
    assert b'old password wrong' in response.data


def test_change_password_authenticated_user_same_old_and_new_password():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changepassword', data={
            'oldPassword': 'password123',
            'password': 'password123',
            'passwordConfirm': 'password123'
        })

    assert response.status_code == 200
    assert b'new password can not be same with old password' in response.data


def test_change_password_authenticated_user_passwords_do_not_match():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/changepassword', data={
            'oldPassword': 'password123',
            'password': 'newpassword123',
            'passwordConfirm': 'mismatchedpassword'
        })

    assert response.status_code == 200
    assert b'passwords must match' in response.data


def test_change_password_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/changepassword', follow_redirects=True)

    assert response.status_code == 200
    assert b'you need login for change your password' in response.data
