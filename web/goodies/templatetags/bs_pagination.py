# coding: utf-8
from django import template

register = template.Library()

from django_pagination_bootstrap.templatetags.pagination_tags import paginate
register.inclusion_tag("paginate_bs2.html", takes_context=True, name="paginate_bs2")(paginate)
