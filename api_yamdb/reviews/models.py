from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstracts import PubInfo
from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        primary_key=True,
        max_length=50,
        verbose_name='Ссылка'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        primary_key=True,
        max_length=50,
        verbose_name='Ссылка'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение'
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        db_index=True,
        validators=[validate_year]
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        through='TitleGenre',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return (f'{self.title_id}: {self.genre_id}')


class Review(PubInfo):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Отзыв')
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(PubInfo):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
