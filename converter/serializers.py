from rest_framework import serializers


class ConverterSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1, max_value=None, default=1)
