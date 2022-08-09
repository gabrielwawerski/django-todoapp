# Generated by Django 4.1 on 2022-08-09 05:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_rename_user_list_owner_list_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', to=settings.AUTH_USER_MODEL),
        ),
    ]