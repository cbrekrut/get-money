# Generated by Django 4.2 on 2024-01-30 11:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0005_data_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='date'),
        ),
    ]
