from django.contrib import admin

from properties.models import Property, PropertyControlElement, AccessPermission, AccessLog


class PropertyControlInline(admin.TabularInline):
    model = PropertyControlElement
    extra = 1


class AccessLogInline(admin.TabularInline):
    model = AccessLog
    extra = 0

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "ha_base_url"]
    inlines = [PropertyControlInline, ]


@admin.register(PropertyControlElement)
class PropertyControlElement(admin.ModelAdmin):
    list_display = ["name", "ha_id", "service_action", "property"]
    list_filter = ["property"]
    inlines = [AccessLogInline, ]


@admin.register(AccessPermission)
class AccessPermissionAdmin(admin.ModelAdmin):
    list_display = ["control_element", "person", "date_start", "date_end"]
    list_filter = ["control_element__property"]


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ["control_element", "person", "timestamp", "result"]
    ordering = ["-timestamp"]
    list_filter = ["control_element", "person"]

