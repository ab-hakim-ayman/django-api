import logging
from datetime import UTC, datetime

from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse

logger = logging.getLogger("django_api.monitoring")
STARTED_AT = datetime.now(UTC)


def liveness_probe(_request):
    uptime_seconds = int((datetime.now(UTC) - STARTED_AT).total_seconds())
    logger.info("liveness_probe_ok")
    return JsonResponse(
        {
            "status": "ok",
            "service": "django-api",
            "uptime_seconds": uptime_seconds,
        }
    )


def readiness_probe(_request):
    try:
        connections["default"].cursor()
    except OperationalError:
        logger.exception("readiness_probe_failed")
        return JsonResponse(
            {"status": "error", "service": "django-api", "database": "unavailable"},
            status=503,
        )

    logger.info("readiness_probe_ok")
    return JsonResponse(
        {"status": "ok", "service": "django-api", "database": "available"}
    )
