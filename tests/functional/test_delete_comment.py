from tests.conftest import app, create_test_comment


def test_delete_comment_authenticated_user_own_comment(mocker):
    """
    Test deleting a comment by an authenticated user who owns the comment.
    """
    mocker.patch('routes.deleteComment.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deleteComment.message')

    create_test_comment(1, 'This is a test comment.', 'test_user', '2023-01-01', '12:00:00')

    response = app.test_client().get('/deletecomment/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/test'
    mock_message.assert_called_once_with('2', 'COMMENT: "1" DELETED')


def test_delete_comment_authenticated_user_other_user_comment(mocker):
    """
    Test an authenticated user attempting to delete a comment created by another user.
    """
    mocker.patch('routes.deleteComment.session', {'userName': 'test_user'})
    mock_message = mocker.patch('routes.deleteComment.message')

    create_test_comment(1, 'This is a test comment.', 'other_user', '2023-01-01', '12:00:00')

    response = app.test_client().get('/deletecomment/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/test'
    mock_message.assert_called_once_with(
        '1', 'COMMENT: "1" NOT DELETED "1" DOES NOT BELONG TO test_user')


def test_delete_comment_unauthenticated_user(mocker):
    """
    Test an unauthenticated user attempting to delete a comment.
    """
    mocker.patch('routes.deleteComment.session', {})
    mock_message = mocker.patch('routes.deleteComment.message')

    response = app.test_client().get('/deletecomment/1/redirect=test')

    assert response.status_code == 302
    assert response.headers['Location'] == '/test'
    mock_message.assert_called_once_with('1', 'USER NEEDS TO LOGIN FOR DELETE COMMENT: 1')
