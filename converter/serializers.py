from rest_framework import serializers
from .models import Currency

class ConverterSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1, max_value=None, default=1)
    base_currency = serializers.CharField(
        max_length=3,
        error_messages={'required': 'Поле исходной валюты обязательно', 'invalid': 'Ошибка исходной валюты'},
    )
    target_currency = serializers.CharField(
        max_length=3,
        error_messages={'required': 'Поле целевой валюты обязательно', 'invalid': 'Ошибка целевой валюты '},
    )


    def validate(self, attrs):
        base_currency_code = attrs.get('base_currency')
        target_currency_code = attrs.get('target_currency')

        try:
            Currency.objects.get(code=base_currency_code)
            Currency.objects.get(code=target_currency_code)

        except Currency.DoesNotExist:
            raise serializers.ValidationError("Base or target currency does not exist.")

        return attrs
