from django.contrib import admin

from redirects.models import PhysicalTag


# Register your models here.
@admin.register(PhysicalTag)
class PhysicalTagAdmin(admin.ModelAdmin):
    list_display = ["ref", "token", "to_url", "hit_count", "tag_type", "url", "png_qr_image_url"]


