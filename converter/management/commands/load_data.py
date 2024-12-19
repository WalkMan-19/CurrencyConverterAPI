import json
import os
import logging
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Загрузка данных из фикстур'

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Начало загрузки данных из фикстур')


    def handle(self, *args, **kwargs):
        app_label = 'converter'
        datasets_dir = os.path.join('converter', 'datasets', 'json')

        Currency = apps.get_model(app_label, 'Currency')
        ExchangeRate = apps.get_model(app_label, 'ExchangeRate')

        ExchangeRate.objects.all().delete()
        currencies = {}

        currency_file_path = os.path.join(datasets_dir, 'fixtures_currency.json')
        exchange_rate_file_path = os.path.join(datasets_dir, 'fixtures_exr.json')

        if not os.path.exists(currency_file_path):
            self.logger.error(f'Файл не найден: {currency_file_path}')
            raise FileNotFoundError
            # self.stdout.write(self.style.ERROR(f'Файл не найден: {currency_file_path}'))

        if not os.path.exists(exchange_rate_file_path):
            self.logger.error(f'Файл не найден: {exchange_rate_file_path}')
            raise FileNotFoundError
            # self.stdout.write(self.style.ERROR(f'Файл не найден: {exchange_rate_file_path}'))

        with open(file=currency_file_path, mode='r', encoding='utf-8') as f:
            currencies_data = json.load(f)
            for currency in currencies_data:
                currency_instance, created = Currency.objects.get_or_create(
                    code=currency['fields']['code'],
                    defaults={'name': currency['fields']['name']}
                )
                currencies[currency['pk']] = currency_instance

        with open(exchange_rate_file_path, 'r', encoding='utf-8') as f:
            exchange_rates_data = json.load(f)
            for rate in exchange_rates_data:
                base_currency = currencies[rate['fields']['base_currency']]
                target_currency = currencies[rate['fields']['target_currency']]

                ExchangeRate.objects.create(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    rate=rate['fields']['rate']
                )

        self.logger.info('Загрузка данных завершена успешно.')
        # self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))
