from django import template
from django.conf import settings
from django.template.defaultfilters import slugify

from wagtail.wagtailcore.utils import camelcase_to_underscore


register = template.Library()


# Return the model name/"content type" as a css-friendly string e.g blog-page, news-listing-page
# Usage: {% verbatim %}{{ self|content_type_slugified }}{% endverbatim %}
@register.filter
def content_type_slugified(model):
    return slugify(model.__class__.__name__)
