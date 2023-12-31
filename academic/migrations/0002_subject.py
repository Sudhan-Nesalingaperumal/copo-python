# Generated by Django 4.2.2 on 2023-06-14 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('degree', models.CharField(max_length=100)),
                ('subject_code', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('staff_name', models.CharField(max_length=100)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='academic.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='academic.course')),
            ],
            options={
                'verbose_name_plural': 'subject',
            },
        ),
    ]
