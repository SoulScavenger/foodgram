# Generated by Django 3.2.3 on 2025-01-30 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='short_link',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='Короткая ссылка'),
        ),
    ]
