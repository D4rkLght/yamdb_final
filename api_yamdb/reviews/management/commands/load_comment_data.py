# import logging

# from csv import DictReader
# from django.core.management import BaseCommand

# from reviews.models import Comment, Review, User


# logger = logging.getLogger(__name__)

# MAIN_FILE_NAME = 'comments.csv'
# RELATED_FILE_NAME_R = 'review.csv'
# RELATED_FILE_NAME_U = 'users.csv'

# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))
# MAIN_DATA_LEN = len(list(MAIN_DATA))
# MAIN_DATA = DictReader(
#     open(f'./static/data/{MAIN_FILE_NAME}', encoding='utf-8'))

# RELATED_DATA_R = DictReader(
#     open(f'./static/data/{RELATED_FILE_NAME_R}', encoding='utf-8'))
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


# def table_length(pk):
#     if Comment.objects.get(pk=pk):
#         table_len = len(Comment.objects.all())
#         logger.info(f'Запись сохранена: {table_len} / {MAIN_DATA_LEN}')
#         return table_len
#     return '?'


# class Command(BaseCommand):
#     help = f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.'

#     def handle(self, *args, **options):
#         logger.info('')
#         if Comment.objects.exists():
#             logger.info('Произведения уже есть в базе данных.')
#             logger.info('')
#             logger.info(ALREADY_LOADED_ERROR_MESSAGE)
#             return

#         logger.info(f'Загрузка данных из {MAIN_FILE_NAME} в базу данных.')
#         logger.info('')
#         logger.info(
#             f'Подключение смежных данных из файла {RELATED_FILE_NAME_R}')

#         relates_r = {}

#         for row in RELATED_DATA_R:
#             try:
#                 pk = row['id']
#                 relates_r[pk] = pk
#             except Exception as error:
#                 data_error(RELATED_FILE_NAME_R, row, error)

#         relates_u = {}

#         for row in RELATED_DATA_U:
#             try:
#                 pk = row['id']
#                 relates_u[pk] = pk
#             except Exception as error:
#                 data_error(RELATED_FILE_NAME_R, row, error)

#         for row in MAIN_DATA:
#             try:
#                 pk = row['id']
#                 text = row['text']
#                 pub_date = row['pub_date']

#                 related_r_pk = row['review_id']
#                 pk_r = relates_r[related_r_pk]
#                 review = Review.objects.get(pk=pk_r)

#                 related_u_pk = row['author']
#                 pk_u = relates_u[related_u_pk]
#                 author = User.objects.get(pk=pk_u)

#                 table_record = Comment(
#                     text=text,
#                     pub_date=pub_date,
#                     review=review,
#                     author=author
#                 )
#                 table_record.save()

#                 table_len = table_length(pk)

#             except Exception as error:
#                 data_error(MAIN_FILE_NAME, row, error)

#         if table_len == MAIN_DATA_LEN:
#             logger.info('Загрузка данных успешно завершена.')
#         else:
#             logger.info('Что-то пошло не так - данные не импортировались.')
