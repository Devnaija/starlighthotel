# Generated by Django 4.0.3 on 2022-03-06 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(default='pix.jpg', upload_to='media')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='pix.jpg', upload_to='media')),
                ('description', models.TextField()),
                ('available', models.BooleanField(default=True)),
                ('price', models.FloatField(default=True)),
                ('min_quantity', models.IntegerField(default=1)),
                ('max_quantity', models.IntegerField(default=1)),
                ('min_occupants', models.IntegerField(default=1)),
                ('max_occupants', models.IntegerField(default=1)),
                ('min_adults', models.IntegerField(default=1)),
                ('max_adults', models.IntegerField(default=1)),
                ('min_kids', models.IntegerField(default=1)),
                ('max_kids', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reservation_no', models.CharField(max_length=36)),
                ('pay_code', models.CharField(max_length=36)),
                ('paid_order', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('image', models.ImageField(default='pix.jpg', upload_to='client')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('reservation_no', models.CharField(max_length=50)),
                ('paid_order', models.BooleanField()),
                ('check_in', models.DateField(default=1)),
                ('check_out', models.DateField(default=1)),
                ('adults', models.IntegerField(default=1)),
                ('kids', models.IntegerField(default=1)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelapp.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
