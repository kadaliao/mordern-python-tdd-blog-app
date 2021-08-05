import json
import requests
import pathlib
from typing import ContextManager
import pytest
from jsonschema import validate, RefResolver
from blog.app import app
from blog.models import Article


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def validate_payload(paylaod, schema_name):
    schema_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/schemas")

    schema = json.loads(pathlib.Path(f"{schema_dir}/{schema_name}").read_text())

    validate(
        paylaod,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schema_dir}/{schema_name}").absolute()),
            schema,
        ),
    )


def test_get_article(client):
    article = Article(
        author="jane@doe.com",
        title="New Article",
        content="Super extra awesome article",
    ).save()
    resp = client.get(f"/article/{article.id}/", content_type="application/json")

    validate_payload(resp.json, "Article.json")


def test_list_articles(client):
    Article(
        author="jane@doe.com",
        title="New Article",
        content="Super extra awesome article",
    ).save()
    resp = client.get("/article-list/", content_type="application/json")

    validate_payload(resp.json, "ArticleList.json")


@pytest.mark.parametrize(
    "data",
    [
        {
            "author": "John Doe",
            "title": "New Article",
            "content": "Some extra awesome content",
        },
        {
            "author": "John Doe",
            "title": "New Article",
        },
        {"author": "John Doe", "title": None, "content": "Some extra awesome content"},
    ],
)
def test_create_article_bad_request(client, data):
    """
    GIVEN request data with invalid values or missing attributes
    WHEN endpoint /create-article/ is called
    THEN it should return status 400 and JSON body
    """
    response = client.post(
        "/create-article/",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json is not None


@pytest.mark.e2e
def test_create_list_get(client):
    requests.post(
        "http://127.0.0.1:5000/creacreate-article/",
        json=dict(author="john@doe.com", title="new article", content="new content"),
    )
    response = requests.get("http://127.0.0.1:5000/article-list/")
    articles = response.json()

    response = requests.get(f"http://127.0.0.1:5000/article/{articles[0]['id']}")
    assert response.status_code == 200
