from django.contrib import admin

from waiting_list.models import WaitingListPerson, WaitingListAction


class WaitingListActionInline(admin.TabularInline):
    model = WaitingListAction


@admin.register(WaitingListPerson)
class WaitingListPersonAdmin(admin.ModelAdmin):
    list_display = ["name", "timestamp", "date_of_birth", "contact_person_name", "contact_phone", "contact_email", "status", "has_family", "has_member_recommendation"]
    list_filter = ["status", ]
    inlines = [WaitingListActionInline, ]

    @admin.display(boolean=True, description='Familie')
    def has_family(self, obj):
        return obj.family.count() > 0

    @admin.display(boolean=True, description='Recomandare')
    def has_member_recommendation(self, obj):
        return obj.recommended_by is not None


@admin.register(WaitingListAction)
class WaitingListActionAdmin(admin.ModelAdmin):
    list_display = ["person", "old_status", "new_status", "action_by", "action_type", "timestamp", "notes"]
    list_filter = ["action_by", "old_status", "new_status"]
