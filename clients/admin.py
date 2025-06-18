from django.contrib import admin
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
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "version", "filename")
    list_filter = ("insecure", "show", "working")
    ordering = ("-created_at",)
