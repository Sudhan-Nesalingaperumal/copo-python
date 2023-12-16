# Generated by Django 4.2.2 on 2023-06-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_co_import'),
    ]

    operations = [
        migrations.CreateModel(
            name='po_import',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('po_number', models.CharField(max_length=100)),
                ('po', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'po_import',
            },
        ),
    ]
