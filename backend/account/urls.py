from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
    path('email-verification/resend/', EmailVerificationResendView.as_view(), name='email-verification-resend'),
    path('email-verification/<str:uidb64>/<str:token>', EmailVerificationView.as_view(), name='email-verification'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
