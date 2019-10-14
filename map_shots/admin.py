from django.contrib import admin

from map_shots.models import Shot, GeoSquare


class ShotInlineAdmin(admin.TabularInline):
    readonly_fields = ('image', 'created')
    extra = 0
    model = Shot


@admin.register(GeoSquare)
class GeoSquareAdmin(admin.ModelAdmin):
    inlines = (ShotInlineAdmin,)
