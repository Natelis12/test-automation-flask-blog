from random import randint

import pytest

from app import app


@pytest.fixture()
def test_app():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


def test_post_post_method_200(client):
    response = client.post(f"/post/{randint(1000, 10000)}")
    assert response.status_code == 200


def test_post_post_method_404(client):
    response = client.post("/post/")
    assert response.status_code == 404


def test_post_get_method(client):
    get_response = client.get(f"/post/{1}")
    assert get_response.status_code == 200


def test_post_get_method_404(client):
    response = client.get("/post/")
    assert response.status_code == 404
