from tests.conftest import app, create_test_comment, create_test_user


def test_admin_panel_comments_authenticated_admin():
    create_test_user('admin', 'admin@example.com', 'password123', 'admin')
    create_test_comment(1, 'Test Comment 1', 'test_user', '2023-01-01', '12:00:00')
    create_test_comment(2, 'Test Comment 2', 'another_user', '2023-01-02', '14:30:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'admin'

        response = client.get('/admin/comments')

    assert response.status_code == 200
    assert b'Admin Panel --> Comments' in response.data
    assert b'Test Comment 1' in response.data
    assert b'Test Comment 2' in response.data


def test_admin_panel_comments_authenticated_user(mocker):
    mocker.patch('routes.adminPanelComments.session', {'userName': 'test_user'})
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_comment(1, 'Test Comment 1', 'test_user', '2023-01-01', '12:00:00')

    response = app.test_client().get('/admin/comments')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_admin_panel_comments_unauthenticated_user(mocker):
    mocker.patch('routes.adminPanelComments.session', {})

    response = app.test_client().get('/admin/comments')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
