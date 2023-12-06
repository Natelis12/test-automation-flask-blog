from tests.conftest import app


def test_account_settings_authenticated_user(mocker):
    mocker.patch('app.getProfilePicture', return_value='/static/default_profile_picture.png')
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/accountsettings')

    assert response.status_code == 200
    assert b'change your username' in response.data
    assert b'changepassword' in response.data
    assert b'delete your account' in response.data


def test_account_settings_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/accountsettings')

        assert response.status_code == 302
        assert response.headers['Location'] == '/login/redirect=&accountsettings'
