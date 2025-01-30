import json
import os

from django.core.management.base import BaseCommand

from core.constants import DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    """Загрузка ингридиентов в БД."""

    def handle(self, *args, **options):
        os.chdir(DIR)
        path_to_csv_folder = os.getcwd()
        path_to_file = os.path.join(path_to_csv_folder, 'ingredients.json')
        print(path_to_file)

        with open(path_to_file, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")
