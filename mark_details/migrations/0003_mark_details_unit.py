# Generated by Django 4.1.6 on 2023-06-27 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mark_details', '0002_rename_mark_deatils_mark_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark_details',
            name='unit',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]