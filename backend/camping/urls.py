from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('camping-plots', CampingPlotViewSet, basename='camping-plot')
router.register('camping-sections', CampingSectionViewSet, basename='camping-section')
router.register('cars', CarViewSet, basename='car')
router.register('opinions', OpinionViewSet, basename='opinion')
router.register('payments', PaymentViewSet, basename='payment')
router.register('reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
