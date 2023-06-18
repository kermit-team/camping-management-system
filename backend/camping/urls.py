from django.urls import include, path
from rest_framework.routers import DefaultRouter

from camping.views import AvailableCampingPlotsView, CampingPlotViewSet, CampingSectionViewSet, \
    CarViewSet, CarAbleToEnterCampingView, OpinionViewSet, ReservationViewSet, \
    PaymentPossibleMethodsView, PaymentPossibleStatusesView, PaymentWebhookView

router = DefaultRouter()
router.register('camping-plots', CampingPlotViewSet, basename='camping-plot')
router.register('camping-sections', CampingSectionViewSet, basename='camping-section')
router.register('cars', CarViewSet, basename='car')
router.register('opinions', OpinionViewSet, basename='opinion')
router.register('reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('payments/methods/', PaymentPossibleMethodsView.as_view(), name='payment-methods'),
    path('payments/statuses/', PaymentPossibleStatusesView.as_view(), name='payment-statuses'),
    path('payments/webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
    path('camping-plots/available/', AvailableCampingPlotsView.as_view(), name='available-camping-plots'),
    path('cars/able-to-enter-camping/', CarAbleToEnterCampingView.as_view(), name='car-able-to-enter-camping'),
    path('', include(router.urls)),
]
