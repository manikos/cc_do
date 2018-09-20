"""
Custom methods for Jinja2 defined inside
['OPTIONS']['globals'] dict key setting.
"""
from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language_info as gli

from {{ project_name }}.urls import urlpatterns


def lang_info(languages=settings.LANGUAGES):
    """
    Returns a dict of language info using the get_language_info of the
    utils.translation module.
    :param tuple languages: a tuple of tuples ('lang_code', 'lang_name')
    :return: dict
    """
    info = [gli(lang[0]) for lang in languages]
    return info


def app_urls():
    """
    Dict with url_name: url, if url pattern has a "name" declared.
    :return: dict
    """
    return {
        url.name: reverse(url.name) for url in urlpatterns if hasattr(url, "name")
    }

