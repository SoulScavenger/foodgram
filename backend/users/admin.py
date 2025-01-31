from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, Subscribe


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Админка раздела пользователей."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_staff'
    )

    list_editable = ('is_staff',)
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админка раздела подписок."""

    list_display = (
        'id',
        'user',
        'author',
    )

    list_editable = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user__username', 'author__username')


admin.site.empty_value_display = 'Не задано'
