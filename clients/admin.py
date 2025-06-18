from django.contrib import admin

from client_statistics.models import LoaderLaunchStats
from .models import Client
from unfold.admin import ModelAdmin


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = (
        "name",
        "version",
        "filename",
        "main_class",
        "insecure",
        "show",
        "working",
        "launches",
        "downloads",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "version", "filename")
    list_filter = ("insecure", "show", "working")
    ordering = ("-created_at",)

    def launches(self, obj):
        """Display the number of launches for this client"""
        return obj.get_launches()

    launches.short_description = "Launches"
    launches.admin_order_field = "id"  # Allow sorting by ID as proxy

    def downloads(self, obj):
        """Display the number of downloads for this client"""
        return obj.get_downloads()

    downloads.short_description = "Downloads"
    downloads.admin_order_field = "id"  # Allow sorting by ID as proxy


@admin.register(LoaderLaunchStats)
class LoaderLaunchStatsAdmin(ModelAdmin):
    list_display = (
        "launches",
        "last_launched_at",
    )
    search_fields = ("launches",)
