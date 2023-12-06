from tests.conftest import app

app.config['TESTING'] = True


def test_signup_authenticated_redirects(mocker):
    with app.test_request_context('/signup'):
        mocker.patch('routes.signup.session', {'userName': 'test_user'})
        response = app.test_client().get('/signup')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_signup_valid_submission(mocker):
    form_data = {
        'userName': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password123'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        mocker.patch('routes.signup.session', {})
        response = app.test_client().post('/signup', data=form_data)

    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    final_response = app.test_client().get(response.headers['Location'])
    assert final_response.status_code == 200


def test_signup_invalid_password_confirmation(mocker):
    form_data = {
        'userName': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password456'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        mocker.patch('routes.signup.session', {})
        response = app.test_client().post('/signup', data=form_data)

    assert b'password must match' in response.data
    assert response.status_code == 200


def test_signup_existing_user(mocker):
    mocker.patch('routes.signup.session', {})

    form_data = {
        'userName': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password123'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        response = app.test_client().post('/signup', data=form_data)

        assert response.status_code == 302
        assert response.headers['Location'] == '/'

        final_response = app.test_client().get(response.headers['Location'])
        assert final_response.status_code == 200

        form_data['email'] = 'new_new_user@example.com'
        response = app.test_client().post('/signup', data=form_data)

    assert b'This username is unavailable.' in response.data
    assert response.status_code == 200


def test_signup_existing_email(mocker):
    mocker.patch('routes.signup.session', {})

    form_data = {
        'userName': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password123'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        response = app.test_client().post('/signup', data=form_data)

        assert response.status_code == 302
        assert response.headers['Location'] == '/'

        final_response = app.test_client().get(response.headers['Location'])
        assert final_response.status_code == 200

        form_data['userName'] = 'new_new_user'
        response = app.test_client().post('/signup', data=form_data)

    assert b'This email is unavailable.' in response.data
    assert response.status_code == 200


def test_signup_existing_user_and_email(mocker):
    mocker.patch('routes.signup.session', {})

    form_data = {
        'userName': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password123'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        response = app.test_client().post('/signup', data=form_data)

        assert response.status_code == 302
        assert response.headers['Location'] == '/'

        final_response = app.test_client().get(response.headers['Location'])
        assert final_response.status_code == 200

        response = app.test_client().post('/signup', data=form_data)

    assert b'This username and email is unavailable.' in response.data
    assert response.status_code == 200


def test_signup_invalid_username_characters(mocker):
    form_data = {
        'userName': 'new_userЇ',
        'email': 'new_user@example.com',
        'password': 'password123',
        'passwordConfirm': 'password123'
    }

    with app.test_request_context('/signup', method='POST', data=form_data):
        mocker.patch('routes.signup.session', {})
        response = app.test_client().post('/signup', data=form_data)

    assert b'username does not fit ascii characters' in response.data
    assert response.status_code == 200
