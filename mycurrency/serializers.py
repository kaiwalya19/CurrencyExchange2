from rest_framework import serializers
from .models import Currency, CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class ExchangeRateSerializer(serializers.ModelSerializer):
    # Include the `code` field from related `Currency` objects
    source_currency = serializers.CharField(source='source_currency.code', read_only=True)
    exchanged_currency = serializers.CharField(source='exchanged_currency.code', read_only=True)

    class Meta:
        model = CurrencyExchangeRate
        fields = ['id', 'valuation_date', 'rate_value', 'source_currency', 'exchanged_currency']

    # Optional: Custom validation for rate_value
    def validate_rate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Exchange rate must be greater than zero.")
        return value
