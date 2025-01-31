from rest_framework.pagination import PageNumberPagination

from core.constants import DEFAULT_PAGINATION


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация."""

    page_size = DEFAULT_PAGINATION
    page_size_query_param = 'limit'
