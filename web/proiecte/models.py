# coding: utf-8
from builtins import object
from django.db import models
from django.db.models import Sum, IntegerChoices

from taxonomy.models import CategorizedModelMixin

# Create your models here.


PROJECT_VISIBILITY_STATUSES = ((1, "Secret"), (2, "Centrul Local"), (3, "Organizație"), (4, "Public"))


class Project(CategorizedModelMixin, models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    visibility = models.IntegerField(choices=PROJECT_VISIBILITY_STATUSES)
    slug = models.SlugField(unique=True)


# --------------- People & Teams -------------------

class ProjectRole(models.Model):
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)


class ProjectPosition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    starting_on = models.DateTimeField(null=True, blank=True)
    ending_on = models.DateTimeField(null=True, blank=True)

    # TODO: deal with team ownership / assignments here as well
    member = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE, related_name="projects")


# --------------- Budgets & Money -------------------

class ProjectBudgetLine(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("proiecte.ProjectBudgetLine", null=True, blank=True, related_name="sublines", on_delete=models.CASCADE)

    def total_sum(self):
        sum = self.entries.all().aggregate(Sum("sum")).get("sum__sum")
        parent_list = list(self.sublines.all())
        while parent_list:
            line = parent_list.pop()
            sum += line.total_sum()
        return sum


class ProjectBudgetEntry(models.Model):
    class BudgetDirection(IntegerChoices):
        INCOME = 1, "Income"
        EXPENDITURE = 2, "Expediture"

    budget_line = models.ForeignKey(ProjectBudgetLine, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sum = models.FloatField()
    direction = models.PositiveSmallIntegerField(choices=BudgetDirection.choices, default=BudgetDirection.EXPENDITURE)


# --------------- Objectives & Activities -------------------

class ProjectObjective(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_form = models.CharField(max_length=5)


class ProjectActivity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField()

    event = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.SET_NULL)
    task_item = models.ForeignKey("proiecte.TaskItem", null=True, blank=True, on_delete=models.SET_NULL)


TAKSITEM_STATUSES = ()


class TaskItem(models.Model):
    class PriorityOptions(IntegerChoices):
        LOW = 1, "Joasă"
        NORMAL = 2, "Normală"
        HIGH = 3, "Înaltă"

    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)

    parent_task = models.ForeignKey("TaskItem", null=True, blank=True, on_delete=models.SET_NULL)

    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)

    current_state = models.ForeignKey("proiecte.TaskState", null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(choices=PriorityOptions.choices, default=PriorityOptions.NORMAL)

    owner = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class Workflow(models.Model):
    name = models.CharField(max_length=255)


class TaskState(models.Model):
    name = models.CharField(max_length=255)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    available_states = models.ManyToManyField("TaskState", blank=True)


class TaskStateHistory(models.Model):
    task = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    state = models.ForeignKey(TaskState, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255, null=True, blank=True)


class TaskItemResponsibility(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)
    owner = models.ForeignKey("structuri.Membru", related_name="task_associations", on_delete=models.CASCADE)
