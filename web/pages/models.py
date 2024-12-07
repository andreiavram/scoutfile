from django.db import models
from django.forms import CheckboxSelectMultiple
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, Orderable
from wagtail.search import index


class WikiPageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify pages by this category'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ]

    class Meta:
        verbose_name = "Wiki Category"
        verbose_name_plural = "Wiki Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class WikiPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "WikiPage",
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]




class WikiPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True)

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    categories = ParentalManyToManyField("pages.WikiPageCategory", blank=True)
    tags = ClusterTaggableManager(through=WikiPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('related_links', heading="Related links", label="Related link"),
        FieldPanel("tags"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=CheckboxSelectMultiple)
            ],
            heading="Categories"
        )
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('cover_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["categories"] = WikiPageCategory.objects.all()
        return context


class WikiPageRelatedLink(Orderable):
    page = ParentalKey(WikiPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

