from django.urls import path, re_path

from . import views

urlpatterns = [
    path(r"", views.ArticleListView.as_view(), name="articles-list"),
    path(
        r"articles/<int:pk>/", views.ArticleDetailView.as_view(), name="articles-detail"
    ),
    path(
        r"articles/<int:pk>/<str:type>",
        views.ArticleStarView.as_view(),
        name="articles-star",
    ),
    path(r"authors/", views.AuthorListView.as_view(), name="author-list"),
    path(r"authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path(
        r"author/<int:pk>/<str:type>",
        views.AuthorStarView.as_view(),
        name="author-star",
    ),
]
