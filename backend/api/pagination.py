from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация."""

    page_size = 5
    page_size_query_param = 'limit'
