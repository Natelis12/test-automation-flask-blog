from tests.conftest import app, create_test_post


def test_delete_post_authenticated_user_own_post(mocker):
    mocker.patch('routes.deletePost.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deletePost.message')

    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')

    response = app.test_client().get('/deletepost/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    mock_message.assert_called_once_with('2', 'POST: "1" DELETED')


def test_delete_post_authenticated_user_other_user_post(mocker):
    mocker.patch('routes.deletePost.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deletePost.message')

    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'other_user', 0,
                     '2023-01-01', '12:00:00')

    response = app.test_client().get('/deletepost/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    mock_message.assert_called_once_with(
        '1', 'POST: "1" NOT DELETED "1" DOES NOT BELONG TO USER: test_user')


def test_delete_post_unauthenticated_user(mocker):
    mocker.patch('routes.deletePost.session', {})
    mock_message = mocker.patch('routes.deletePost.message')

    response = app.test_client().get('/deletepost/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/login/redirect=&post&1'
    mock_message.assert_called_once_with('1', 'USER NEEDS TO LOGIN FOR DELETE POST: "1"')
