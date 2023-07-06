from django.db import models
from django.db.models import TextChoices


class RecipeSuitability(models.Model):
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    base_multiplier = models.IntegerField(default=10)
    suitability = models.ManyToManyField(RecipeSuitability)


class RecipeStep(models.Model):
    order = models.PositiveIntegerField()


class MeasurementUnit(TextChoices):
    GRAM = "gram", "g"
    KILOGRAM = "kilogram", "Kg"
    MILILITER = "milliliter", "ml"
    PIECE = "piece", "bucată"

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=255, choices=)





