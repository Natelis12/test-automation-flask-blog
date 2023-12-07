from tests.conftest import app, create_test_comment, create_test_post, create_test_user


def test_view_user_found(mocker):
    mock_message = mocker.patch('routes.user.message')
    mock_render_template = mocker.patch('routes.user.render_template')

    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')
    create_test_comment(1, 'This is a comment.', 'test_user', '2023-01-01', '12:00:00')

    response = app.test_client().get('/user/test_user')

    assert response.status_code == 200
    assert mock_message.called
    assert mock_render_template.called
    assert mock_render_template.call_args[0][0] == 'user.html'
    assert mock_message.call_args[0][1] == 'USER: "test_user"s PAGE LOADED'
    assert mock_render_template.call_args[1]['user'][1] == 'test_user'
    assert mock_render_template.call_args[1]['views'] == 0
    assert mock_render_template.call_args[1]['showPosts'] is True
    assert mock_render_template.call_args[1]['showComments'] is True


def test_view_user_not_found(mocker):
    mock_message = mocker.patch('routes.user.message')
    mock_render_template = mocker.patch('routes.user.render_template')

    response = app.test_client().get('/user/nonexistent_user')

    assert response.status_code == 200
    assert mock_message.called
    assert mock_render_template.called
    assert mock_render_template.call_args[0][0] == '404.html'
    assert mock_message.call_args[0][1] == 'USER: "nonexistent_user" NOT FOUND'


def test_view_user_no_posts_or_comments(mocker):
    mock_message = mocker.patch('routes.user.message')
    mock_render_template = mocker.patch('routes.user.render_template')

    create_test_user('test_user', 'test_user@example.com', 'password123')

    response = app.test_client().get('/user/test_user')

    assert response.status_code == 200
    assert mock_message.called
    assert mock_render_template.called
    assert mock_render_template.call_args[0][0] == 'user.html'
    assert mock_message.call_args[0][1] == 'USER: "test_user"s PAGE LOADED'
    assert mock_render_template.call_args[1]['user'][1] == 'test_user'
    assert mock_render_template.call_args[1]['views'] == 0
    assert mock_render_template.call_args[1]['showPosts'] is False
    assert mock_render_template.call_args[1]['showComments'] is False
