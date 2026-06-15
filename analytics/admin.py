from django.contrib import admin

from .models import PixelEvent


@admin.register(PixelEvent)
class PixelEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_id",
        "advertiser_id",
        "event_type",
        "user_id",
        "user_email",
        "source",
        "created_at",
    )
    list_filter = ("advertiser_id", "event_type", "source", "created_at")
    search_fields = ("event_id", "advertiser_id", "user_id", "user_email", "page_url", "referrer")
    readonly_fields = ("created_at",)
