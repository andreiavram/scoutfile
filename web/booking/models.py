from django.db import models
from django.db.models import IntegerChoices


class Space(models.Model):
    """
    Space is a Room or a Campsite section
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    parent = models.ForeignKey("booking.Space", null=True, on_delete=models.CASCADE)


class ServiceUnit(models.Model):
    """
    This models something that you can reserve
    """

    class Types(IntegerChoices):
        BED = 1, "Pat"
        BED_BUNK_DOWN = 2, "Pat supraetajat, jos"
        BED_BUNK_TOP = 3, "Pat supraetajat, sus"
        TENT_2 = 4, "Loc de cort, 1 / 2 persoane"
        TENT_4 = 5, "Loc de cort, 3 / 5 persoane"
        COOKED_MEAL = 6, "Mâncare gătită / catering"
        KITCHEN_SPACE = 7, "Loc de gătit în bucătărie"

    name = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=Types, default=Types.BED)


# this is not easy. In the end, you'll end up with a model that is a Reservation, that should model a person
# taking up a service unit in a period of time
