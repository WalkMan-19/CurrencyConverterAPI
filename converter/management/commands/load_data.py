import os
import logging
from json import JSONDecodeError
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Загрузка данных из фикстур"
    datasets_dir = os.path.join('converter', 'datasets', 'json')
    loaddata_command = "loaddata"
    filenames = [
        "fixtures_currency",
        # "fixtures_exr",
    ]

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Началась загрузка фикстур.")

    def handle(self, *args, **kwargs):
        try:
            for file in self.filenames:
                call_command(
                    self.loaddata_command, os.path.join(self.datasets_dir, f"{file}.json")
                )
            self.logger.info('Данные успешно загружены.')
        except FileNotFoundError as e:
            logging.error(f"Файл с фикстурами не найден", e)
        except JSONDecodeError as e:
            logging.error("Ошибка декодирования json.", e)
        except Exception as e:
            logging.error("Произошла ошибка при загрузке данных.")