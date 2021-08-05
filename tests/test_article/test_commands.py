import pytest

from blog.models import Article
from blog.commands import CreateArticleCommand, AlreadyExists


def test_create_article():
    cmd = CreateArticleCommand(author="1@gmail.com", title="1", content="new content")
    article = cmd.execute()

    db_article = Article.get_by_id(article.id)

    assert db_article.id == article.id
    assert db_article.title == article.title
    assert db_article.content == article.content


def test_create_article_already_exists():
    Article(author="hello@gmail.com", title="new three", content="new content").save()

    cmd = CreateArticleCommand(
        author="hello@gmail.com", title="new three", content="new content"
    )

    # cmd.execute()

    with pytest.raises(AlreadyExists):
        cmd.execute()
