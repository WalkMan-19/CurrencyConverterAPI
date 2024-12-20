from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Currency, ExchangeRate
from .serializers import ConverterSerializer


class ConverterView(generics.CreateAPIView):
    serializer_class = ConverterSerializer
    permission_classes = (IsAuthenticated,)
    template_name = 'converter/converter.html'

    def get(self, request):
        latest_exchange_rate = ExchangeRate.objects.order_by('-last_update').first()
        last_update = latest_exchange_rate.last_update if latest_exchange_rate else None

        return render(
            request,
            template_name=self.template_name,
            context={
                'currencies': Currency.objects.all(),
                'last_update': last_update,
            }
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data['amount']
            base_currency_code = serializer.validated_data['base_currency']
            target_currency_code = serializer.validated_data['target_currency']

            base_currency = Currency.objects.get(code=base_currency_code)
            exchange_rate = ExchangeRate.objects.filter(
                base_currency=base_currency,
                target_currency__code=target_currency_code
            ).latest('last_update')

            converted_amount = amount * float(exchange_rate.rate)

            return render(request, template_name=self.template_name, context={
                'result': converted_amount,
                'currencies': Currency.objects.all(),
                'error_message': serializer.errors,
                'amount': amount,
                'base_currency_code': base_currency_code,
                'target_currency_code': target_currency_code,
                'last_update': exchange_rate.last_update
            })