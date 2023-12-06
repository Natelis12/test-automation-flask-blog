from tests.conftest import app, create_test_user

user_name = 'test_user'
email = 'test_email@test.com'
password = 'test_password'


def test_logout_authenticated_user(mocker):
    create_test_user(user_name, email, password)
    mocker.patch('routes.logout.session', {'userName': user_name})
    mock_message = mocker.patch('routes.logout.message')

    with app.test_request_context('/logout'):
        response = app.test_client().get('/logout')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    mock_message.assert_called_once_with("2", f'USER: "{user_name}" LOGGED OUT')


def test_logout_unauthenticated_user(mocker):
    mocker.patch('routes.logout.session', {})
    mock_message = mocker.patch('routes.logout.message')

    with app.test_request_context('/logout'):
        response = app.test_client().get('/logout')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    mock_message.assert_called_once_with("1", "USER NOT LOGGED IN")
