from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from map_shots.models import Shot, GeoSquare
from map_shots.tasks import make_combinations, make_shots


@admin.register(GeoSquare)
class GeoSquareAdmin(admin.ModelAdmin):
    change_form_template = 'admin/geosquare_change.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = HttpResponseRedirect(
            reverse('admin:map_shots_geosquare_change', args=(object_id,))
        )

        if request.GET.get('make_shot'):
            make_shots.delay(object_id)
        elif request.GET.get('make_combinations'):
            make_combinations.delay(object_id)
        else:
            response = super().change_view(
                request,
                object_id,
                form_url,
                extra_context
            )

        return response

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ('created', 'is_combination', 'image',)
    list_filter = ('is_combination', 'square',)
    list_select_related = ()
