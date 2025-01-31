import json
import os

from django.core.management.base import BaseCommand

from core.constants import DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    """Загрузка ингридиентов в БД."""

    def handle(self, *args, **options):
        # os.chdir(DIR)
        path_to_ingr = os.getcwd()
        path_to_ingredients = os.path.join(path_to_ingr, 'ingredients.json')
        # path_to_tags = os.path.join(path_to_ingr, 'tags.json')

        with open(path_to_ingredients, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")

        # with open(path_to_tags, 'r', encoding='UTF-8') as file:
        #     ingredients = json.load(file)

        # for ingredient in ingredients:
        #     try:
        #         Ingredient.objects.get_or_create(**ingredient)
        #     except Exception as error:
        #         print(f"Что-то пошло не так. {error}")
