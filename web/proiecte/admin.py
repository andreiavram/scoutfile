import datetime

from django.contrib import admin

from proiecte.models import Project, ProjectRole, ProjectPosition, ProjectBudgetLine, ProjectBudgetEntry, \
    ProjectObjective, ProjectActivity


class ProjectActivityInline(admin.StackedInline):
    model = ProjectActivity
    extra = 1


class ProjectObjectiveInline(admin.StackedInline):
    model = ProjectObjective
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "visibility"]
    inlines = [ProjectActivityInline, ProjectObjectiveInline]

@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


@admin.register(ProjectPosition)
class ProjectPositionAdmin(admin.ModelAdmin):
    list_display = ["role", "project", "starting_on", "ending_on", "is_active", "member"]
    list_filter = ["project", ]


@admin.register(ProjectBudgetLine)
class ProjectBudgetLineAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "parent", "total_sum"]
    list_filter = ["project"]


@admin.register(ProjectBudgetEntry)
class ProjectBudgetEntryAdmin(admin.ModelAdmin):
    list_display = ["title", "budget_line", "description", "sum", "direction"]


@admin.register(ProjectObjective)
class ProjectObjectiveAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "project", "short_form"]
    list_filter = ["project"]


@admin.register(ProjectActivity)
class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "description", "date_start", "date_end", "event", "task_item"]
