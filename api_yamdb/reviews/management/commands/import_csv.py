import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title
                            )
from user.models import User

URL = os.path.join(*settings.STATICFILES_DIRS, 'data/')


def category(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2]
    )


def title(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genre(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def review(row):
    Review.objects.get_or_create(
        id=row[0],
        title_id=row[1],
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comment(row):
    Comment.objects.get_or_create(
        id=row[0],
        review_id=row[1],
        text=row[2],
        author_id=row[3],
        pub_date=row[4]
    )


def user(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6]
    )


csv_dict = {
    URL + 'category.csv': category,
    URL + 'genre.csv': genre,
    URL + 'titles.csv': title,
    URL + 'users.csv': user,
    URL + 'review.csv': review,
    URL + 'comments.csv': comment
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for url, model_create in csv_dict.items():
            with open(url, 'r', encoding='utf-8') as file:
                csv_data = csv.reader(file)
                next(csv_data)
                for row in csv_data:
                    model_create(row)
