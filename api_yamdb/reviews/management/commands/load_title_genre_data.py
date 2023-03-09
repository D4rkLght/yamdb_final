# import logging

# from csv import DictReader
# from django.core.management import BaseCommand

# from reviews.models import Genre, Title, TitleGenre


# logger = logging.getLogger(__name__)

# MAIN_FILE_NAME = 'genre_title.csv'
# RELATED_FILE_NAME_T = 'titles.csv'
# RELATED_FILE_NAME_G = 'genre.csv'

# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))
# MAIN_DATA_LEN = len(list(MAIN_DATA))
# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))

# RELATED_DATA_T = DictReader(
#     open(f'./static/data/{RELATED_FILE_NAME_T}', encoding='utf-8'))
# RELATED_DATA_G = DictReader(
#     open(f'./static/data/{RELATED_FILE_NAME_G}', encoding='utf-8'))

# ALREADY_LOADED_ERROR_MESSAGE = (
#     f'Чтобы загрузить данные из {MAIN_FILE_NAME} в базу данных,\n'
#     f'ее необходимо полностью очистить любым из способов:\n'
#     f'1. Использовать команду: python manage.py flush\n'
#     f'2.1. Удалить файл db.sqlite3.\n'
#     f'2.2. Выполнить миграцию.'
# )


# def data_error(file_name, row, error):
#     raise Exception(
#         f'Ошибка загрузки данных.\n'
#         f'Файл: {file_name}\n'
#         f'Строка: {row}\n'
#         f'Ошибка: {error}'
#     )


# def table_length(title, genre):
#     if TitleGenre.objects.get(title=title, genre=genre):
#         table_len = len(TitleGenre.objects.all())
#         logger.info(f'Запись сохранена: {table_len} / {MAIN_DATA_LEN}')
#         return table_len
#     return '?'


# class Command(BaseCommand):
#     help = f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.'

#     def handle(self, *args, **options):
#         logger.info('')
#         if TitleGenre.objects.exists():
#             logger.info('Произведения уже есть в базе данных.')
#             logger.info('')
#             logger.info(ALREADY_LOADED_ERROR_MESSAGE)
#             return

#         logger.info(f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.')
#         logger.info('')
#         logger.info(
#             f'Подключение смежных данных из файла {RELATED_FILE_NAME_T}')

#         relates_t = {}

#         for row in RELATED_DATA_T:
#             try:
#                 pk = row['id']
#                 relates_t[pk] = pk
#             except Exception as error:
#                 data_error(RELATED_FILE_NAME_T, row, error)

#         logger.info(f'Смежные данные подключены: {relates_t}')
#         logger.info('')
#         logger.info(
#             f'Подключение смежных данных из файла {RELATED_FILE_NAME_G}')

#         relates_g = {}

#         for row in RELATED_DATA_G:
#             try:
#                 pk = row['id']
#                 slug = row['slug']
#                 relates_g[pk] = slug
#             except Exception as error:
#                 data_error(RELATED_FILE_NAME_G, row, error)

#         logger.info(f'Смежные данные подключены: {relates_g}')
#         logger.info('')
#         logger.info(f'Загрузка данных из файла {MAIN_FILE_NAME}')

#         for row in MAIN_DATA:
#             try:
#                 related_t_pk = row['title_id']
#                 pk_t = relates_t[related_t_pk]
#                 title = Title.objects.get(pk=pk_t)

#                 related_g_pk = row['genre_id']
#                 slug_g = relates_g[related_g_pk]
#                 genre = Genre.objects.get(slug=slug_g)

#                 table_record = TitleGenre(
#                     title=title,
#                     genre=genre
#                 )
#                 table_record.save()

#                 table_len = table_length(title, genre)

#             except Exception as error:
#                 data_error(MAIN_FILE_NAME, row, error)

#         if table_len == MAIN_DATA_LEN:
#             logger.info('Загрузка данных успешно завершена.')
#         else:
#             logger.info('Что-то пошло не так - данные не импортировались.')
