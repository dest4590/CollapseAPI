from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from client_statistics.models import LoaderLaunchStats

from .models import Client, ChangelogEntry, News, ClientScreenshot


class ChangelogEntryInline(TabularInline):
    model = ChangelogEntry
    extra = 1
    fields = ["version", "content", "created_at"]
    readonly_fields = ["created_at"]


class ClientScreenshotInline(TabularInline):
    model = ClientScreenshot
    extra = 1
    fields = ["image", "order"]


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = [
        "name",
        "version",
        "working",
        "show",
        "created_at",
    ]
    list_filter = ["working", "show", "insecure", "version"]
    search_fields = ["name", "version"]
    inlines = [ChangelogEntryInline, ClientScreenshotInline]
    fieldsets = (
        ("Basic Information", {"fields": ("name", "version", "filename", "md5_hash")}),
        (
            "Configuration",
            {"fields": ("main_class", "insecure", "show", "working", "source_link")},
        ),
    )


@admin.register(ChangelogEntry)
class ChangelogEntryAdmin(admin.ModelAdmin):
    list_display = ["client", "version", "created_at"]
    list_filter = ["client", "created_at"]
    search_fields = ["client__name", "version", "content"]


@admin.register(LoaderLaunchStats)
class LoaderLaunchStatsAdmin(ModelAdmin):
    list_display = (
        "launches",
        "last_launched_at",
    )
    search_fields = ("launches",)


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = (
        "title",
        "language",
        "created_at",
        "updated_at",
    )
    search_fields = ("title",)
    list_filter = ("language",)


@admin.register(ClientScreenshot)
class ClientScreenshotAdmin(ModelAdmin):
    list_display = ["client", "order", "created_at"]
    list_filter = ["client", "created_at"]
    search_fields = ["client__name"]
