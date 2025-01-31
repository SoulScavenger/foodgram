from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    AllValuesMultipleFilter
)

from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    """Фильтр для Рецептов."""

    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )

    is_favorited = BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart_recipes__user=self.request.user)
        return queryset
