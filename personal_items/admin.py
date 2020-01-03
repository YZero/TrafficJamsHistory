from django.contrib import admin

from personal_items.models import PersonalThing, Nomenclature, Unit, Category


@admin.register(PersonalThing)
class PersonalThingAdmin(admin.ModelAdmin):
    pass


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
