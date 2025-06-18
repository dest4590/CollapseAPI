from rest_framework import routers, serializers, viewsets
from django.db import connections

from clients.models import Client


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
                "SELECT COUNT(*) FROM client_launches WHERE client_id = %s", [obj.id]
            )
            return cursor.fetchone()[0]
        except:
            return 0

    def get_downloads(self, obj):
        """Get download count from statistics database"""
        try:
            cursor = connections["statistics"].cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM client_downloads WHERE client_id = %s", [obj.id]
            )
            return cursor.fetchone()[0]
        except:
            return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("insecure") is not True:
            representation.pop("insecure", None)
        return representation


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet)
