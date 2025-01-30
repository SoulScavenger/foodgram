from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from core.constants import (
    MAX_INGREDIENT_AMOUNT,
    MAX_INGREDIENT_NAME_LENGTH,
    MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
    MAX_RECIPE_NAME_LENGTH,
    MAX_TAG_NAME_LENGTH,
    MAX_TAG_SLUG_LENGTH,
    MAX_VIEW_LENGTH,
    MIN_COCKING_TIME,
    MIN_INGREDIENT_AMOUNT,
    TAG_REGEX)

from users.models import CustomUser


class Tag(models.Model):
    """Модель Тега."""

    name = models.CharField(
        max_length=MAX_TAG_NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_TAG_SLUG_LENGTH,
        validators=(RegexValidator(TAG_REGEX),),
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        default_related_name = 'tags'

    def __str__(self):
        return self.name[:MAX_VIEW_LENGTH]


class Ingredient(models.Model):
    """Модель Ингридиента."""

    name = models.CharField(
        max_length=MAX_INGREDIENT_NAME_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
        verbose_name='Единицы измерения.'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        default_related_name = 'ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return self.name[:MAX_VIEW_LENGTH]


class Recipe(models.Model):
    """Модель Рецепта."""

    name = models.CharField(
        max_length=MAX_RECIPE_NAME_LENGTH,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    cooking_time = models.SmallIntegerField(
        validators=[
            MinValueValidator(MIN_COCKING_TIME)
        ],
        verbose_name='Время приготовления (в минутах)'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    short_link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Короткая ссылка'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return self.name[:MAX_VIEW_LENGTH]


class RecipeTag(models.Model):
    """Модель Рецепта/Тега."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        default_related_name = 'recipe_tags'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]
        verbose_name = 'Связь Рецепт/Тег'
        verbose_name_plural = 'Связи Рецепты/Теги'

    def __str__(self):
        return self.tag.name[:MAX_VIEW_LENGTH]


class RecipeIngredient(models.Model):
    """Модель Рецепта/Ингридиента."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(MIN_INGREDIENT_AMOUNT),
            MaxValueValidator(MAX_INGREDIENT_AMOUNT)
        ],
        verbose_name='Количество'
    )

    class Meta:
        default_related_name = 'recipe_ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Связь Рецепт/Ингридиент'
        verbose_name_plural = 'Связи Рецепты/Ингридиенты'


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorite_recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'Избранные рецепт: {self.recipe} пользователя {self.user}'


class ShoppingCartRecipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        default_related_name = 'cart_recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart_recipe'
            )
        ]

    def __str__(self):
        return f'Рецепт: {self.recipe} в корзине пользователя {self.user}'
