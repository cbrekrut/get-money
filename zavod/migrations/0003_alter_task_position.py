# Generated by Django 5.0 on 2024-01-06 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zavod', '0002_data_rename_description_task_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zavod.position'),
        ),
    ]
