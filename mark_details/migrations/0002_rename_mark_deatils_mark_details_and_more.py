# Generated by Django 4.1.6 on 2023-06-24 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_question_pattern_unit'),
        ('mark_details', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mark_Deatils',
            new_name='Mark_Details',
        ),
        migrations.AlterModelOptions(
            name='mark_details',
            options={'verbose_name_plural': 'Mark_Details'},
        ),
    ]
