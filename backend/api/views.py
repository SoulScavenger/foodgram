from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from api.filters import RecipeFilterSet
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AvatarSerializer,
    ShoppingCartRecipeSerializer,
    CreateCustomUserSerializer,
    CreateRecipeSerializer,
    CreateSubscribeSerializer,
    FavoriteRecipeSerializer,
    GetCustomUserSerializer,
    GetRecipeSerializer,
    GetSubscribeSerializer,
    IngredientSerializer,
    TagSerializer,
)
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCartRecipe,
    Tag
)
from users.models import CustomUser, Subscribe


# Вьюсеты пользователя.
class CustomUserViewSet(UserViewSet):
    """Вьюсет создания кастомного пользователя."""

    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if (
            self.action == 'list'
            or self.action == 'retrieve'
            or self.action == 'me'
        ):
            return GetCustomUserSerializer
        return super().get_serializer_class()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def me(self, request):
        """Просмотр профиля пользователя."""
        user = get_object_or_404(CustomUser, username=request.user.username)
        serializer = GetCustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me/avatar',
        url_name='avatar'
    )
    def avatar(self, request):
        """Редактирование аватара."""
        instance = self.request.user
        if request.method == 'DELETE':
            instance.avatar = None
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AvatarSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<id>\d+)/subscribe',
        url_name='subscribe',
    )
    def subscribe(self, request, id):
        """Управление подпиской."""
        user = self.request.user
        author = get_object_or_404(CustomUser, id=id)
        if self.request.method == 'POST':
            serializer = CreateSubscribeSerializer(
                data={'user': user.id, 'author': author.id},
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        unsubscribe, _ = Subscribe.objects.filter(
            user=user,
            author=author,
        ).delete()
        if unsubscribe == 0:
            return Response(
                f"Подписка на {author.username} отсутствует",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def get_subscriptions(self, request):
        """Получения списка подписок."""
        user = self.request.user
        subscribes = CustomUser.objects.filter(author__user=user)
        paginator = CustomPagination()
        result_pages = paginator.paginate_queryset(
            queryset=subscribes, request=request
        )
        serializer = GetSubscribeSerializer(
            result_pages, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)


# Вьюсеты рецепта.
class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет Тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет Ингридиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(
    viewsets.ModelViewSet,
):
    """Вьюсет Рецепта."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateRecipeSerializer
        return GetRecipeSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path=r'(?P<id>\d+)/get-link',
        url_name='get-link',
    )
    def get_link(self, request, id):
        """Добавление и удаление рецепта из избранного."""
        return Response("link")

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['post', 'delete'],
        url_path=r'(?P<id>\d+)/favorite',
        url_name='favorite',
    )
    def add_recipe_to_favorite(self, request, id):
        """Добавление и удаление рецепта из избранного."""
        recipe = get_object_or_404(Recipe, id=id)
        user = self.request.user
        if self.request.method == 'POST':
            serializer = FavoriteRecipeSerializer(
                data={'user': user.id, 'recipe': recipe.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = FavoriteRecipe.objects.filter(
            user=user, recipe=recipe
        )
        if len(recipe) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['post', 'delete'],
        url_path=r'(?P<id>\d+)/shopping_cart',
        url_name='shopping_cart',
    )
    def add_recipe_to_shopping_cart(self, request, id):
        """Добавление и удаление рецепта в корзину покупок."""
        recipe = get_object_or_404(Recipe, id=id)
        user = self.request.user
        if self.request.method == 'POST':
            serializer = ShoppingCartRecipeSerializer(
                data={'user': user.id, 'recipe': recipe.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = ShoppingCartRecipe.objects.filter(
            user=user, recipe=recipe
        )
        if len(recipe) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart_recipe__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response
