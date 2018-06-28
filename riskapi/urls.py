from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from riskapi import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'risktypekeys', views.RiskTypeKeyViewSet,'risktypekeys')
router.register(r'riskkeys', views.RiskKeyViewSet,'riskkeys')
router.register(r'risktypes', views.RiskTypeViewSet)
router.register(r'risks', views.RiskViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))    
]