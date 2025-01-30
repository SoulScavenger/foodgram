from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomUserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tag')
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')
router_v1.register('recipes', RecipeViewSet, basename='recipe')
router_v1.register('users', CustomUserViewSet, basename='customuser')

api_v1_urls = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('', include(api_v1_urls))
]
