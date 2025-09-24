from django.contrib import admin

from redirects.models import PhysicalTag


# Register your models here.
@admin.register(PhysicalTag)
class PhysicalTagAdmin(admin.ModelAdmin):
    list_display = ["token", "ref", "to_url", "hit_count", "tag_type", "url"]
    search_fields = ["token"]


