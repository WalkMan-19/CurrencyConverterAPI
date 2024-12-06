import json
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Загрузка данных из фикстур'

    def handle(self, *args, **kwargs):
        app_label = 'converter'
        datasets_dir = 'converter/datasets/json/'

        Currency = apps.get_model(app_label, 'Currency')
        ExchangeRate = apps.get_model(app_label, 'ExchangeRate')

        ExchangeRate.objects.all().delete()
        currencies = {}

        with open(f'{datasets_dir}fixtures_currency.json', 'r', encoding='utf-8') as f:
            currencies_data = json.load(f)
            for currency in currencies_data:
                currency_instance, created = Currency.objects.get_or_create(
                    code=currency['fields']['code'],
                    defaults={'name': currency['fields']['name']}
                )
                currencies[currency['pk']] = currency_instance

        with open(f'{datasets_dir}fixtures_exr.json', 'r', encoding='utf-8') as f:
            exchange_rates_data = json.load(f)
            for rate in exchange_rates_data:
                base_currency = currencies[rate['fields']['base_currency']]
                target_currency = currencies[rate['fields']['target_currency']]

                ExchangeRate.objects.create(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    rate=rate['fields']['rate']
                )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))
