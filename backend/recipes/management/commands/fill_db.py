import json
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from foodgram.settings import PATH_TO_INGREDIENTS, PATH_TO_TAGS
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    """Загрузка ингридиентов в БД."""

    def handle(self, *args, **options):

        with open(PATH_TO_INGREDIENTS, 'r', encoding='UTF-8') as file:
            ingredients = json.load(file)

            for ingredient in tqdm(ingredients):
                try:
                    Ingredient.objects.get_or_create(**ingredient)
                except CommandError as error:
                    raise CommandError(
                        f'Ошибка при добавление ингридиента: {ingredient}.'
                        f' Описание: {error}'
                    )

        with open(PATH_TO_TAGS, 'r', encoding='UTF-8') as file:
            tags = json.load(file)

            for tag in tqdm(tags):
                try:
                    Tag.objects.get_or_create(**tag)
                except CommandError as error:
                    raise CommandError(
                        f'Ошибка при добавление тега: {tag}.'
                        f' Описание: {error}'
                    )
