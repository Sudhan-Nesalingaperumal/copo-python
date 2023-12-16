# Generated by Django 4.2.2 on 2023-06-15 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_unit_details_assessment'),
        ('academic', '0005_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='question_pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('question_no', models.CharField(max_length=100)),
                ('question', models.CharField(max_length=100)),
                ('marks_allotted', models.CharField(max_length=100)),
                ('exam_date', models.DateField()),
                ('co_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='co_question', to='settings.co_import')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depart_question', to='academic.course')),
            ],
            options={
                'verbose_name_plural': 'question_pattern',
            },
        ),
    ]