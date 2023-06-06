import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
<<<<<<< HEAD
    Category, Comment, Genre, Review, Title, User, GenreTitle
=======
    Category, Comment, Genre, Review, Title, User
>>>>>>> categories/genres/titles
)


ModeltoFile = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Title: 'titles.csv',
    User: 'users.csv',
<<<<<<< HEAD
    GenreTitle: 'genre_title.csv',
=======
>>>>>>> categories/genres/titles
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in ModeltoFile.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
