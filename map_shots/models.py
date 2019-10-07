from django.contrib.postgres.fields import ArrayField
from django.db import models


class Shot(models.Model):
    """
    Объединённый сникок карты со слоем пробок на конкретную дату и время
    """
    image = models.ImageField(
        verbose_name='Готовое изображение',
        upload_to='static/images/%Y/%m/%d/',
        null=True,
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now=True,
    )
    latlng = ArrayField(
        verbose_name='Координаты',
        base_field=models.DecimalField(
            decimal_places=6,
            max_digits=9,
        ),
    )

    class Meta:
        verbose_name = 'снимок'
        verbose_name_plural = 'Снимки'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.created}'


class ShotPart(models.Model):
    """
    Часть снимка карты со слоем пробок
    """
    shot = models.ForeignKey(
        Shot,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='static/images/%Y/%m/%d/%H_%M',
    )
    number = models.IntegerField(
        verbose_name='Номер снимка',
    )
    latlng = ArrayField(
        verbose_name='Координаты',
        base_field=models.DecimalField(
            decimal_places=6,
            max_digits=9,
        ),
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'часть'
        verbose_name_plural = 'части'
        ordering = ('-id',)

    def __unicode__(self):
        return self.number
