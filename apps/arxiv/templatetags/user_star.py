from django import template

register = template.Library()


@register.simple_tag
def is_user_start(article, user):
    return article.user_starts.filter(pk=user.pk).exists()
