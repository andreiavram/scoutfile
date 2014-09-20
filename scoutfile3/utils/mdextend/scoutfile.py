# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from django.template.loader import render_to_string

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
        from documente.models import Document

        shortcode = m.group(3)
        components = shortcode.split("#")
        print components, shortcode
        tag_registry = {
            "doc": "documente/markdown/document.html"
        }

        template_name = tag_registry.get(components[0], None)
        print template_name, "template name"
        if template_name is None:
            return ""

        html = render_to_string(template_name, {"object": Document.objects.get(id=int(components[1]))})
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