# Generated by Django 4.2.2 on 2023-06-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('employee_id', models.CharField(max_length=100, unique=True, verbose_name='employee_id')),
                ('username', models.CharField(max_length=100, verbose_name='username')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('department', models.CharField(max_length=100, verbose_name='department')),
                ('designation', models.CharField(max_length=100, verbose_name='designation')),
                ('password', models.CharField(max_length=100, verbose_name='password')),
            ],
            options={
                'verbose_name_plural': 'user',
            },
        ),
    ]
