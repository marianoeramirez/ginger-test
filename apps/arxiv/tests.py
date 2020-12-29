from unittest import mock
import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from . import models

TEST_RESPONSE = {
    "bozo": False,
    "entries": [
        {
            "id": "http://arxiv.org/abs/2012.12258v1",
            "link": "http://arxiv.org/abs/2012.12258v1",
            "updated": "2020-12-22T18:56:39Z",
            "published": "2020-12-22T18:56:39Z",
            "title": "Underwater image filtering: methods, datasets and evaluation",
            "summary": "Underwater images are degraded by the selective attenuation...",
            "authors": [
                {"name": "Harley Queen"},
                {"name": "Batman"},
                {"name": "Joker"},
            ],
            "links": [
                {
                    "href": "http://arxiv.org/abs/2012.12258v1",
                    "rel": "alternate",
                    "type": "text/html",
                },
                {
                    "title": "pdf",
                    "href": "http://arxiv.org/pdf/2012.12258v1",
                    "rel": "related",
                    "type": "application/pdf",
                },
            ],
        },
        {
            "id": "http://arxiv.org/abs/2012.12257v1",
            "link": "http://arxiv.org/abs/2012.12257v1",
            "updated": "2019-12-22T18:56:39Z",
            "published": "2019-12-22T18:56:39Z",
            "title": "Machine Learning analysis",
            "summary": "machine learning qa...",
            "authors": [
                {"name": "Robert Patinson"},
            ],
            "links": [
                {
                    "href": "http://arxiv.org/abs/2012.12257v1",
                    "rel": "alternate",
                    "type": "text/html",
                },
                {
                    "title": "pdf",
                    "href": "http://arxiv.org/pdf/2012.12257v1",
                    "rel": "related",
                    "type": "application/pdf",
                },
            ],
        },
    ],
    "feed": {
        "opensearch_totalresults": "2",
        "opensearch_startindex": "0",
        "opensearch_itemsperpage": "2",
    },
    "headers": {},
}


@pytest.mark.django_db
class TestCommand:
    @mock.patch("feedparser.parse", return_value=TEST_RESPONSE)
    def test_command(self, mock_parser):
        """We chekc here with a harcoded request to check that it imported
        only one element and worked, because the second element have more than 6 months
        """
        call_command("arxiv_data", items_page=2)
        assert mock_parser.called
        assert "start=0&max_results=2" in mock_parser.call_args.args[0]

        assert models.Article.objects.count() == 1
        assert models.Author.objects.count() == 3
        assert (
            models.Article.objects.first().title
            == "Underwater image filtering: methods, datasets and evaluation"
        )


@pytest.fixture
def author():
    return models.Author.objects.create(name="Batman")


@pytest.fixture
def author2():
    return models.Author.objects.create(name="Superman")


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username="someone", password="something")


@pytest.fixture
def article(author):
    instance = models.Article.objects.create(
        title="Analysis of", remote_id="1", published=timezone.now()
    )
    instance.authors.add(author)
    return instance


@pytest.fixture
def article2(author2):
    instance = models.Article.objects.create(
        title="Machine Learning", remote_id="2", published=timezone.now()
    )
    instance.authors.add(author2)
    return instance


@pytest.fixture
def article3(author):
    instance = models.Article.objects.create(
        title="Image analysis", remote_id="3", published=timezone.now()
    )
    instance.authors.add(author)
    return instance


@pytest.mark.django_db
class TestAuthorsViews:
    def test_list(self, client, author, article, article2, article3):
        response = client.get(reverse("author-list"))
        assert response.status_code == 200
        assert "Batman</a> Articles: 2" in str(response.content)
        assert "Superman</a> Articles: 1" in str(response.content)

    def test_detail(self, client, author, article, article2, article3):
        response = client.get(reverse("author-detail", args=(author.pk,)))
        assert response.status_code == 200
        assert "<h3>Batman</h3>" in str(response.content)

    def test_star(self, client, author, user):
        client.force_login(user)
        HTTP_REFERER = "/test"

        response = client.get(
            reverse("author-star", args=(author.pk, "star")), HTTP_REFERER=HTTP_REFERER
        )
        assert response.status_code == 302
        assert response.url == HTTP_REFERER
        assert author.user_starts.filter(pk=user.pk).exists()


@pytest.mark.django_db
class TestArticlesViews:
    def test_list(self, client, author, article, article2, article3):
        response = client.get(reverse("articles-list"))
        assert response.status_code == 200
        assert "Analysis of" in str(response.content)
        assert "Machine Learning" in str(response.content)
        assert "Image analysis" in str(response.content)

    def test_detail(self, client, author, article, article2, article3):
        response = client.get(reverse("articles-detail", args=(article.pk,)))
        assert response.status_code == 200
        assert "<h3>Analysis of</h3>" in str(response.content)
