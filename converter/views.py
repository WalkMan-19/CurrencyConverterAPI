from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Currency, ExchangeRate
from .serializers import ConverterSerializer


class ConverterView(generics.CreateAPIView):
    serializer_class = ConverterSerializer
    permission_classes = (IsAuthenticated,)
    template_name = 'converter/converter.html'

    def get(self, request):
        return render(request, template_name=self.template_name, context={'currencies': Currency.objects.all()})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        base_currency_code = request.data.get('base_currency')
        target_currency_code = request.data.get('target_currency')

        try:
            base_currency = Currency.objects.get(code=base_currency_code)
            exchange_rate = ExchangeRate.objects.get(base_currency=base_currency,
                                                     target_currency__code=target_currency_code)
        except Currency.DoesNotExist:
            return Response({"error": "Base currency does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except ExchangeRate.DoesNotExist:
            return Response({"error": "Exchange rate not found."}, status=status.HTTP_404_NOT_FOUND)

        converted_amount = amount * exchange_rate.rate

        return Response({
            "base_currency": base_currency_code,
            "target_currency": target_currency_code,
            "amount": amount,
            "converted_amount": converted_amount,
            "rate": exchange_rate.rate
        }, status=status.HTTP_200_OK)

