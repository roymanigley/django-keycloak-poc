
from rest_framework import viewsets
from apps.core.models import Dummy
from apps.core.serializers import DummySerializer
from rest_framework.permissions import DjangoModelPermissions


class DummyViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer
    permission_classes = [DjangoModelPermissions]
