import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

from foodgram.settings import JSON_FILES_DIR


class Command(BaseCommand):
    """Загрузка ингридиентов в БД."""

    def handle(self, *args, **options):
        path_to_json_file_ingr = f'{JSON_FILES_DIR}/ingredients.json'
        path_to_json_file_tags = f'{JSON_FILES_DIR}/tags.json'
        with open(path_to_json_file_ingr, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")

        with open(path_to_json_file_tags, 'r', encoding='UTF-8') as file:
            tags = json.load(file)

        for tag in tags:
            try:
                Tag.objects.get_or_create(**tag)
            except Exception as error:
                print(f"Что-то пошло не так. {error}")
