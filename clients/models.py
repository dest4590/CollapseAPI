from django.db import models
from django.utils.safestring import mark_safe


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

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.name + ".jar"
        super().save(*args, **kwargs)

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
