from django.contrib import admin

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCartRecipe,
    Tag
)


class BaseFavoriteShopping(admin.ModelAdmin):
    """Базовый класс для Избранного/Списка покупок."""

    list_display = (
        'id',
        'user',
        'recipe',
    )

    list_filter = ('user__username', 'recipe')
    search_fields = ('user__username', 'recipe')


class BaseInline(admin.StackedInline):
    """Базовый класс для строчного представления."""
    extra = 0
    min_num = 1


class RecipeIngredientInline(BaseInline):
    """Строчное представление Ингредиента в Рецепте"""

    model = RecipeIngredient


class RecipeTagInline(BaseInline):
    """Строчное представление Ингредиента в Рецепте"""

    model = RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов"""

    list_display = (
        'name',
        'get_username',
        'text',
        'image',
        'cooking_time',
        'get_ingredients',
        'get_tags',
        'created_at',
        'added_to_favorite',
    )
    search_fields = (
        'author__username',
        'name'
    )
    list_filter = ('name', 'tags',)
    filter_horizontal = ('tags',)
    inlines = [RecipeIngredientInline, RecipeTagInline]

    def get_username(self, object):
        """Автор рецепта."""
        return object.author.username
    get_username.short_description = 'Автор'

    def get_ingredients(self, object):
        """Список тегов."""
        return '\n'.join(
            obj.ingredient.name for obj in object.recipe_ingredients.all()
        )
    get_ingredients.short_description = 'Ингридиенты'

    def get_tags(self, object):
        """Список тегов."""
        return '\n'.join(obj.tag.name for obj in object.recipe_tags.all())
    get_tags.short_description = 'Теги'

    def added_to_favorite(self, object):
        """Популярность рецепта."""
        return object.favorite_recipe.count()
    added_to_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка Тегов."""

    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
    )

    list_display_links = ('id', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка Ингридиента."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )

    list_editable = (
        'name',
        'measurement_unit',
    )

    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('id', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка Рецепта/Ингридиента."""

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )

    list_filter = ('recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')
    list_display_links = ('recipe', 'ingredient')


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    """Админка Рецепта/Тега."""
    list_display = (
        'recipe',
        'tag',
    )

    list_filter = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')
    list_display_links = ('recipe', 'tag')


@admin.register(FavoriteRecipe)
class FavoriteAdmin(BaseFavoriteShopping):
    """Админка Избранного."""


@admin.register(ShoppingCartRecipe)
class ShoppingCartAdmin(BaseFavoriteShopping):
    """Админка Списка Покупок."""


admin.site.empty_value_display = 'Не задано'
