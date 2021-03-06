# Generated by Django 2.2.6 on 2019-10-14 20:59

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('map_shots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoSquare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название квадрата')),
                ('enabled', models.BooleanField(default=True, verbose_name='Включен')),
                ('start_latlng', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), size=None, verbose_name='Начальная точка')),
                ('end_latlng', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), size=None, verbose_name='Конечная точка')),
            ],
            options={
                'verbose_name': 'Квадрат',
                'verbose_name_plural': 'Квадраты',
            },
            managers=[
                ('enabled_squares', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='shot',
            options={'ordering': ('created',), 'verbose_name': 'снимок', 'verbose_name_plural': 'Снимки'},
        ),
        migrations.AlterModelOptions(
            name='shotpart',
            options={'ordering': ('number',), 'verbose_name': 'часть', 'verbose_name_plural': 'части'},
        ),
        migrations.AddField(
            model_name='shot',
            name='square',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='map_shots.GeoSquare'),
        ),
    ]
