# Generated by Django 4.1.6 on 2023-07-17 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0009_alter_question_pattern_marks_allotted'),
        ('mark_details', '0003_mark_details_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='CO_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('au_results', models.CharField(max_length=50)),
                ('Assignment_1', models.IntegerField()),
                ('Assignment_2', models.IntegerField()),
                ('Assignment_3', models.IntegerField()),
                ('Assignment_4', models.IntegerField()),
                ('Assignment_5', models.IntegerField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_details', to='academic.student')),
            ],
            options={
                'verbose_name_plural': 'CO_Data',
            },
        ),
    ]