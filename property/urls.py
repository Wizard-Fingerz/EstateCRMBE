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
    path('prospect/count/', ProspectCountView.as_view(), name='prospect_count'),
    path('customer/count/', CustomerCountView.as_view(), name='prospect_count'),
    path('prospects/', ProspectListView.as_view(), name='prospect-list'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('delete-properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('prospects/<int:pk>/allocate/', ProspectAllocationView.as_view(), name='prospect-allocate'),
    path('prospects/<int:prospect_id>/send-email/', SendEmailView.as_view(), name='send-email'),
    path('prospects/send-bulk-email/', BulkEmailView.as_view(), name='send-bulk-email'),
    path('convert-prospect-to-customer/', ConvertProspectToCustomer.as_view(), name='convert_prospect_to_customer'),
    path('follow-up/<int:prospect_id>/', FollowUpReportCreateAPIView.as_view(), name='followup-report-create'),
    path('follow-ups/', MarketerFollowUpReportListAPIView.as_view(), name='followup-reports'),


    # Add other URLs as needed
]

urlpatterns += router.urls
