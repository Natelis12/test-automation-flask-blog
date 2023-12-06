from tests.conftest import app, create_test_user


def test_delete_user_authenticated_admin(mocker):
    mocker.patch('routes.deleteUser.session', {'userName': 'admin'})
    mock_message = mocker.patch('routes.deleteUser.message')

    create_test_user('admin', 'admin@example.com', 'password123', 'admin')
    create_test_user('test_user', 'test_user@example.com', 'password123')

    response = app.test_client().get('/admin/deleteuser/test_user/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == 'test'
    mock_message.assert_called_once_with('2', 'USER: "test_user" DELETED')


def test_delete_user_authenticated_user_own_account(mocker):
    mocker.patch('routes.deleteUser.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deleteUser.message')

    create_test_user('admin', 'admin@example.com', 'password123', 'admin')
    create_test_user('test_user', 'test_user@example.com', 'password123')

    response = app.test_client().get('/admin/deleteuser/test_user/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == 'test'
    mock_message.assert_called_once_with('2', 'USER: "test_user" DELETED')


def test_delete_user_authenticated_user_other_user_account(mocker):
    mocker.patch('routes.deleteUser.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deleteUser.message')

    create_test_user('test_user', 'admin@example.com', 'password123')
    create_test_user('other_user', 'other_user@example.com', 'password123')

    response = app.test_client().get('/admin/deleteuser/other_user/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == 'test'
    mock_message.assert_called_once_with(
        '1', 'USER: "other_user" NOT DELETED YOU ARE NOT other_user')


def test_delete_user_unauthenticated_user(mocker):
    mocker.patch('routes.deleteUser.session', {})
    mock_message = mocker.patch('routes.deleteUser.message')

    response = app.test_client().get('/admin/deleteuser/test_user/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/login/redirect=&deleteuser&test_user&redirect=index'
    mock_message.assert_called_once_with('1', 'USER NEEDS TO LOGIN FOR DELETE USER: test_user')


def test_delete_user_user_not_found():
    create_test_user('admin', 'admin@example.com', 'password123', 'admin')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'admin'

        response = client.get('/admin/deleteuser/nonexistent_user/redirect=index')

    assert response.status_code == 302
    assert response.headers['Location'] == '/index'
