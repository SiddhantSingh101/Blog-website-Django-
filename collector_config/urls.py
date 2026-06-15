from django.contrib import admin
from django.urls import path

from analytics import views as analytics_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", analytics_views.collector_dashboard, name="collector_dashboard"),
    path("collector/", analytics_views.collector_dashboard, name="collector_dashboard_alt"),
    path("api/events/", analytics_views.collect_event, name="collect_event"),
]
