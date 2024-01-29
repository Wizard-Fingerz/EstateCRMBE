# urls.py
from django.urls import path
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'marketers', PropertyMarketerViewSet, basename='marketer')


urlpatterns = [
    path('', include(router.urls)),
    path('create_property/', CreatePropertyView.as_view(), name='create_property'),
    path('create_prospect/', CreateProspectView.as_view(), name='create_property'),
    path('property/count/', PropertyCountView.as_view(), name='property_count'),
    path('prospects/', ProspectListView.as_view(), name='prospect-list'),

    # Add other URLs as needed
]

urlpatterns += router.urls
