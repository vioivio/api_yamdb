# Generated by Django 3.2 on 2023-11-06 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
