# Generated by Django 4.1.5 on 2023-01-13 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0002_pelicula'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pelicula',
            new_name='Movie',
        ),
    ]
