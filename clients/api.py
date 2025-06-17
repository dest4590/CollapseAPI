from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from clients.models import Client


@require_POST
def client_launch(request, client_id):
    """
    API endpoint to record a client launch.
    Increments and returns the updated 'runs' count for the specified client.
    """
    client = get_object_or_404(Client, id=client_id)
    runs = client.increment_client_runs()

    return JsonResponse({"status": "success", "client_id": client_id, "runs": runs})


@require_POST
def client_download(request, client_id):
    """
    API endpoint to record a client download.
    Increments and returns the updated 'downloads_count' for the specified client.
    """
    client = get_object_or_404(Client, id=client_id)
    downloads_count = client.increment_downloads()

    return JsonResponse(
        {
            "status": "success",
            "client_id": client_id,
            "downloads_count": downloads_count,
        }
    )
