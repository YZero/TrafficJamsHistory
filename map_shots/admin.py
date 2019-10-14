from django.contrib import admin

from map_shots.models import Shot, GeoSquare


class ShotInlineAdmin(admin.TabularInline):
    readonly_fields = ('image', 'created')
    extra = 0
    model = Shot

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GeoSquare)
class GeoSquareAdmin(admin.ModelAdmin):
    inlines = (ShotInlineAdmin,)

    def has_delete_permission(self, request, obj=None):
        return False
