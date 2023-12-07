from tests.conftest import app, create_test_post, create_test_user


def test_edit_post_authenticated_user_correct_input():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/editpost/1', data={
            'postTitle': 'Edited Post',
            'postTags': 'edit, example',
            'postContent': 'This is an edited post.'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Post edited' in response.data


def test_edit_post_authenticated_user_empty_content():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.post('/editpost/1', data={
            'postTitle': 'Edited Post',
            'postTags': 'edit, example',
            'postContent': ''
        })

    assert response.status_code == 200
    assert b'post content not be empty' in response.data


def test_edit_post_authenticated_user_not_owner():
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_user('another_user', 'another_user@example.com', 'password456')
    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'another_user', 0,
                     '2023-01-01', '12:00:00')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/editpost/1', follow_redirects=True)

    assert response.status_code == 200
    assert b'this post not yours' in response.data


def test_edit_post_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/editpost/1', follow_redirects=True)

    assert response.status_code == 404
    assert b'you need login for edit a post' in response.data


def test_edit_post_nonexistent_post():
    create_test_user('test_user', 'test_user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'test_user'

        response = client.get('/editpost/999', follow_redirects=True)

    assert response.status_code == 200
    assert b"I don't know what is" in response.data
