from tests.conftest import app, create_test_user


def test_admin_panel_authenticated_admin(mocker):
    mocker.patch('routes.adminPanel.session', {'userName': 'admin'})
    create_test_user('admin', 'admin@example.com', 'password123', 'admin')

    response = app.test_client().get('/admin')

    assert response.status_code == 200
    assert b'Admin Panel' in response.data


def test_admin_panel_authenticated_user(mocker):
    mocker.patch('routes.adminPanel.session', {'userName': 'test_user'})
    create_test_user('test_user', 'test_user@example.com', 'password123')

    response = app.test_client().get('/admin')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_admin_panel_unauthenticated_user(mocker):
    mocker.patch('routes.adminPanel.session', {})

    response = app.test_client().get('/admin')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
