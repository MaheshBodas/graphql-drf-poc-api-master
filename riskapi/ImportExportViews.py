import rest_framework
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from riskapi.resources import RiskTypeResource, RiskTypeFieldResource
from django.http import HttpResponse


class ImportExportRiskTypeView(APIView):
    def get(self, request):
        if request.method == 'GET':
            risktype_resource = RiskTypeResource()
            dataset = risktype_resource.export()
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="persons.json"'
            return response


class ImportExportRiskTypeFieldView(APIView):
    # @classmethod
    # def as_view(cls, *args, **kwargs):
    #     view = super(ImportExportView, cls).as_view(*args, **kwargs)        
    #     view = permission_classes((permissions.IsAdminUser,))(view)
    #     view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
    #     view = api_view(['GET', 'POST'])(view)
    # permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        if request.method == 'GET':
            risktypefield_resource = RiskTypeFieldResource()
            dataset = risktypefield_resource.export()
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="persons.json"'
            return response