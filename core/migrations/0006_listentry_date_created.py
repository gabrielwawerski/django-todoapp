# Generated by Django 4.1 on 2022-08-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_listentry_order_with_respect_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='listentry',
            name='date_created',
            field=models.DateTimeField(auto_now=True, verbose_name='date created'),
        ),
    ]
