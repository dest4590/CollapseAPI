from django.db import models
from django.db import transaction
from django_unixdatetimefield import UnixDateTimeField


class ClientLaunchStats(models.Model):
    client_id = models.IntegerField(
        unique=True, help_text="ID of the client", db_index=True
    )
    launches = models.PositiveIntegerField(
        default=0, help_text="Total number of client launches"
    )
    last_launched_at = UnixDateTimeField(
        auto_now=True, help_text="When the client was last launched", db_index=True
    )

    class Meta:
        db_table = "client_launches"
        ordering = ["-last_launched_at"]
        verbose_name = "Client Launch Statistics"
        verbose_name_plural = "Client Launch Statistics"

    def increment_launches(self):
        """Atomically increment the launches counter"""
        with transaction.atomic():
            self.launches = models.F("launches") + 1
            self.save(update_fields=["launches", "last_launched_at"])
            self.refresh_from_db()
        return self.launches

    @classmethod
    def record_launch(cls, client_id):
        """Record a launch for the given client_id"""
        obj, created = cls.objects.using("statistics").get_or_create(
            client_id=client_id, defaults={"launches": 0}
        )
        return obj.increment_launches()


class ClientDownloadStats(models.Model):
    client_id = models.IntegerField(
        unique=True, help_text="ID of the client", db_index=True
    )
    downloads = models.PositiveIntegerField(
        default=0, help_text="Total number of client downloads"
    )
    last_downloaded_at = models.DateTimeField(
        auto_now=True, help_text="When the client was last downloaded", db_index=True
    )

    class Meta:
        db_table = "client_downloads"
        ordering = ["-last_downloaded_at"]
        verbose_name = "Client Download Statistics"
        verbose_name_plural = "Client Download Statistics"

    def increment_downloads(self):
        """Atomically increment the downloads counter"""
        with transaction.atomic():
            self.downloads = models.F("downloads") + 1
            self.save(update_fields=["downloads", "last_downloaded_at"])
            self.refresh_from_db()
        return self.downloads

    @classmethod
    def record_download(cls, client_id):
        """Record a download for the given client_id"""
        obj, created = cls.objects.using("statistics").get_or_create(
            client_id=client_id, defaults={"downloads": 0}
        )
        return obj.increment_downloads()


class LoaderLaunchStats(models.Model):
    launches = models.PositiveIntegerField(
        default=0, help_text="Total number of loader launches"
    )
    last_launched_at = UnixDateTimeField(
        auto_now=True, help_text="When the loader was last launched", db_index=True
    )

    class Meta:
        db_table = "loader_launches"
        ordering = ["-last_launched_at"]
        verbose_name = "Loader Launch Statistics"
        verbose_name_plural = "Loader Launch Statistics"

    def increment_launches(self):
        """Atomically increment the launches counter"""
        with transaction.atomic():
            self.launches = models.F("launches") + 1
            self.save(update_fields=["launches", "last_launched_at"])
            self.refresh_from_db()
        return self.launches

    @classmethod
    def record_launch(cls):
        """Record a launch for the given loader_id"""
        obj, created = cls.objects.using("statistics").get_or_create(
            defaults={"launches": 0}
        )
        return obj.increment_launches()
