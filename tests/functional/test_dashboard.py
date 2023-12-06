from tests.conftest import app, create_test_comment, create_test_post, create_test_user


def test_dashboard_authenticated_user_own_dashboard():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post 1', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')
    create_test_comment(1, 'Test Comment 1', 'test_user', '2023-01-01', '12:00:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/dashboard/test_user')

    assert response.status_code == 200
    assert b'test_user' in response.data
    assert b'/post/1' in response.data
    assert b'Test Post 1' in response.data
    assert b'Test Comment 1' in response.data


def test_dashboard_authenticated_user_other_user_dashboard():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_user('other_user', 'other_user@example.com', 'password456')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/dashboard/other_user')

    assert response.status_code == 302
    assert response.headers['Location'] == '/dashboard/test_user'


def test_dashboard_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/dashboard/test_user', follow_redirects=True)

    assert response.status_code == 200
    assert b'you need login for reach to dashboard' in response.data


def test_dashboard_no_posts_no_comments():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/dashboard/test_user')

    assert response.status_code == 200
    assert b'test_user' in response.data
    assert b'/post/1' not in response.data
