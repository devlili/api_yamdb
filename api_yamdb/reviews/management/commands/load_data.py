import csv

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User

DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Title.genre.through: "genre_title.csv",
    Comment: "comments.csv",
}


class Command(BaseCommand):
    help = "Load data from csv files"

    def handle(self, *args, **kwargs):
        try:
            for model, base in DICT.items():
                self.stdout.write(
                    self.style.NOTICE(f"Importing data from file: {base}")
                )
                with open(
                    f"{settings.BASE_DIR}/static/data/{base}",
                    "r",
                    encoding="utf-8",
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        for field in ("category", "author"):
                            if field in row:
                                row[f"{field}_id"] = row.pop(field)
                        model.objects.create(**row)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Data from file {base} successfully imported into"
                            f" table {model.__name__}."
                        )
                    )

        except Exception as error:
            CommandError(str(error))
