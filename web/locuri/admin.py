from django.contrib import admin

from locuri.models import GPXTrack


@admin.register(GPXTrack)
class GPXTrackAdmin(admin.ModelAdmin):
    list_display = ["title", "created_by", "positive_altitude"]
    list_filter = ["created_by"]
    actions = ["process_gpx"]

    @admin.action(description="Process GPX file")
    def process_gpx(self, request, queryset):
        for gpx_track in queryset:
            if gpx_track.gpx_file:
                gpx_track.process_gpx()
