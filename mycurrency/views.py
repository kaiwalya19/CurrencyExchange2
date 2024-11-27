from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Currency, CurrencyExchangeRate
from django.core.cache import cache
from .serializers import CurrencySerializer, ExchangeRateSerializer

# Currency List & Create View
class CurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# Currency Detail View
class CurrencyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# Retrieve Exchange Rates
class ExchangeRateAPIView(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if not source_currency or not date_from or not date_to:
            return Response(
                {"error": "source_currency, date_from, and date_to are required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=[date_from, date_to]
        )
        serializer = ExchangeRateSerializer(rates, many=True)
        return Response(serializer.data)


# Convert Currency
class CurrencyConvertView(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        target_currency = request.query_params.get('target_currency')
        amount = float(request.query_params.get('amount', 0))

        if not source_currency or not target_currency or amount <= 0:
            return Response(
                {"error": "Invalid parameters. Ensure source_currency, target_currency, and a positive amount are provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cache_key = f"conversion-{source_currency}-{target_currency}-{amount}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            exchanged_currency__code=target_currency
        ).order_by('-valuation_date').first()

        if not rate:
            return Response({"error": "Exchange rate not found."}, status=404)

        converted_amount = amount * float(rate.rate_value)
        result = {"converted_amount": converted_amount}
        cache.set(cache_key, result, timeout=3600)  # Cache the result for 1 hour
        return Response(result)
