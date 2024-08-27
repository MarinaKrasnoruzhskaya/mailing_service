from django.core.cache import cache

from blog.models import BlogPost
from config import settings


def get_blogpost_for_cache():
    """Функция получает список постов из кэша или из БД и тогда записывает в кэш"""
    if settings.CACHE_ENABLED:
        key = 'blogposts'
        blogposts_list = cache.get(key)
        if blogposts_list is None:
            blogposts_list = BlogPost.objects.filter(is_published=True)
            cache.set(key, blogposts_list)
    else:
        blogposts_list = BlogPost.objects.filter(is_published=True)

    return blogposts_list
