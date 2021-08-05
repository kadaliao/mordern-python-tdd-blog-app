import pytest
import time
import os
import tempfile

from blog.models import Article


@pytest.fixture(autouse=True)
def database():
    _, filename = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = filename
    Article.create_table(database_name=filename)
    yield
    os.unlink(filename)
