# coding: utf-8
from django.db import models

# Create your models here.


PROJECT_VISIBILITY_STATUSES = ((1, "Secret"), (2, u"Centrul Local"), (3, u"Organizație", (4, u"Public")))


class Project(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    visibility = models.IntegerField(choices=PROJECT_VISIBILITY_STATUSES)
    slug = models.SlugField(unique=True)


class ProjectRole(models.Model):
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)


class ProjectPosition(models.Model):
    project = models.ForeignKey(Project)
    role = models.ForeignKey(ProjectRole)
    starting_on = models.DateTimeField(null=True, blank=True)
    ending_on = models.DateTimeField(null=True, blank=True)
    member = models.ForeignKey("structuri.Membru")


TAKSITEM_STATUSES = ()


class TaskItem(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)

    parent_task = models.ForeignKey("TaskItem", null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)

    #status = models.CharField(max_length=255, choices=TAKSITEM_STATUSES, default="idea")
    owner = models.ForeignKey("structuri.Membru", null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return self.titled


class Workflow(models.Model):
    name = models.CharField(max_length=255)


class TaskState(models.Model):
    name = models.CharField(max_length=255)
    workflow = models.ForeignKey(Workflow)
    available_states = models.ManyToManyField("TaskState", null=True, blank=True)


class TaskStateHistory(models.Model):
    task = models.ForeignKey(TaskItem)
    state = models.ForeignKey(TaskState)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255, null=True, blank=True)


class TaskItemResponsibility(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey("structuri.Membru")
    owner = models.ForeignKey("structuri.Membru", related_name="task_associations")


