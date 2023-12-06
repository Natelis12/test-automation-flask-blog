from tests.conftest import app, create_test_post


def test_view_existing_post(mocker):
    mocker.patch('routes.post.session', {'userName': 'test_user'})
    mocker.patch('app.getProfilePicture', return_value='/static/default_profile_picture.png')

    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')
    with app.test_request_context('/post/1', method='GET'):
        response = app.test_client().get('/post/1')

    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data


def test_view_non_existing_post(mocker):
    mocker.patch('routes.post.session', {'userName': 'test_user'})
    mocker.patch('app.getProfilePicture', return_value='/static/default_profile_picture.png')

    with app.test_request_context('/post/999', method='GET'):
        response = app.test_client().get('/post/999')

    assert response.status_code == 200
    assert b"I don't know what is" in response.data


def test_comment_on_existing_post(mocker):
    mocker.patch('routes.post.session', {'userName': 'test_user'})
    mocker.patch('routes.post.addPoints')
    mocker.patch('app.getProfilePicture', return_value='/static/default_profile_picture.png')

    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')

    with app.test_request_context('/post/1', method='POST'):
        response = app.test_client().post('/post/1', data={'comment': 'This is a comment.'})

    assert response.status_code == 302
    assert response.headers['Location'] == '/post/1'


def test_comment_on_non_existing_post(mocker):
    mocker.patch('routes.post.session', {'userName': 'test_user'})
    mocker.patch('app.getProfilePicture', return_value='/static/default_profile_picture.png')

    with app.test_request_context('/post/999', method='POST'):
        response = app.test_client().post('/post/999', data={'comment': 'This is a comment.'})

    assert response.status_code == 200
    assert b"I don't know what is" in response.data
