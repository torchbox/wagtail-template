from django import template
from django.conf import settings
from django.template.defaultfilters import slugify

from wagtail.wagtailcore.util import camelcase_to_underscore

from core.models import *

register = template.Library()

# Return the kind of field as a string e.g boolean_field
# Usage: {{ field|field_type }}
@register.filter
def field_type(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


# Return the kind of field widget as a string e.g checkbox_input
# Usage: {{ field|widget_type }}
@register.filter
def widget_type(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)


# Return the model name/"content type" as a css-friendly string e.g blog-page, news-listing-page
# Usage: {{ self|content_type_slugified }}
@register.filter
def content_type_slugified(model):
    return slugify(model.__class__.__name__)
