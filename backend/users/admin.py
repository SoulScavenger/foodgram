from django.contrib import admin

from users.models import CustomUser, Subscribe


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
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
    search_fields = ('username',)


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
    search_fields = ('user', 'author')


admin.site.empty_value_display = 'Не задано'
