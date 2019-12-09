from django.contrib import admin

from personal_items.models import PersonalThing, Nomenclature, Unit


@admin.register(PersonalThing)
class PersonalThingAdmin(admin.ModelAdmin):
    pass


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
