import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category, Comment, Genre, Review, Title, CustomUser, GenreTitle
)


ModeltoFile = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Title: 'titles.csv',
    CustomUser: 'users.csv',
    GenreTitle: 'genre_title.csv',
}

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in ModeltoFile.items():
            with open(
                f'{settings.BASE_DIR}/static/csv_folder/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
