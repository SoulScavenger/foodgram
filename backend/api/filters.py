from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)

from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    """Фильтр для Рецептов."""

    author = CharFilter(
        field_name='author__id',
        lookup_expr='icontains'
    )

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
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
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart_recipe__user=self.request.user)
        return queryset
