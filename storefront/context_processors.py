from django.conf import settings


def deployment_settings(request):
    return {
        "PIXEL_SCRIPT_URL": settings.PIXEL_SCRIPT_URL,
        "PIXEL_COLLECTOR_URL": settings.PIXEL_COLLECTOR_URL,
        "PIXEL_ID": settings.PIXEL_ID,
    }
