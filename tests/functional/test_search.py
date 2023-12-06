import pytest

from tests.conftest import app, create_test_comment, create_test_post, create_test_user


@pytest.mark.parametrize('query, result', [
    ('test_user', b'test_user'),
    ('Test Post 1', b'Test Post 1'),
    ('test, example', b'test, example'),
])
def test_search_with_results(query, result):
    create_test_user('test_user', 'test_user@example.com', 'password123')
    create_test_post(1, 'Test Post 1', 'test, example', 'This is a test post.', 'test_user', 0,
                     '2023-01-01', '12:00:00')
    create_test_comment(1, 'Test Comment 1', 'test_user', '2023-01-01', '12:00:00')

    with app.test_client() as client:
        response = client.get(f'/search/{query}')

    assert response.status_code == 200
    assert result in response.data


def test_search_with_no_results():
    with app.test_client() as client:
        response = client.get('/search/nonexistent_user')

    assert response.status_code == 200
    assert b'not found' in response.data


def test_search_with_empty_query():
    with app.test_client() as client:
        response = client.get('/search/')

    assert response.status_code == 404
    assert b"I don't know what is" in response.data
