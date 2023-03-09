# import logging

# from csv import DictReader
# from django.core.management import BaseCommand

# from reviews.models import Review, Title, User


# logger = logging.getLogger(__name__)

# MAIN_FILE_NAME = 'review.csv'
# RELATED_FILE_NAME_T = 'titles.csv'
# RELATED_FILE_NAME_U = 'users.csv'

# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))
# MAIN_DATA_LEN = len(list(MAIN_DATA))
# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))

# RELATED_DATA_T = DictReader(
#     open(f'./static/data/{RELATED_FILE_NAME_T}', encoding='utf-8'))
# RELATED_DATA_U = DictReader(
#     open(f'./static/data/{RELATED_FILE_NAME_U}', encoding='utf-8'))

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


# def table_length(title, author):
#     if Review.objects.get(title=title, author=author):
#         table_len = len(Review.objects.all())
#         logger.info(f'Запись сохранена: {table_len} / {MAIN_DATA_LEN}')
#         return table_len
#     return '?'


# class Command(BaseCommand):
#     help = f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.'

#     def handle(self, *args, **options):
#         logger.info('')
#         if Review.objects.exists():
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
#             f'Подключение смежных данных из файла {RELATED_FILE_NAME_U}')

#         relates_u = {}

#         for row in RELATED_DATA_U:
#             try:
#                 pk = row['id']
#                 relates_u[pk] = pk
#             except Exception as error:
#                 data_error(RELATED_FILE_NAME_U, row, error)

#         logger.info(f'Смежные данные подключены: {relates_u}')
#         logger.info('')
#         logger.info(f'Загрузка данных из файла {MAIN_FILE_NAME}')

#         for row in MAIN_DATA:
#             try:
#                 text = row['text']
#                 score = row['score']
#                 pub_date = row['pub_date']

#                 related_t_pk = row['title_id']
#                 pk_t = relates_t[related_t_pk]
#                 title = Title.objects.get(pk=pk_t)

#                 related_u_pk = row['author']
#                 pk_u = relates_u[related_u_pk]
#                 author = User.objects.get(pk=pk_u)

#                 table_record = Review(
#                     text=text,
#                     score=score,
#                     pub_date=pub_date,
#                     title=title,
#                     author=author
#                 )
#                 table_record.save()

#                 table_len = table_length(title, author)

#             except Exception as error:
#                 data_error(MAIN_FILE_NAME, row, error)

#         if table_len == MAIN_DATA_LEN:
#             logger.info('Загрузка данных успешно завершена.')
#         else:
#             logger.info('Что-то пошло не так - данные не импортировались.')
