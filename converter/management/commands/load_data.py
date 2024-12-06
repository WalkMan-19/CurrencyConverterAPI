import json
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Загрузка данных из фикстур'

    def handle(self, *args, **kwargs):
        app_label = 'converter'
        datasets_dir = 'converter/datasets/json/'

        with open(f'{datasets_dir}fixtures_currency.json', 'r', encoding='utf-8') as f:
            currencies_data = json.load(f)
            for currency in currencies_data:
                Currency = apps.get_model(app_label, 'Currency')
                Currency.objects.create(**currency['fields'])

        with open(f'{datasets_dir}fixtures_exr.json', 'r', encoding='utf-8') as f:
            exchange_rates_data = json.load(f)
            for rate in exchange_rates_data:
                ExchangeRate = apps.get_model(app_label, 'ExchangeRate')
                ExchangeRate.objects.create(**rate['fields'])

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))
