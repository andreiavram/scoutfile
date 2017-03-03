# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string
from markdown import Extension
from markdown.inlinepatterns import Pattern

# match ^, at least one character that is not ^, and ^ again
SCOUTFILE_RE = r'(\[{2})([^\]]+)(\]){2}'


# def makeExtension(configs=None):
#     """Inform Markdown of the existence of the extension."""
#     return SuperscriptExtension(configs=dict(configs))


class ScoutfilePattern(Pattern):
    def __init__(self, markdown):
        super(ScoutfilePattern, self).__init__(SCOUTFILE_RE)
        self.markdown = markdown

    def handleMatch(self, m):
        from documente import Document
        from album import Imagine

        shortcode = m.group(3)
        components = shortcode.split("#")

        tag_registry = {
            "doc": {
                "template": "documente/markdown/document.html",
                "model": Document
            },
            "img": {
                "template": "album/markdown/imagine.html",
                "model": Imagine
            }
        }

        descriptor = tag_registry.get(components[0], {})
        template_name = descriptor.get("template")

        if template_name is None:
            return ""

        html = render_to_string(template_name, {"object": descriptor.get("model").objects.get(id=int(components[1]))})
        return self.markdown.htmlStash.store(html)


class ScoutfileMarkdown(Extension):
    def __init__(self, renderer=None):
        super(ScoutfileMarkdown, self).__init__()
        self.renderer = renderer

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('scoutfile', ScoutfilePattern(md), '_begin')
        md.registerExtension(self)


def makeExtension(configs=None):  # pragma: no cover
    return ScoutfileMarkdown()