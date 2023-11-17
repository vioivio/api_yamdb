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

filepath = os.path.join(*settings.STATICFILES_DIRS, 'data/')


path_csv = {
    filepath + 'category.csv': Category,
    filepath + 'genre.csv': Genre,
    filepath + 'titles.csv': Title,
    filepath + 'users.csv': User,
    filepath + 'review.csv': Review,
    filepath + 'comments.csv': Comment
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for path, model in path_csv.items():
            try:
                with open(
                    path,
                    'r', encoding='utf-8'
                ) as csv_file:
                    data_list = []
                    data = csv.DictReader(csv_file)
                    for row in data:
                        data_list.append(model(**row))
                    model.objects.bulk_create(data_list)
            except Exception as err:
                self.stdout.write(self.style.ERROR(f'{err}'))
        self.stdout.write(self.style.SUCCESS('Upload Complete!'))
