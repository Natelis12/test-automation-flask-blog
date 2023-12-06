from tests.conftest import app, create_test_post, create_test_user


def test_admin_panel_posts_authenticated_admin():
    create_test_user('admin', 'admin@example.com', 'password123', 'admin')
    create_test_post(1, 'Test Post 1', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')
    create_test_post(2, 'Test Post 2', 'test, example', 'This is another test post.',
                     'another_user', 0, '2023-01-02', '14:30:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'admin'

        response = client.get('/admin/posts')

    assert response.status_code == 200
    assert b'Admin Panel --> Posts' in response.data
    assert b'Test Post 1' in response.data
    assert b'Test Post 2' in response.data


def test_admin_panel_posts_authenticated_user(mocker):
    mocker.patch('routes.adminPanelPosts.session', {'userName': 'test_user'})
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post 1', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')

    response = app.test_client().get('/admin/posts')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def test_admin_panel_posts_unauthenticated_user(mocker):
    mocker.patch('routes.adminPanelPosts.session', {})

    response = app.test_client().get('/admin/posts')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
