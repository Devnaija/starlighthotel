# Generated by Django 4.0.3 on 2022-03-07 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='image',
        ),
        migrations.RemoveField(
            model_name='room',
            name='min_quantity',
        ),
    ]
