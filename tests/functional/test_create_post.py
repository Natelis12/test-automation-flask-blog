from tests.conftest import app


def test_create_post_authenticated_user(mocker):
    mocker.patch('routes.createPost.session', {'userName': 'test_user'})
    mock_add_points = mocker.patch('routes.createPost.addPoints')

    response = app.test_client().post('/createpost', data={
        'postTitle': 'Test Post',
        'postTags': 'test, example',
        'postContent': 'This is a test post content.'
    })

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    mock_add_points.assert_called_with(20, 'test_user')


def test_create_post_authenticated_user_empty_content(mocker):
    mocker.patch('routes.createPost.session', {'userName': 'test_user'})

    response = app.test_client().post('/createpost', data={
        'postTitle': 'Test Post',
        'postTags': 'test, example',
        'postContent': ''
    })

    assert response.status_code == 200
    assert b'post content not be empty' in response.data


def test_create_post_unauthenticated_user(mocker):
    mocker.patch('routes.createPost.session', {})

    response = app.test_client().post('/createpost', data={
        'postTitle': 'Test Post',
        'postTags': 'test, example',
        'postContent': 'This is a test post content.'
    }, follow_redirects=True)

    assert response.status_code == 404
    assert b'you need loin for create a post' in response.data
