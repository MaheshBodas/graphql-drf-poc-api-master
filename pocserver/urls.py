"""BriteCorePOCAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from pocserver.schema import schema
from pocserver.adminschema import schema as adminschema
from riskapi.DRFGraphQLViews import DRFAdminOnlyGraphQLView, DRFAuthenticatedGraphQLView
from graphene_django.views import GraphQLView
# from riskapi.views import DRFAuthenticatedGraphQLView

API_TITLE = 'Pastebin API'
API_DESCRIPTION = 'A Web API for creating and viewing RiskTypes and RiskInstances based on that.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [    
    # url(r'^', include('riskapi.urls')),    
    # path("graphql/", GraphQLView.as_view(graphiql=True)),        
    url(r'^auth/', include('rest_auth.urls')),  
    path('admingq/graphql/', DRFAdminOnlyGraphQLView.as_view(graphiql=True, schema=adminschema)),          
	path('graphql/', DRFAuthenticatedGraphQLView.as_view(graphiql=True, schema=schema)),           
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^schema/$', schema_view),    
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]