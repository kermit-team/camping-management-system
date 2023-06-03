from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from camping.models import Payment


class PaymentPossibleMethodsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response(Payment.Method.choices)
