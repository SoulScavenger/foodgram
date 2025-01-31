from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.constants import MIN_PASSWORD_LENGTH
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCartRecipe,
    Tag
)
from users.models import User, Subscribe


# Сериализаторы пользователя.
class GetUserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_subscribe_status'
    )
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )

    def get_subscribe_status(self, author):
        return False


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания кастомного пользователя."""

    password = serializers.CharField(
        min_length=MIN_PASSWORD_LENGTH, write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватарки"""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class GetSubscribeSerializer(GetUserSerializer):
    """Сериализатор получения подписок."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_subscribe_status'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )

    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = GetUserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_subscribe_status(self, author):
        user = self.context.get('request').user
        return user.followings.filter(author=author).exists()

    def get_recipes(self, author):
        recipes = author.recipes.all()
        request = self.context.get('request')
        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:int(recipes_limit)]
            except ValueError as err:
                print(f'Невозможно преобразовать в int. Описание: {err}')
        return GetShortRecipeSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, author):
        return author.recipes.count()


class CreateSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""

    class Meta:
        fields = ('user', 'author')
        model = Subscribe

    def validate(self, data):
        follower = data['user']
        following = data['author']

        if follower == following:
            raise serializers.ValidationError('Нельзя подписаться на себя...')

        is_subscribe_in_table = Subscribe.objects.select_related(
            'user', 'author'
        ).filter(user=follower, author=following).exists()

        if is_subscribe_in_table:
            raise serializers.ValidationError('Подписка уже оформлена...')

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return GetSubscribeSerializer(
            instance.author, context={'request': request}
        ).data


# Сериализаторы Тега.
class GetRecipeTagSerializer(serializers.ModelSerializer):
    """Сериализатор получения связи Рецепт/Тег."""

    id = serializers.IntegerField(source='tag.id')
    name = serializers.CharField(source='tag.name')
    slug = serializers.SlugField(
        source='tag.slug'
    )

    class Meta:
        model = RecipeTag
        fields = (
            'id',
            'name',
            'slug'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тега."""

    class Meta:
        model = Tag
        fields = '__all__'


# Сериализаторы Ингридиента.
class GetRecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор получения связи Рецепт/Ингридиент."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Тега."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор создания связи Рецепт/Ингридиент."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


# Сериализаторы Рецепта.
class GetShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор получения краткой информацией Рецепта."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор получения полной информации Рецепта."""

    tags = GetRecipeTagSerializer(many=True, source='recipe_tags')
    author = GetUserSerializer(read_only=True)
    ingredients = GetRecipeIngredientsSerializer(
        source='recipe_ingredients',
        many=True
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and request.user.favorite_recipes.all().exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and request.user.cart_recipes.all().exists()
        )


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор создания Рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = CreateRecipeIngredientSerializer(
        many=True, source='recipe_ingredients'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        tags = data.get('tags')
        ingredients = data.get('recipe_ingredients')
        if not tags:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле tags'
            )
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле ingredients'
            )

        ingredients_length = len(ingredients)
        if ingredients_length == 0:
            raise serializers.ValidationError('Не может быть пустым.')
        ingredients_id = [
            ingredient['ingredient'].id for ingredient in ingredients
        ]
        if len(set(ingredients_id)) != ingredients_length:
            raise serializers.ValidationError(
                'Данные должны быть уникальными.'
            )
        return data

    def validate_image(self, value):
        if value:
            return value
        raise serializers.ValidationError(
            'Не может быть пустым.'
        )

    def validate_tags(self, value):
        value_length = len(value)
        if not value_length:
            raise serializers.ValidationError('Не может быть пустым.')
        if len(set(value)) != value_length:
            raise serializers.ValidationError(
                'Данные должны быть уникальными.'
            )
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        RecipeTag.objects.bulk_create(
            (
                RecipeTag(
                    recipe=recipe,
                    tag=tag,
                )
                for tag in tags
            )
        )
        RecipeIngredient.objects.bulk_create(
            (
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            )
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=instance)
        recipe_tags = RecipeTag.objects.filter(recipe=instance)
        recipe_tags.delete()
        recipe_ingredients.delete()

        RecipeTag.objects.bulk_create(
            (
                RecipeTag(
                    recipe=instance,
                    tag=tag,
                )
                for tag in tags
            )
        )
        RecipeIngredient.objects.bulk_create(
            (
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            )
        )

        return instance

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


# Сериализатор избранного Рецепта.
class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецептов в избранное."""

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'

    def validate(self, data):
        is_favorite = FavoriteRecipe.objects.filter(**data).exists()
        if is_favorite:
            raise serializers.ValidationError(
                f'Рецепт \'{data["recipe"]}\''
                'уже добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        return GetShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


# Сериализатор купленного Рецепта.
class ShoppingCartRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецептов в корзину покупок."""

    class Meta:
        model = ShoppingCartRecipe
        fields = '__all__'

    def validate(self, data):
        is_in_cart = ShoppingCartRecipe.objects.filter(**data).exists()
        if is_in_cart:
            raise serializers.ValidationError(
                f'Рецепт \'{data["recipe"]}\''
                'уже добавлен в избранное.'
            )
        return data

    # def create(self, validated_data):
    #     favorite_recipe, status = ShoppingCartRecipe.objects.get_or_create(
    #         **validated_data
    #     )
    #     if not status:
    #         raise serializers.ValidationError(
    #             f'Рецепт \'{validated_data["recipe"]}\''
    #             'уже добавлен в корзину.'
    #         )
    #     return favorite_recipe

    def to_representation(self, instance):
        return GetShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
