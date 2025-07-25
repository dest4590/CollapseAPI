from django.db import connections
from rest_framework import routers, serializers, viewsets

from clients.models import Client, News, ChangelogEntry


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    launches = serializers.SerializerMethodField()
    downloads = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "version",
            "filename",
            "md5_hash",
            "size",
            "main_class",
            "show",
            "working",
            "insecure",
            "launches",
            "downloads",
            "created_at",
        ]

    def get_launches(self, obj):
        """Get launch count from statistics database"""
        try:
            cursor = connections["statistics"].cursor()
            cursor.execute(
                "SELECT launches FROM client_launches WHERE client_id = %s", [obj.id]
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except:
            return 0

    def get_downloads(self, obj):
        """Get download count from statistics database"""
        try:
            cursor = connections["statistics"].cursor()
            cursor.execute(
                "SELECT downloads FROM client_downloads WHERE client_id = %s", [obj.id]
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except:
            return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("insecure") is not True:
            representation.pop("insecure", None)
        return representation


class ChangelogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangelogEntry
        fields = ["version", "content", "created_at"]


class ClientDetailedSerializer(serializers.HyperlinkedModelSerializer):
    changelog_entries = ChangelogEntrySerializer(many=True, read_only=True)
    screenshot_urls = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "source_link",
            "screenshot_urls",
            "changelog_entries",
            "created_at",
        ]

    def get_screenshot_urls(self, obj):
        request = self.context.get("request")
        screenshots = []
        for screenshot in obj.screenshots.all():
            if request:
                screenshots.append(request.build_absolute_uri(screenshot.image.url))
            else:
                screenshots.append(screenshot.image.url)
        return screenshots


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "content", "language", "created_at", "updated_at"]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        language = self.request.query_params.get("language", None)
        if language is not None:
            queryset = queryset.filter(language=language)
        return queryset


router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"news", NewsViewSet)
