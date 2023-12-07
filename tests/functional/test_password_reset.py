from tests.conftest import app, create_test_user


def test_password_reset_code_sent_and_authenticated_user_valid_code(mocker):
    mocker.patch('routes.passwordReset.randint', return_value=1234)
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        # Step 1: Send password reset code
        response_send_code = client.post('/passwordreset/codesent=false', data={
            'userName': 'test_user',
            'email': 'test_user@example.com',
        }, follow_redirects=True)

        assert response_send_code.status_code == 200
        assert b'code sent' in response_send_code.data

        # Step 2: Attempt to reset password with valid code
        response_reset_password = client.post('/passwordreset/codesent=true', data={
            'code': '1234',
            'password': 'newpassword123',
            'passwordConfirm': 'newpassword123'
        }, follow_redirects=True)

    assert response_reset_password.status_code == 200
    assert b'you need login with new password' in response_reset_password.data


def test_password_reset_code_sent_and_authenticated_user_wrong_code():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        # Step 1: Send password reset code
        response_send_code = client.post('/passwordreset/codesent=false', data={
            'userName': 'test_user',
            'email': 'test_user@example.com',
        }, follow_redirects=True)

        assert response_send_code.status_code == 200
        assert b'code sent' in response_send_code.data

        # Step 2: Attempt to reset password with wrong code
        response_reset_password = client.post('/passwordreset/codesent=true', data={
            'code': '5678',
            'password': 'newpassword123',
            'passwordConfirm': 'newpassword123'
        })

    assert response_reset_password.status_code == 200
    assert b'Wrong Code' in response_reset_password.data


def test_password_reset_user_not_found():
    with app.test_client() as client:
        response = client.post('/passwordreset/codesent=false', data={
            'userName': 'non_existing_user',
            'email': 'non_existing_user@example.com',
        })

    assert response.status_code == 200
    assert b'user not found' in response.data


def test_password_reset_code_sent_and_authenticated_user_same_old_and_new_password(mocker):
    mocker.patch('routes.passwordReset.randint', return_value=1234)
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        # Step 1: Send password reset code
        response_send_code = client.post('/passwordreset/codesent=false', data={
            'userName': 'test_user',
            'email': 'test_user@example.com',
        }, follow_redirects=True)

        assert response_send_code.status_code == 200
        assert b'code sent' in response_send_code.data

        # Step 2: Attempt to reset password with the same old and new password
        response_reset_password = client.post('/passwordreset/codesent=true', data={
            'code': '1234',
            'password': 'password123',
            'passwordConfirm': 'password123'
        })

    assert response_reset_password.status_code == 200
    assert b'new password can not be same with old password' in response_reset_password.data


def test_password_reset_code_sent_and_authenticated_user_passwords_do_not_match(mocker):
    mocker.patch('routes.passwordReset.randint', return_value=1234)
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        # Step 1: Send password reset code
        response_send_code = client.post('/passwordreset/codesent=false', data={
            'userName': 'test_user',
            'email': 'test_user@example.com',
        }, follow_redirects=True)

        assert response_send_code.status_code == 200
        assert b'code sent' in response_send_code.data

        # Step 2: Attempt to reset password with passwords that do not match
        response_reset_password = client.post('/passwordreset/codesent=true', data={
            'code': '1234',
            'password': 'newpassword123',
            'passwordConfirm': 'mismatchedpassword'
        })

    assert response_reset_password.status_code == 200
    assert b'passwords must match' in response_reset_password.data
