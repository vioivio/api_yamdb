from django.db import models

from user.models import User
from .constants import (
    CATEGORY_NAME_LENGTH,
    CATEGORY_SLUG_LENGTH,
    DESCRIPTION_LENGTH,
    NAME_LENGTH,
    TEXT_LENGTH,
)
from .validators import (
    validate_date,
    validate_score
)


class Category(models.Model):
    """Модель категории."""

    name = models.CharField('Название категории',
                            max_length=CATEGORY_NAME_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=CATEGORY_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        'Жанр',
        max_length=NAME_LENGTH
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        'Название произведения',
        max_length=NAME_LENGTH,
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(validate_date,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание произведения',
        max_length=DESCRIPTION_LENGTH,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Оценка произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.CharField(
        max_length=TEXT_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[validate_score],
        error_messages={'validators': 'Оценка должна быть в диапазоне 1-10'}
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='review',
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField(
        'Тело комментария',
        max_length=TEXT_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text
