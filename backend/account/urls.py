from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views import UserViewSet, GroupViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]
