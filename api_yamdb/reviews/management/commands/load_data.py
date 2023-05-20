import csv

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)

DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Comment: "comments.csv",
    Review: "review.csv",
    Title.genre.through: "genre_title.csv",
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
                    # for row in reader:
                    #     for field in ("category", "author"):
                    #         if field in row:
                    #             row[f"{field}_id"] = row.pop(field)
                    #     model_write, create = model.objects.get_or_create(
                    #         **row
                    #     )
                    #     if not create:
                    #         model_write = model.objects.update(**row)
                    #         print("Данные обновлены")
                    #     model_write.save()
                    # print(
                    #     f"Данные из файла {base} успешно импортированы"
                    #     f" в таблицу {model.__name__}."
                    # )

                    for row in reader:
                        for field in ("category", "author"):
                            if field in row:
                                row[f"{field}_id"] = row.pop(field)
                        model.objects.create(**row)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Данные из файла {base} успешно импортированы"
                            f" в таблицу {model.__name__}."
                        )
                    )
        except Exception as error:
            CommandError(error)
