# Generated by Django 4.1 on 2022-08-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_listentry_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listentry',
            name='date_created',
            field=models.DateTimeField(verbose_name='date created'),
        ),
    ]