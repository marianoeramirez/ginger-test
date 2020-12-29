from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView, DetailView

from . import models, mixins


class ArticleListView(ListView):
    model = models.Article
    paginate_by = 10


class ArticleDetailView(DetailView):
    queryset = models.Article.objects.all()


class AuthorListView(ListView):
    queryset = (
        models.Author.objects.all().annotate(count=Count("article")).order_by("-count")
    )
    paginate_by = 10


class AuthorDetailView(DetailView):
    queryset = models.Author.objects.all()


class ArticleStarView(LoginRequiredMixin, mixins.BaseStartUnstarMixin):
    queryset = models.Article.objects.all()


class AuthorStarView(LoginRequiredMixin, mixins.BaseStartUnstarMixin):
    queryset = models.Author.objects.all()
