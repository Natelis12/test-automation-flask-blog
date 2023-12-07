from tests.conftest import app, create_test_user


def test_set_user_role_authenticated_admin():
    create_test_user('admin_user', 'admin_user@example.com', 'password123', role='admin')
    create_test_user('user_to_change', 'user@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'admin_user'

        response = client.get('/setuserrole/user_to_change/new_role')

    assert response.status_code == 302
    assert b'/admin/users' in response.data


def test_set_user_role_authenticated_non_admin():
    create_test_user('regular_user', 'user@example.com', 'password123')
    create_test_user('user_to_change', 'user_to_change@example.com', 'password123')

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['userName'] = 'regular_user'

        response = client.get('/setuserrole/user_to_change/new_role')

    assert response.status_code == 302
    assert b'/' in response.data


def test_set_user_role_unauthenticated_user():
    with app.test_client() as client:
        response = client.get('/setuserrole/user_to_change/new_role')

    assert response.status_code == 302
    assert b'/' in response.data
