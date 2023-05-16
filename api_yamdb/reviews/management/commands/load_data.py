import csv

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from reviews.models import (
    Category,
    Comment,
    Genre,
    Genre_title,
    Review,
    Title,
    User,
)

DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Genre_title: "genre_title.csv",
    Comment: "comments.csv",
    Review: "review.csv",
}


class Command(BaseCommand):
    help = "Load data from csv files"

    def handle(self, *args, **kwargs):
        try:
            for model, base in DICT.items():
                with open(
                    f"{settings.BASE_DIR}/static/data/{base}",
                    "r",
                    encoding="utf-8",
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    objs = []
                    for row in reader:
                        for field in ('category', 'author'):
                            if field in row:
                                row[f'{field}_id'] = row[field]
                                del row[field]
                        objs.append(model(**row))
                    model.objects.bulk_create(objs)

        except Exception as error:
            CommandError(error)

        self.stdout.write(self.style.SUCCESS("Successfully load data"))
