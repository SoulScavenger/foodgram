import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Загрузка ингридиентов в БД."""

    def handle(self, *args, **options):
        path_to_ingredients = settings.BASE_DIR / 'data/ingredients.json'
        path_to_tags = settings.BASE_DIR / 'data/tags.json'

        with open(path_to_ingredients, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")

        with open(path_to_tags, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")
