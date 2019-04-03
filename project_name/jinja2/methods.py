"""
Custom methods for Jinja2 defined inside
['OPTIONS']['globals'] dict key setting.
"""
from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language_info as gli

# from easy_thumbnails.templatetags import thumbnail as _thumbnail

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


def thumbnail(source, **kwargs):
    """
    If easy_thumbnails is installed, use it with Jinja2 as follows:

    {% templatetag openblock %} set thumb = thumbnail(obj.ImageFieldName, size=(300, 300), quality=75) {% templatetag closeblock %}
	<img
	  src="{{ thumb.url }}"
	  alt="..."
	  width="{{ thumb.width }}"
	  height="{{ thumb.height }}"
	>

	Line 'kwargs["crop"] = ...' may be deleted if "crop" is not the default.

    :param source: an ImageField object
    :param kwargs: size (tuple), crop (bool), quality (int)
    :return: thumbnail object
    """
    kwargs["crop"] = kwargs.get("crop", True)
    return _thumbnail.get_thumbnailer(source).get_thumbnail(kwargs)
