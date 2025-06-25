import hashlib
import io
import os

import requests
from django.core.files.base import ContentFile
from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image


def client_screenshot_path(instance, filename):
    """Generate path for client screenshots"""
    return f"client_screenshots/{instance.client.id}/{filename}"


class ClientScreenshot(models.Model):
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="screenshots",
        help_text="The client this screenshot belongs to.",
    )
    image = models.ImageField(
        upload_to=client_screenshot_path,
        help_text="Client screenshot (will be optimized to WebP format).",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of the screenshot (lower numbers appear first).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Client Screenshot"
        verbose_name_plural = "Client Screenshots"

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, "file"):
            self._optimize_screenshot()
        super().save(*args, **kwargs)

    def _optimize_screenshot(self):
        """Optimize screenshot to WebP format"""
        try:
            image = Image.open(self.image.file)

            if image.mode in ("RGBA", "LA", "P"):
                image = image.convert("RGB")

            max_size = (1920, 1080)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = io.BytesIO()
            image.save(output, format="WebP", quality=85, optimize=True)
            output.seek(0)

            filename = f"{self.client.name}_screenshot_{self.id}.webp"
            self.image.save(filename, ContentFile(output.getvalue()), save=False)
        except Exception as e:
            print(f"Error optimizing screenshot for {self.client.name}: {e}")


class Client(models.Model):
    name = models.CharField(
        max_length=100, unique=True, help_text="Name of the client."
    )
    version = models.CharField(
        max_length=50,
        default="1.16.5",
        help_text="Version of the client (e.g. 1.16.5, 1.12.2).",
    )
    filename = models.CharField(
        max_length=100,
        blank=True,
        help_text=mark_safe(
            "Filename with the client (on CDN). </br><b>Defaults to the client name + .jar if left blank.</b>"
        ),
    )
    md5_hash = models.CharField(
        max_length=32,
        blank=True,
        help_text="MD5 hash of the client file (auto-calculated from CDN, you can also set it manually).",
    )

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.name + ".jar"

        if self.filename and not self.md5_hash:
            self._calculate_md5_from_cdn()

        super().save(*args, **kwargs)

    def _calculate_md5_from_cdn(self):
        """Calculate MD5 hash from CDN file"""
        if os.path.exists("/app/collapse"):
            file_path = os.path.join("/app/collapse", self.filename)
            if os.path.isfile(file_path):
                md5_hash = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        md5_hash.update(chunk)
                self.md5_hash = md5_hash.hexdigest()
            else:
                print(f"File {file_path} does not exist, skipping MD5 calculation.")
        else:
            try:
                cdn_url = f"https://cdn.collapseloader.org/{self.filename}"
                response = requests.get(cdn_url, timeout=30, stream=True)
                if response.status_code == 200:
                    md5_hash = hashlib.md5()
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            md5_hash.update(chunk)
                    self.md5_hash = md5_hash.hexdigest()
            except Exception as e:
                print(f"Error calculating MD5 for {self.name}: {e}")

    def get_screenshot_urls(self):
        """Get URLs for all client screenshots"""
        return [screenshot.image.url for screenshot in self.screenshots.all()]

    def get_launches(self):
        """Get the total number of launches for this client"""
        try:
            from client_statistics.models import ClientLaunchStats

            stats = ClientLaunchStats.objects.using("statistics").get(client_id=self.id)
            return stats.launches
        except ClientLaunchStats.DoesNotExist:
            return 0

    def get_downloads(self):
        """Get the total number of downloads for this client"""
        try:
            from client_statistics.models import ClientDownloadStats

            stats = ClientDownloadStats.objects.using("statistics").get(
                client_id=self.id
            )
            return stats.downloads
        except ClientDownloadStats.DoesNotExist:
            return 0

    main_class = models.CharField(
        max_length=300,
        default="net.minecraft.client.main.Main",
        help_text="Main class for the client.",
    )
    insecure = models.BooleanField(
        default=False,
        help_text="Whether the client is insecure (e.g., contains code obfuscation).",
    )
    show = models.BooleanField(
        default=True, help_text="Whether to show this client in listings."
    )
    working = models.BooleanField(
        default=True, help_text="Indicates if the client is currently working."
    )
    source_link = models.URLField(
        max_length=200,
        blank=True,
        help_text="URL where the client can be found.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the client was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the client was last updated."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} ({self.version})"


class ChangelogEntry(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="changelog_entries",
        help_text="The client this changelog entry belongs to.",
    )
    version = models.CharField(
        max_length=50,
        help_text="Version this changelog entry is for.",
    )
    content = models.TextField(
        help_text="Changelog content describing what's new in this version."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this changelog entry was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this changelog entry was last updated.",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Changelog Entry"
        verbose_name_plural = "Changelog Entries"
        unique_together = ["client", "version"]

    def __str__(self):
        return f"{self.client.name} - {self.version}"


class News(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ru", "Russian"),
    ]

    title = models.CharField(max_length=200, help_text="Title of the news article.")
    content = models.TextField(help_text="Content of the news article (HTML format).")
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
        help_text="Language of the news article.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the news article was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the news article was last updated."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
