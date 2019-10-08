# Generated by Django 2.2.6 on 2019-10-08 21:17

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images/%Y/%m/%d/', verbose_name='Готовое изображение')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('start_latlng', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), size=None, verbose_name='Начальная точка')),
                ('end_latlng', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), size=None, verbose_name='Конечная точка')),
            ],
            options={
                'verbose_name': 'снимок',
                'verbose_name_plural': 'Снимки',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ShotPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/%H_%M', verbose_name='изображение')),
                ('number', models.IntegerField(verbose_name='Номер снимка')),
                ('latlng', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), size=None, verbose_name='Координаты')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map_shots.Shot')),
            ],
            options={
                'verbose_name': 'часть',
                'verbose_name_plural': 'части',
                'ordering': ('-id',),
            },
        ),
    ]
