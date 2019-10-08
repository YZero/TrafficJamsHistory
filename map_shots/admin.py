from django.contrib import admin

from map_shots.models import Shot, ShotPart


class ShotPartInlineAdmin(admin.TabularInline):
    readonly_fields = ('image', 'number', 'created', 'latlng',)
    extra = 0
    model = ShotPart


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    readonly_fields = ('image', 'created', 'start_latlng', 'end_latlng')
    # inlines = (ShotPartInlineAdmin,)
