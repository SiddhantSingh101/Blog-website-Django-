from django.db import models


class PixelEvent(models.Model):
    event_id = models.CharField(max_length=80, unique=True)
    advertiser_id = models.CharField(max_length=80, db_index=True)
    event_type = models.CharField(max_length=80)
    user_id = models.CharField(max_length=120, db_index=True)
    user_email = models.EmailField(blank=True, db_index=True)
    page_url = models.URLField(max_length=2048)
    referrer = models.URLField(max_length=2048, blank=True)
    client_timestamp = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=40, default="web")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} from {self.user_id}"
