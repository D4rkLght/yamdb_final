import logging
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category

logger = logging.getLogger(__name__)

MAIN_FILE_NAME = 'category.csv'

MAIN_DATA = DictReader(
    open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))
MAIN_DATA_LEN = len(list(MAIN_DATA))
MAIN_DATA = DictReader(
    open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))

ALREADY_LOADED_ERROR_MESSAGE = (
    f'Чтобы загрузить данные из {MAIN_FILE_NAME} в базу данных,\n'
    f'ее необходимо полностью очистить любым из способов:\n'
    f'1. Использовать команду: python manage.py flush\n'
    f'2.1. Удалить файл db.sqlite3.\n'
    f'2.2. Выполнить миграцию.'
)


def data_error(file_name, row, error):
    raise Exception(
        f'Ошибка загрузки данных.\n'
        f'Файл: {file_name}\n'
        f'Строка: {row}\n'
        f'Ошибка: {error}'
    )


def table_length(pk):
    if Category.objects.get(slug=pk):
        table_len = len(Category.objects.all())
        logger.info(f'Запись сохранена: {table_len} / {MAIN_DATA_LEN}')
        return table_len
    return '?'


class Command(BaseCommand):
    help = f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.'

    def handle(self, *args, **options):
        logger.info('')
        if Category.objects.exists():
            logger.info('Произведения уже есть в базе данных.')
            logger.info('')
            logger.info(ALREADY_LOADED_ERROR_MESSAGE)
            return

        logger.info(f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.')

        for row in MAIN_DATA:
            try:
                name = row['name']
                slug = row['slug']

                table_record = Category(
                    name=name,
                    slug=slug
                )
                table_record.save()

                table_len = table_length(slug)

            except Exception as error:
                data_error(MAIN_FILE_NAME, row, error)

        if table_len == MAIN_DATA_LEN:
            logger.info('Загрузка данных успешно завершена.')
        else:
            logger.info('Что-то пошло не так - данные не импортировались.')
