from tests.conftest import app, create_test_user


def test_admin_panel_users_authenticated_admin():
    create_test_user('admin', 'admin@example.com', 'password123', 'admin')
    create_test_user('test_user1', 'test_user1@example.com', 'password123')
    create_test_user('test_user2', 'test_user2@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'admin'

        response = client.get('/admin/users')

    assert response.status_code == 200
    assert b'Admin Panel' in response.data
    assert b'test_user1' in response.data
    assert b'test_user2' in response.data


def test_admin_panel_users_authenticated_user(mocker):
    mocker.patch('routes.adminPanelUsers.session', {'userName': 'test_user'})
    create_test_user('test_user', 'test_user@example.com', 'password123')

    response = app.test_client().get('/admin/users')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_admin_panel_users_unauthenticated_user(mocker):
    mocker.patch('routes.adminPanelUsers.session', {})

    response = app.test_client().get('/admin/users')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
