import requests
from celery import shared_task
from core import settings
from .models import Currency, ExchangeRate
import time


@shared_task
def fetch_exchange_rates():
    api_key = settings.EXR_API_KEY
    currencies = Currency.objects.all()
    currency_codes = [currency.code for currency in currencies]

    for base_currency in currency_codes:
        currencies_string = ', '.join([code for code in currency_codes if code != base_currency])

        params = {
            "access_key": api_key,
            "source": base_currency,
            "currencies": currencies_string
        }

        response = requests.get('https://api.exchangerate.host/live', params=params)

        if response.status_code == 200:
            data = response.json()
            if 'quotes' in data:
                rates = data['quotes']
                for target_currency_code, rate in rates.items():
                    target_currency = target_currency_code[3:]
                    if Currency.objects.filter(code=target_currency).exists():

                        ExchangeRate.objects.update_or_create(
                            base_currency=Currency.objects.get(code=base_currency),
                            target_currency=Currency.objects.get(code=target_currency),
                            defaults={'rate': rate},
                        )
                        print(f"Курс обновлен: 1 {base_currency} = {rate} {target_currency}")
            else:
                print(f"Нет данных о курсах для {base_currency}.")
        else:
            print(f"Ошибка запроса для {base_currency}: {response.status_code}")
        time.sleep(1)