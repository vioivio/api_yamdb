import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.conf.global_settings import STATICFILES_DIRS

from user.models import User
from reviews.models import (Category,
                            Genre,
                            Title,
                            Review,
                            Comment,
                            )

URL = STATICFILES_DIRS + '/data/'


def category(row):
    Category.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2]
    )


def title(row):
    Title.objects.create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genre(row):
    Genre.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def review(row):
    Review.objects.create(
        id=row[0],
        title=row[1],
        text=row[2],
        author=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comment(row):
    Comment.objects.create(
        id=row[0],
        review=row[1],
        text=row[2],
        author=row[3],
        pub_date=row[4]
    )


def user(row):
    User.objects.create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6]
    )


csv_dict = {
    URL+'category.csv': category,
    URL+'comments.csv': comment,
    URL+'genre.csv': genre,
    URL+'review.csv': review,
    URL+'users.csv': user,
    URL+'titles.csv': title
    }


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        for url, model_create in csv_dict.items():
            with open(url, 'r', encoding='utf-8') as file:
                csv_data = csv.reader(file)
                next(csv_data)
                for row in csv_data:
                    model_create(row)
