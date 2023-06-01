from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# TODO: decide on using MPTT here?
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    icon = models.ImageField("categories/icons/", null=True, blank=True)

    parent = models.ForeignKey("taxonomy.Category", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()


class CategorizedModelMixin:
    def categories(self):
        return CategoryItem.objects.filter(
            content_type = ContentType.objects.get_for_model(self),
            object_id = self.id
        )
