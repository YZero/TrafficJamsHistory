from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        blank=False,
    )

    class Meta:
        verbose_name = 'катогория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    единица измерения
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        blank=False,
    )

    class Meta:
        verbose_name = 'ед.изм'
        verbose_name_plural = 'единица измерения'

    def __str__(self):
        return self.name


class Nomenclature(models.Model):
    """
    номенклатура
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        blank=False,
    )

    class Meta:
        verbose_name = 'номенклатура'
        verbose_name_plural = 'справочник номенлатуры'

    def __str__(self):
        return self.name


class PersonalThing(models.Model):
    """
    Личная вещь
    """
    category = models.ForeignKey(
        to=Category,
        verbose_name='категория',
        related_name='personal_things',
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )
    nomenclature = models.ForeignKey(
        to=Nomenclature,
        verbose_name='наименование',
        related_name='personal_things',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name=u'единица измерения',
        related_name='personal_things',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        null=False,
        blank=False,
    )
    cost = models.IntegerField(
        verbose_name='Стоимость',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'вещь'
        verbose_name_plural = 'Личные вещи'
        ordering = ('-id',)

    def __str__(self):
        return (
            f'{self.nomenclature.name} - {self.quantity} '
            f'{self.unit.name} - {self.cost} руб.'
        )

