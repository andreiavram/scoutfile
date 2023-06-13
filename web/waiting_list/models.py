from django.db import models
from django.db.models import IntegerChoices


class WaitingStatusOptions(IntegerChoices):
    NEW = 0, "New"
    ASSIGNED = 3, "Assigned to unit"
    ACCEPTED = 4, "Accepted (by person)"
    REJECTED = 5, "Rejected (by person)"
    DELAYED = 6, "Delayed"


class WaitingListActions(IntegerChoices):
    CONTACT_PHONE = 1, "Phoned"
    CONTACT_EMAIL = 2, "Emailed"
    DECISION_MADE = 3, "Assigned"
    CLOSED = 4, "Closed (either rejected or accepted)"


class WaitingListPerson(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_person_name = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=14, blank=True)
    contact_email = models.EmailField(blank=True)
    notes = models.TextField()

    status = models.PositiveSmallIntegerField(choices=WaitingStatusOptions.choices, default=WaitingStatusOptions.NEW)
    membru = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL)

    recommended_by = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL, related_name="waitinglist_recommendations")
    family = models.ManyToManyField("structuri.Membru", blank=True, related_name="waitinglist_family")

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.name


class WaitingListAction(models.Model):
    person = models.ForeignKey(WaitingListPerson, on_delete=models.CASCADE)
    old_status = models.PositiveSmallIntegerField(choices=WaitingStatusOptions.choices)
    new_status = models.PositiveSmallIntegerField(choices=WaitingStatusOptions.choices)

    action_by = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)
    action_type = models.PositiveSmallIntegerField(choices=WaitingListActions.choices)
    timestamp = models.DateTimeField()

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.person} moved to {self.get_new_status_display()} by {self.action_by}"
