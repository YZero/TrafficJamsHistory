# Generated by Django 2.2.6 on 2019-11-14 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_shots', '0006_auto_20191028_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='is_combination',
            field=models.BooleanField(default=False, verbose_name='Объединённый снимок'),
        ),
    ]