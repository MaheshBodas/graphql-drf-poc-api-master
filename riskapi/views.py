from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets, mixins
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from riskapi.models import *
from riskapi.serializers import *
from django_filters import rest_framework as filters

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username', 'email', 'is_staff',)
    permission_classes = (permissions.IsAuthenticated,)

class RiskTypeKeyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = risktype.objects.all()
    serializer_class = RiskTypeKeySerializer
    permission_classes = (permissions.IsAuthenticated,)    
    # http_method_names = ['get']

class RiskKeyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = risk.objects.all()
    serializer_class = RiskKeySerializer
    permission_classes = (permissions.IsAuthenticated,)    
    # http_method_names = ['get']

class RiskTypeViewSet(viewsets.ModelViewSet):
    queryset = risktype.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'risk_type_name',)
    serializer_class = RiskTypeSerializer
    permission_classes = (permissions.IsAdminUser,)
    # http_method_names = ['get', 'post']

    def pre_save(self, obj):
        obj.createdby = self.request.user

class RiskViewSet(viewsets.ModelViewSet):
    queryset = risk.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'risk_name',)
    serializer_class = RiskSerializer    
    permission_classes = (permissions.IsAuthenticated,)
    # http_method_names = ['get', 'post']

    def pre_save(self, obj):
        obj.createdby = self.request.user
