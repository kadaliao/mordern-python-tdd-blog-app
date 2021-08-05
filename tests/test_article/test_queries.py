from pydantic.main import ANNOTATED_FIELD_UNTOUCHED_TYPES
from blog.models import Article
from blog.queries import ListArticlesQuery, GetArticleByIDQuery


def test_list_articles():
    Article(
        author="jane@doe.com",
        title="new article",
        content="super extra awesome content",
    ).save()

    Article(
        author="jane@doe.com", title="Another Article", content="Super awesome article"
    ).save()

    query = ListArticlesQuery()

    assert len(query.execute()) == 2


def test_get_article_by_id():
    article = Article(
        author="jane@doe.com", title="new article", content="hello content"
    ).save()

    query = GetArticleByIDQuery(id=article.id)

    assert query.execute().id == article.id
