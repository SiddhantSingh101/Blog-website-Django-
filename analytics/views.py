import json

from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import PixelEvent


def collector_dashboard(request):
    events = PixelEvent.objects.all()[:100]
    total_events = PixelEvent.objects.count()
    unique_users = PixelEvent.objects.values("user_id").distinct().count()

    context = {
        "events": events,
        "total_events": total_events,
        "unique_users": unique_users,
    }
    return render(request, "analytics/dashboard.html", context)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def collect_event(request):
    if request.method == "OPTIONS":
        return _cors_response(HttpResponse(status=204), request)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _cors_response(JsonResponse({"error": "Invalid JSON payload."}, status=400), request)

    required_fields = [
        "event_id",
        "advertiser_id",
        "event_type",
        "user_id",
        "page_url",
        "client_timestamp",
        "source",
    ]
    missing_fields = [field for field in required_fields if not payload.get(field)]

    if missing_fields:
        return _cors_response(
            JsonResponse(
                {"error": "Missing required fields.", "missing": missing_fields},
                status=400,
            ),
            request,
        )

    event, created = PixelEvent.objects.get_or_create(
        event_id=payload["event_id"],
        defaults={
            "advertiser_id": payload["advertiser_id"],
            "event_type": payload["event_type"],
            "user_id": payload["user_id"],
            "user_email": payload.get("user_email") or "",
            "page_url": payload["page_url"],
            "referrer": payload.get("referrer") or "",
            "client_timestamp": parse_datetime(payload["client_timestamp"]),
            "source": payload["source"],
            "ip_address": _client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        },
    )

    return _cors_response(
        JsonResponse(
            {
                "status": "stored" if created else "duplicate",
                "event_id": event.event_id,
            },
            status=201 if created else 200,
        ),
        request,
    )


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def _cors_response(response, request):
    allowed_origins = getattr(settings, "COLLECTOR_ALLOWED_ORIGINS", [])
    origin = request.META.get("HTTP_ORIGIN")
    if origin in allowed_origins:
        response["Access-Control-Allow-Origin"] = origin
    elif allowed_origins:
        response["Access-Control-Allow-Origin"] = allowed_origins[0]
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response
