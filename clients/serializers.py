from rest_framework import routers, serializers, viewsets

from clients.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "version",
            "filename",
            "main_class",
            "insecure",
            "runs",
            "downloads_count",
            "created_at",
        ]

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
