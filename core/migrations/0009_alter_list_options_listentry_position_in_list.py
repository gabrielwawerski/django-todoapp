# Generated by Django 4.1 on 2022-08-11 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_listentry_date_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='list',
            options={'ordering': ['date_created']},
        ),
        migrations.AddField(
            model_name='listentry',
            name='position_in_list',
            field=models.IntegerField(default=0),
        ),
    ]