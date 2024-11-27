from celery import shared_task
from .adapters import CurrencyBeaconProvider
from .models import CurrencyExchangeRate
from datetime import datetime, timedelta

@shared_task(bind=True, max_retries=3)
def fetch_historical_rates(self, source_currency, target_currency, start_date, end_date):
    provider = CurrencyBeaconProvider()
    try:
        current_date = start_date
        while current_date <= end_date:
            rate_data = provider.get_exchange_rate_data(source_currency, target_currency, current_date)
            if rate_data:
                CurrencyExchangeRate.objects.update_or_create(
                    source_currency=source_currency,
                    exchanged_currency=target_currency,
                    valuation_date=current_date,
                    defaults={'rate_value': rate_data['rate_value']}
                )
            current_date += timedelta(days=1)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@shared_task
def test_task():
    return "Task executed successfully!"
