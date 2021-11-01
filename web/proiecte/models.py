# coding: utf-8
from builtins import object
from django.db import models

# Create your models here.


PROJECT_VISIBILITY_STATUSES = ((1, u"Secret"), (2, u"Centrul Local"), (3, u"Organizație"), (4, u"Public"))


class Project(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    visibility = models.IntegerField(choices=PROJECT_VISIBILITY_STATUSES)
    slug = models.SlugField(unique=True)


class ProjectRole(models.Model):
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)


class ProjectPosition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    starting_on = models.DateTimeField(null=True, blank=True)
    ending_on = models.DateTimeField(null=True, blank=True)
    member = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)


TAKSITEM_STATUSES = ()


class TaskItem(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)

    parent_task = models.ForeignKey("TaskItem", null=True, blank=True, on_delete=models.SET_NULL)

    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)

    #status = models.CharField(max_length=255, choices=TAKSITEM_STATUSES, default="idea")
    owner = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ["-start_date"]

    def __str__(self):
        return self.titled


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
