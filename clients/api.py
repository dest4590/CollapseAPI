import mimetypes
import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from client_statistics.models import (
    ClientDownloadStats,
    ClientLaunchStats,
    LoaderLaunchStats,
)
from clients.models import Client
from clients.serializers import ClientDetailedSerializer


@csrf_exempt
@require_POST
def client_launch(request, client_id):
    """
    API endpoint to record a client launch.
    Increments the launches counter and returns the updated count.
    """
    client = get_object_or_404(Client, id=client_id)

    launches = ClientLaunchStats.record_launch(client_id)

    return JsonResponse({"status": "success", "client_id": client_id, "runs": launches})


@csrf_exempt
@require_POST
def client_download(request, client_id):
    """
    API endpoint to record a client download.
    Increments the downloads counter and returns the updated count.
    """
    client = get_object_or_404(Client, id=client_id)

    downloads = ClientDownloadStats.record_download(client_id)

    return JsonResponse(
        {
            "status": "success",
            "client_id": client_id,
            "downloads_count": downloads,
        }
    )


@csrf_exempt
@require_POST
def loader_launch(request):
    """
    API endpoint to record a loader launch.
    Increments the launches counter and returns the updated count.
    """
    launches = LoaderLaunchStats.record_launch()

    return JsonResponse({"status": "success", "runs": launches})


@csrf_exempt
@require_GET
def client_statistics(request):
    """
    API endpoint to get client statistics.
    Returns JSON with total launches and downloads for all clients.
    """
    total_launches = ClientLaunchStats.get_total_launches()
    total_downloads = ClientDownloadStats.get_total_downloads()

    return JsonResponse(
        {"total_launches": total_launches, "total_downloads": total_downloads}
    )


@require_GET
def client_screenshots(request, client_id):
    """
    API endpoint to get client screenshots.
    Returns JSON with all screenshot URLs or 404 if not found.
    """
    client = get_object_or_404(Client, id=client_id)

    screenshots = client.screenshots.all()
    if not screenshots.exists():
        return JsonResponse({"error": "No screenshots available"}, status=404)

    screenshot_urls = []
    for screenshot in screenshots:
        screenshot_urls.append(
            {
                "id": screenshot.id,
                "url": request.build_absolute_uri(screenshot.image.url),
                "order": screenshot.order,
            }
        )

    return JsonResponse({"client_id": client_id, "screenshots": screenshot_urls})


@require_GET
def client_detailed(request, client_id):
    """
    API endpoint to get detailed client information including changelog and screenshots.
    """
    client = get_object_or_404(Client, id=client_id)
    serializer = ClientDetailedSerializer(client, context={"request": request})
    return JsonResponse(serializer.data)
