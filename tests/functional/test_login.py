from tests.conftest import app, create_test_user

user_name = 'test_user'
email = 'test_email@test.com'
password = 'test_password'


def test_login_authenticated_redirects(mocker):
    create_test_user(user_name, email, password)

    with app.test_request_context('/login/redirect=test'):
        mocker.patch('routes.login.session', {'userName': user_name})
        response = app.test_client().get('/login/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == 'test'


def test_login_valid_submission(mocker):
    create_test_user(user_name, email, password)
    # mocker.patch('routes.login.session', {})

    form_data = {
        'userName': user_name,
        'password': password
    }

    with app.test_request_context('/login/redirect=test', method='POST', data=form_data):
        response = app.test_client().post('/login/redirect=test', data=form_data)

    assert response.status_code == 302
    assert response.headers['Location'] == 'test'


def test_login_invalid_password(mocker):
    create_test_user(user_name, email, password)
    mocker.patch('routes.login.session', {})

    form_data = {
        'userName': user_name,
        'password': 'wrong_password'
    }

    with app.test_request_context('/login/redirect=test', method='POST', data=form_data):
        response = app.test_client().post('/login/redirect=test', data=form_data)

    assert b'wrong password' in response.data
    assert response.status_code == 200


def test_login_user_not_found(mocker):
    mocker.patch('routes.login.session', {})

    form_data = {
        'userName': 'nonexistent_user',
        'password': 'password123'
    }

    with app.test_request_context('/login/redirect=test', method='POST', data=form_data):
        response = app.test_client().post('/login/redirect=test', data=form_data)

    assert b'user not found' in response.data
    assert response.status_code == 200
