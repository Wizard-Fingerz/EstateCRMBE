from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'users'

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'marketers', MarketerViewSet, basename='marketer')

urlpatterns = [
    path('api-auth-token', obtain_auth_token, name='api_token'),
    path('create_marketer/', CreateMarketerView.as_view(), name='create_marketer'),
    path('create_accountant/', CreateAccountantView.as_view(),
         name='create_accountant'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('check-password-change/', PasswordChangeCheckView.as_view(), name='check_password_change'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('marketer/count/', MarketerCountView.as_view(), name='property_count'),

]

urlpatterns += router.urls
