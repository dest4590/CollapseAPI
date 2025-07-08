import os
import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def send_heartbeat():
    """
    Sends a heartbeat GET request to the external monitoring service.
    """
    heartbeat_url = os.getenv("HEARTBEAT_URL")

    if not heartbeat_url:
        logger.warning(
            "HEARTBEAT_URL environment variable not set. Skipping heartbeat."
        )
        return

    try:
        response = requests.get(heartbeat_url, timeout=10)

        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to send heartbeat to {heartbeat_url}: {e}")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_heartbeat,
        "interval",
        minutes=5,
        id="send_heartbeat_001",
        replace_existing=True,
    )
    scheduler.start()
