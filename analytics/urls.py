from django.urls import path

from . import views


urlpatterns = [
    path("", views.collector_dashboard, name="collector_dashboard"),
    path("api/events/", views.collect_event, name="collect_event"),
]
