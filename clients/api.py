from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from clients.models import Client
from client_statistics.models import ClientLaunchStats, ClientDownloadStats


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
