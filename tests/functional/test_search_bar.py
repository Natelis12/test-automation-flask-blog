from tests.conftest import app


def test_search_bar_route():
    with app.test_client() as client:
        response = client.get('/searchbar')

    assert response.status_code == 200
    assert b'<title>Search</title>' in response.data
    assert b'searchBar searchBarPage' in response.data
